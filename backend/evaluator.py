"""
evaluator.py
============

This file ties together classifier.py, router.py, and cost.py to run the
fixed benchmark in data/benchmark.json and answer the hackathon's core
question: "how much does our optimized routing system save compared to
always using the powerful model, without sacrificing quality?"

WHAT THIS FILE DELIBERATELY DOES NOT DO YET:
It does NOT call any real LLM API. There is no import of llm_clients.py
and no OpenAI SDK usage here, and it must never contain an API key.
That's intentional: real LLM calls (with real token usage and real model
output to score for quality) are wired in as a later step. Until then,
this evaluator:
  - estimates token counts from prompt text length (clearly labeled as an
    ESTIMATE, not real usage),
  - leaves `quality_score` and `latency_ms` as None placeholders on every
    result.
That keeps this module honest: nothing here pretends a cost saving is
real before it's backed by actual token usage, per the project's rule
against fabricating savings numbers.

WHEN REAL LLM CALLS ARE ENABLED (a future step):
The plan is for whatever calls this evaluator (e.g. main.py, or an
updated run_benchmark) to optionally pass in a real "generate" callable
(matching llm_clients.generate_response's signature) so token counts come
from actual API usage and quality_score/latency_ms get populated from
real responses -- without evaluator.py itself ever importing llm_clients.py
directly or holding an API key.

PIPELINE PER BENCHMARK ITEM:
    1. classifier.classify(prompt)          -> difficulty + confidence
    2. router.route_request(difficulty)     -> selected model tier + reason
    3. estimate_tokens(prompt)              -> estimated prompt/completion tokens
    4. cost.calculate_cost(..., tier)       -> optimized cost
    5. cost.calculate_cost(..., POWERFUL)   -> baseline cost (always-powerful)
    6. cost.calculate_savings(...)          -> savings vs baseline
    7. quality_score=None, latency_ms=None  -> placeholders for later

WHERE THIS FILE LIVES:
    LLMcostoptimizer/backend/evaluator.py
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

from classifier import RuleBasedDifficultyClassifier
from cost import CostBreakdown, SavingsResult, calculate_cost, calculate_savings
from router import route_request
from schemas import DifficultyLevel, ModelTier

# ---------------------------------------------------------------------------
# CONFIGURATION
# ---------------------------------------------------------------------------

# Default location of the benchmark file, relative to the project root.
# Exposed as a constant (and as a parameter on run_benchmark) rather than
# hard-coded inline, so tests or other callers can point at a different
# benchmark file without editing this module.
DEFAULT_BENCHMARK_PATH = Path(__file__).resolve().parent.parent / "data" / "benchmark.json"

# --- Token estimation configuration ---
# Until real LLM calls are wired in, we don't have real token usage, so we
# use a simple, clearly-labeled ESTIMATE based on text length. ~4
# characters per token is a commonly used rough approximation for
# English text with GPT-style tokenizers.
CHARS_PER_TOKEN_ESTIMATE: float = float(os.environ.get("CHARS_PER_TOKEN_ESTIMATE", 4.0))

# We also don't have a real completion yet, so we assume a fixed
# estimated completion length (in tokens) for every benchmark item. This
# is intentionally simple and configurable via an env var so it's obvious
# in the demo that it's a stand-in, not a measured value.
ASSUMED_COMPLETION_TOKENS: int = int(os.environ.get("ASSUMED_COMPLETION_TOKENS", 300))


def estimate_tokens(text: str) -> int:
    """
    Roughly estimate the number of tokens in `text` from its character
    count.

    This is a placeholder for real tokenization. It exists so cost.py can
    be exercised end-to-end on the benchmark before real LLM calls (and
    therefore real usage numbers) are wired in. Swap this out for a real
    tokenizer (e.g. tiktoken) or real API usage once available -- nothing
    else in this file needs to change, since every caller just treats
    this as "the token count for this text."
    """
    if not text:
        return 0
    return max(1, int(len(text) / CHARS_PER_TOKEN_ESTIMATE))


# ---------------------------------------------------------------------------
# RESULT DATA STRUCTURES
# ---------------------------------------------------------------------------


@dataclass
class BenchmarkResult:
    """Everything recorded for a single benchmark prompt."""

    id: str
    category: str
    prompt: str
    expected_difficulty: DifficultyLevel

    # Step 1: classifier output
    classified_difficulty: DifficultyLevel
    classifier_confidence: float
    classifier_explanation: str

    # Step 2-3: router output
    selected_model_tier: ModelTier
    routing_reason: str

    # Token estimates fed into cost calculations (see estimate_tokens()).
    estimated_prompt_tokens: int
    estimated_completion_tokens: int

    # Step 4-6: cost and savings
    optimized_cost: CostBreakdown
    baseline_cost: CostBreakdown
    savings: SavingsResult

    # Step 7: placeholders, populated once real LLM calls are enabled.
    quality_score: Optional[float] = None
    latency_ms: Optional[float] = None


@dataclass
class BenchmarkSummary:
    """Aggregate totals across every BenchmarkResult in a run."""

    total_items: int
    total_baseline_cost_usd: float
    total_optimized_cost_usd: float
    total_savings_usd: float
    total_savings_percent: float
    tier_distribution: dict[str, int] = field(default_factory=dict)


# ---------------------------------------------------------------------------
# BENCHMARK LOADING
# ---------------------------------------------------------------------------


def load_benchmark(path: Path | str = DEFAULT_BENCHMARK_PATH) -> list[dict]:
    """
    Load the benchmark prompt list from a JSON file.

    Parameters
    ----------
    path: Path | str
        Path to the benchmark JSON file. Defaults to
        LLMcostoptimizer/data/benchmark.json.

    Returns
    -------
    list[dict]
        The raw list of benchmark items (id/category/prompt/expected_difficulty),
        exactly as stored in the JSON file.
    """
    path = Path(path)
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


# ---------------------------------------------------------------------------
# EVALUATION
# ---------------------------------------------------------------------------


def evaluate_item(item: dict, classifier: RuleBasedDifficultyClassifier) -> BenchmarkResult:
    """
    Run the full classify -> route -> cost -> savings pipeline for one
    benchmark item.

    Parameters
    ----------
    item: dict
        A single benchmark entry with keys: id, category, prompt,
        expected_difficulty.
    classifier: RuleBasedDifficultyClassifier
        The classifier instance to use (passed in rather than constructed
        here, so callers can swap in a different classifier implementation
        without editing this function).

    Returns
    -------
    BenchmarkResult
    """
    prompt = item["prompt"]

    # 1. Run the classifier.
    classification = classifier.classify(prompt)

    # 2-3. Run the router and record the selected tier.
    decision = route_request(classification.difficulty)

    # Estimated token counts (see estimate_tokens() docstring for why
    # these are estimates, not real usage).
    prompt_tokens = estimate_tokens(prompt)
    completion_tokens = ASSUMED_COMPLETION_TOKENS

    # 4. Optimized cost: whatever tier the router actually selected.
    optimized_cost = calculate_cost(prompt_tokens, completion_tokens, decision.model_tier)

    # 5. Baseline cost: what it would have cost if we always used the
    # powerful model, for the exact same token counts.
    baseline_cost = calculate_cost(prompt_tokens, completion_tokens, ModelTier.POWERFUL)

    # 6. Savings vs baseline.
    savings = calculate_savings(baseline_cost.total_cost_usd, optimized_cost.total_cost_usd)

    # 7. Quality/latency are left as placeholders until real LLM calls
    # are enabled -- see module docstring.
    return BenchmarkResult(
        id=item["id"],
        category=item["category"],
        prompt=prompt,
        expected_difficulty=DifficultyLevel(item["expected_difficulty"]),
        classified_difficulty=classification.difficulty,
        classifier_confidence=classification.confidence,
        classifier_explanation=classification.explanation,
        selected_model_tier=decision.model_tier,
        routing_reason=decision.reason,
        estimated_prompt_tokens=prompt_tokens,
        estimated_completion_tokens=completion_tokens,
        optimized_cost=optimized_cost,
        baseline_cost=baseline_cost,
        savings=savings,
        quality_score=None,
        latency_ms=None,
    )


def run_benchmark(
    benchmark_path: Path | str = DEFAULT_BENCHMARK_PATH,
    classifier: Optional[RuleBasedDifficultyClassifier] = None,
) -> list[BenchmarkResult]:
    """
    Run the full evaluation pipeline over every item in the benchmark file.

    Parameters
    ----------
    benchmark_path: Path | str
        Path to the benchmark JSON file. Defaults to data/benchmark.json.
    classifier: RuleBasedDifficultyClassifier, optional
        Classifier instance to use. A fresh one is created if not
        provided -- exposed as a parameter so a different/tuned classifier
        can be injected without changing this function.

    Returns
    -------
    list[BenchmarkResult]
        One BenchmarkResult per benchmark item, in the file's order.
    """
    if classifier is None:
        classifier = RuleBasedDifficultyClassifier()

    items = load_benchmark(benchmark_path)
    return [evaluate_item(item, classifier) for item in items]


def summarize_results(results: list[BenchmarkResult]) -> BenchmarkSummary:
    """
    Aggregate a list of BenchmarkResults into overall totals.

    Useful for a top-line demo number ("optimized routing saved $X, or
    Y%, versus always using the powerful model across N benchmark
    prompts") as well as showing how requests were distributed across
    model tiers.
    """
    total_baseline = sum(r.baseline_cost.total_cost_usd for r in results)
    total_optimized = sum(r.optimized_cost.total_cost_usd for r in results)
    total_savings = calculate_savings(total_baseline, total_optimized)

    tier_distribution: dict[str, int] = {}
    for r in results:
        key = r.selected_model_tier.value
        tier_distribution[key] = tier_distribution.get(key, 0) + 1

    return BenchmarkSummary(
        total_items=len(results),
        total_baseline_cost_usd=total_baseline,
        total_optimized_cost_usd=total_optimized,
        total_savings_usd=total_savings.savings_usd,
        total_savings_percent=total_savings.savings_percent,
        tier_distribution=tier_distribution,
    )
