"""
classifier.py
==============

This file implements the FIRST version of the "request difficulty
classifier" required by the hackathon spec.

WHY START WITH A RULE-BASED CLASSIFIER INSTEAD OF AN ML MODEL:
The spec explicitly asks for a "transparent baseline classifier" first,
with the ability to swap in a trained ML/LLM classifier later. A rule-based
classifier is:
  - fast to build and needs no training data,
  - fully explainable (you can point at exactly which rule fired),
  - easy to demo to judges ("look, it flagged this because it detected
    coding keywords and a long prompt").

HOW SWAPPING IN A REAL MODEL LATER WILL WORK:
Every classifier in this system just needs one method:
    classify(prompt: str) -> ClassificationResult
Because main.py / router.py (built later) will only ever call
`classify()` and use the returned ClassificationResult, we can later write
a second class (e.g. MLDifficultyClassifier) with the same method
signature and swap it in without changing any other file.

WHERE THIS FILE LIVES:
    LLMcostoptimizer/backend/classifier.py
"""

from __future__ import annotations

import re

from schemas import ClassificationFeatures, ClassificationResult, DifficultyLevel

# ---------------------------------------------------------------------------
# CONFIGURATION: keyword lists and scoring weights
# ---------------------------------------------------------------------------
# Keeping these as named constants at the top (instead of "magic numbers"
# buried inside the logic) makes the classifier easy to tune and easy to
# explain in a demo.

# Words that suggest the request involves writing/debugging code.
CODE_KEYWORDS = [
    "code", "function", "class", "python", "javascript", "bug", "debug",
    "compile", "algorithm", "refactor", "unit test", "api", "sql",
    "regex", "stack trace", "exception", "script",
]

# Words that suggest the request needs deeper reasoning/analysis rather
# than a quick factual lookup.
REASONING_KEYWORDS = [
    "why", "explain", "analyze", "compare", "evaluate", "reason",
    "prove", "derive", "trade-off", "tradeoff", "optimi", "design",
    "architecture", "strategy", "root cause",
]

# Phrases that suggest the request has multiple sub-tasks / steps chained
# together, which tends to make a prompt harder to answer well in one shot.
MULTISTEP_MARKERS = [
    "step 1", "step by step", "first", "then", "after that",
    "and then", "finally", "1.", "2.", "3.",
]

# --- Scoring weights ---
# Each signal below adds a fixed amount to a running "raw_score". The
# thresholds after that decide the final easy/medium/hard bucket.
WEIGHT_LONG_PROMPT = 1.0        # added if the prompt is long
WEIGHT_VERY_LONG_PROMPT = 1.0   # added on top if the prompt is very long
WEIGHT_CODE_KEYWORDS = 1.5
WEIGHT_REASONING_KEYWORDS = 1.0
WEIGHT_MULTISTEP_MARKERS = 1.5

# Length thresholds, measured in words, for the "long prompt" signals above.
LONG_PROMPT_WORD_THRESHOLD = 40
VERY_LONG_PROMPT_WORD_THRESHOLD = 120

# Final score cutoffs that decide the difficulty bucket.
# raw_score < MEDIUM_CUTOFF        -> easy
# MEDIUM_CUTOFF <= score < HARD_CUTOFF -> medium
# raw_score >= HARD_CUTOFF          -> hard
MEDIUM_CUTOFF = 1.5
HARD_CUTOFF = 3.0

# Max possible raw_score, used only to normalize the score into a 0-1
# confidence value. Recompute this if you change the weights above.
MAX_POSSIBLE_SCORE = (
    WEIGHT_LONG_PROMPT
    + WEIGHT_VERY_LONG_PROMPT
    + WEIGHT_CODE_KEYWORDS
    + WEIGHT_REASONING_KEYWORDS
    + WEIGHT_MULTISTEP_MARKERS
)


