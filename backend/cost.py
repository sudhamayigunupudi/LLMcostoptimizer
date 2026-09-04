"""
cost.py
=======

This file turns raw token counts into dollar amounts, and compares costs
between the "always use the powerful model" baseline and our optimized
routing system.

WHY THIS IS A SEPARATE FILE:
  - llm_clients.py's only job is calling the LLM API and reporting back
    how many tokens were used (UsageInfo: prompt_tokens/completion_tokens).
  - cost.py's only job is turning those token counts into a dollar figure,
    using configurable per-tier pricing.
Splitting these means cost.py has ZERO network dependency -- it's pure
arithmetic, so it can be unit tested instantly and reused anywhere (e.g.
by evaluator.py to compute baseline-vs-optimized comparisons) without
ever touching the OpenAI SDK.

PRICING CONFIGURATION (never hard-coded inside the calculation logic):
Prices are read from environment variables, expressed as USD per 1,000
tokens (a common way LLM providers publish pricing):

    CHEAP_INPUT_PRICE_PER_1K
    CHEAP_OUTPUT_PRICE_PER_1K
    POWERFUL_INPUT_PRICE_PER_1K
    POWERFUL_OUTPUT_PRICE_PER_1K

These should be set in the project's `.env` file to match whatever real
pricing the CHEAP_MODEL / POWERFUL_MODEL (from llm_clients.py) actually
charge, so the cost numbers shown in the demo are real, not invented --
per the hackathon rule against pretending savings are real.

WHERE THIS FILE LIVES:
    LLMcostoptimizer/backend/cost.py
"""

from __future__ import annotations

import os
from dataclasses import dataclass

from schemas import ModelTier


# ---------------------------------------------------------------------------
# CONFIGURATION: per-tier pricing, read from environment variables
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class TierPricing:
    """USD price per 1,000 tokens for one model tier."""

    input_price_per_1k: float
    output_price_per_1k: float


def _read_price(env_var: str, default: float) -> float:
    """
    Read a price from an environment variable, falling back to `default`
    if it's unset or not a valid number.

    Falling back instead of crashing keeps this module importable (and
    its arithmetic testable) even before a .env file with real prices has
    been set up -- but real demo numbers should always come from actual
    configured pricing, not these fallback defaults.
    """
    raw_value = os.environ.get(env_var)
    if raw_value is None:
        return default
    try:
        return float(raw_value)
    except ValueError:
        return default


# Fallback defaults are illustrative placeholders only (roughly in the
# ballpark of typical small-vs-large model pricing) -- set the real
# environment variables in .env for accurate demo numbers.
_PRICING: dict[ModelTier, TierPricing] = {
    ModelTier.CHEAP: TierPricing(
        input_price_per_1k=_read_price("CHEAP_INPUT_PRICE_PER_1K", 0.00015),
        output_price_per_1k=_read_price("CHEAP_OUTPUT_PRICE_PER_1K", 0.0006),
    ),
    ModelTier.POWERFUL: TierPricing(
        input_price_per_1k=_read_price("POWERFUL_INPUT_PRICE_PER_1K", 0.0025),
        output_price_per_1k=_read_price("POWERFUL_OUTPUT_PRICE_PER_1K", 0.01),
    ),
}


def get_pricing(tier: ModelTier) -> TierPricing:
    """
    Return the configured TierPricing for a given tier.

    Exposed as its own function (rather than making callers reach into
    the private _PRICING dict directly) so evaluator.py or a future
    /metrics endpoint can display "here's the pricing we're using" in the
    demo without depending on this module's internal storage format.
    """
    pricing = _PRICING.get(tier)
    if pricing is None:
        raise ValueError(f"No pricing configured for tier: {tier!r}")
    return pricing


# ---------------------------------------------------------------------------
# COST CALCULATION
# ---------------------------------------------------------------------------


@dataclass
class CostBreakdown:
    """The result of calculate_cost(): a full breakdown of one request's cost."""

    model_tier: ModelTier
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
    input_cost_usd: float
    output_cost_usd: float
    total_cost_usd: float


def calculate_cost(
    prompt_tokens: int,
    completion_tokens: int,
    tier: ModelTier,
) -> CostBreakdown:
    """
    Calculate the USD cost of a single request from its token counts.

    Parameters
    ----------
    prompt_tokens: int
        Number of input ("prompt") tokens used, as reported by the LLM API.
    completion_tokens: int
        Number of output ("completion") tokens generated.
    tier: ModelTier
        Which model tier was used -- determines which configured price to
        apply. Pricing itself lives in `_PRICING` / the environment
        variables above, never inline in this function.

    Returns
    -------
    CostBreakdown
        input_cost_usd, output_cost_usd, total_cost_usd, and total_tokens.
    """
    if prompt_tokens < 0 or completion_tokens < 0:
        raise ValueError("Token counts cannot be negative.")

    pricing = get_pricing(tier)

    input_cost = (prompt_tokens / 1000.0) * pricing.input_price_per_1k
    output_cost = (completion_tokens / 1000.0) * pricing.output_price_per_1k
    total_cost = input_cost + output_cost

    return CostBreakdown(
        model_tier=tier,
        prompt_tokens=prompt_tokens,
        completion_tokens=completion_tokens,
        total_tokens=prompt_tokens + completion_tokens,
        input_cost_usd=input_cost,
        output_cost_usd=output_cost,
        total_cost_usd=total_cost,
    )


# ---------------------------------------------------------------------------
# BASELINE-VS-OPTIMIZED SAVINGS
# ---------------------------------------------------------------------------


@dataclass
class SavingsResult:
    """
    The result of comparing an always-powerful baseline cost against the
    optimized (routed) cost for the same request(s).
    """

    baseline_cost_usd: float
    optimized_cost_usd: float
    savings_usd: float
    savings_percent: float  # 0-100; 0.0 if baseline_cost_usd is 0


def calculate_savings(baseline_cost_usd: float, optimized_cost_usd: float) -> SavingsResult:
    """
    Compare the "always use the powerful model" baseline cost against the
    optimized routing system's actual cost for the same request(s).

    Parameters
    ----------
    baseline_cost_usd: float
        What it would have cost if every request had gone to the powerful
        model tier (compute this by calling calculate_cost(..., tier=
        ModelTier.POWERFUL) for the same token counts).
    optimized_cost_usd: float
        What our routing system actually cost.

    Returns
    -------
    SavingsResult
        savings_usd = baseline_cost_usd - optimized_cost_usd (can be
        negative if the optimized path was somehow more expensive).
        savings_percent = savings_usd / baseline_cost_usd * 100, safely
        returned as 0.0 when baseline_cost_usd is 0 (nothing to save).
    """
    if baseline_cost_usd < 0 or optimized_cost_usd < 0:
        raise ValueError("Costs cannot be negative.")

    savings_usd = baseline_cost_usd - optimized_cost_usd

    if baseline_cost_usd == 0:
        savings_percent = 0.0
    else:
        savings_percent = (savings_usd / baseline_cost_usd) * 100.0

    return SavingsResult(
        baseline_cost_usd=baseline_cost_usd,
        optimized_cost_usd=optimized_cost_usd,
        savings_usd=savings_usd,
        savings_percent=savings_percent,
    )