class RuleBasedDifficultyClassifier:
    """
    A transparent, rule-based implementation of the difficulty classifier.

    Usage:
        clf = RuleBasedDifficultyClassifier()
        result = clf.classify("Write a Python function that reverses a string")
        print(result.difficulty)     # DifficultyLevel.MEDIUM (for example)
        print(result.explanation)    # human-readable reason
    """

    def classify(self, prompt: str) -> ClassificationResult:
        """
        Classify a single prompt's difficulty.

        Parameters
        ----------
        prompt: str
            The raw text of the user's request.

        Returns
        -------
        ClassificationResult
            difficulty + confidence + explanation + the raw features used.
        """
        # Work on a lowercased copy for keyword matching, but keep the
        # original around for accurate length counts.
        lowered = prompt.lower()

        word_count = len(prompt.split())
        char_count = len(prompt)

        has_code = self._contains_any(lowered, CODE_KEYWORDS)
        has_reasoning = self._contains_any(lowered, REASONING_KEYWORDS)
        has_multistep = self._contains_any(lowered, MULTISTEP_MARKERS)

        # --- Build up the raw score from each signal ---
        raw_score = 0.0
        fired_reasons: list[str] = []

        if word_count >= LONG_PROMPT_WORD_THRESHOLD:
            raw_score += WEIGHT_LONG_PROMPT
            fired_reasons.append(
                f"prompt is long ({word_count} words >= {LONG_PROMPT_WORD_THRESHOLD})"
            )
        if word_count >= VERY_LONG_PROMPT_WORD_THRESHOLD:
            raw_score += WEIGHT_VERY_LONG_PROMPT
            fired_reasons.append(
                f"prompt is very long ({word_count} words >= {VERY_LONG_PROMPT_WORD_THRESHOLD})"
            )
        if has_code:
            raw_score += WEIGHT_CODE_KEYWORDS
            fired_reasons.append("coding-related keywords detected")
        if has_reasoning:
            raw_score += WEIGHT_REASONING_KEYWORDS
            fired_reasons.append("reasoning/analysis keywords detected")
        if has_multistep:
            raw_score += WEIGHT_MULTISTEP_MARKERS
            fired_reasons.append("multi-step structure detected")

        difficulty = self._bucket_score(raw_score)
        confidence = self._score_to_confidence(raw_score)

        if fired_reasons:
            explanation = (
                f"Classified as '{difficulty.value}' because: "
                + "; ".join(fired_reasons)
                + "."
            )
        else:
            explanation = (
                f"Classified as '{difficulty.value}': prompt is short and "
                "contains no coding, reasoning, or multi-step signals."
            )

        features = ClassificationFeatures(
            prompt_length_chars=char_count,
            prompt_length_words=word_count,
            has_code_keywords=has_code,
            has_reasoning_keywords=has_reasoning,
            has_multistep_markers=has_multistep,
            raw_score=raw_score,
        )

        return ClassificationResult(
            difficulty=difficulty,
            confidence=confidence,
            explanation=explanation,
            features=features,
        )

    # -----------------------------------------------------------------
    # Internal helpers
    # -----------------------------------------------------------------

    @staticmethod
    def _contains_any(lowered_text: str, keywords: list[str]) -> bool:
        """
        Return True if any keyword/phrase appears in lowered_text as a
        whole word (or whole phrase), not just as a substring.

        WHY NOT A SIMPLE `keyword in lowered_text` CHECK:
        Plain substring matching has a nasty bug: the keyword "api" is
        also a substring of ordinary words like "capital" (c-API-tal).
        That would wrongly flag "What is the capital of France?" as a
        coding question. Wrapping each keyword in \\b (a "word boundary"
        regex marker) makes sure it only matches when "api" appears as
        its own word, not buried inside another word.
        """
        for keyword in keywords:
            cleaned = keyword.strip()
            # \b only makes sense next to a "word" character (letters,
            # digits, underscore). For a keyword like "1." the trailing
            # character is a period, not a word character, so we skip the
            # trailing \b in that case -- otherwise the regex could never
            # match (a boundary can't exist between two non-word chars).
            prefix = r"\b" if cleaned[0].isalnum() else ""
            suffix = r"\b" if cleaned[-1].isalnum() else ""
            pattern = prefix + re.escape(cleaned) + suffix
            if re.search(pattern, lowered_text):
                return True
        return False

    @staticmethod
    def _bucket_score(raw_score: float) -> DifficultyLevel:
        """Turn a numeric raw_score into a DifficultyLevel bucket."""
        if raw_score >= HARD_CUTOFF:
            return DifficultyLevel.HARD
        if raw_score >= MEDIUM_CUTOFF:
            return DifficultyLevel.MEDIUM
        return DifficultyLevel.EASY

    @staticmethod
    def _score_to_confidence(raw_score: float) -> float:
        """
        Convert the raw_score into a 0.0-1.0 confidence value.

        This is a simple normalization against the maximum possible score,
        clamped to [0, 1]. It's a placeholder for "how confident are we in
        this bucket" -- a more sophisticated classifier (e.g. an ML model)
        would replace this with a real predicted-probability value.
        """
        confidence = raw_score / MAX_POSSIBLE_SCORE
        return max(0.0, min(1.0, confidence))
