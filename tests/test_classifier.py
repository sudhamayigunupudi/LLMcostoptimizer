"""
test_classifier.py
===================

A minimal test suite for RuleBasedDifficultyClassifier.

WHY THESE TESTS:
The goal at this stage isn't exhaustive coverage -- it's to prove the
classifier behaves sensibly on one clearly-easy, one clearly-medium, and
one clearly-hard example, and that the ClassificationResult it returns is
well-formed (valid confidence range, non-empty explanation, etc.).

HOW TO RUN THIS:
From the `LLMcostoptimizer/` project root:
    pip install pytest
    PYTHONPATH=backend pytest tests/

(The PYTHONPATH=backend part is needed because classifier.py imports
`schemas` directly, e.g. `from schemas import ...`, matching the flat
backend/ layout FastAPI apps typically use. Setting PYTHONPATH lets Python
find backend/schemas.py and backend/classifier.py from the tests folder.)

WHERE THIS FILE LIVES:
    LLMcostoptimizer/tests/test_classifier.py
"""

import os
import sys

# Make sure `backend/` is importable even if PYTHONPATH wasn't set manually
# (e.g. when running tests directly from an IDE). This inserts the
# project's backend/ folder at the front of the import search path.
BACKEND_DIR = os.path.join(os.path.dirname(__file__), "..", "backend")
sys.path.insert(0, os.path.abspath(BACKEND_DIR))

from classifier import RuleBasedDifficultyClassifier  # noqa: E402
from schemas import DifficultyLevel  # noqa: E402


def test_easy_prompt_is_classified_easy():
    clf = RuleBasedDifficultyClassifier()
    result = clf.classify("What is the capital of France?")

    assert result.difficulty == DifficultyLevel.EASY
    assert 0.0 <= result.confidence <= 1.0
    assert result.explanation  # not empty
    assert result.features.has_code_keywords is False
    assert result.features.has_reasoning_keywords is False


def test_coding_prompt_is_classified_medium_or_harder():
    clf = RuleBasedDifficultyClassifier()
    result = clf.classify(
        "Write a Python function that reverses a string and explain why it works."
    )

    # Should be at least medium: it has both code keywords and a reasoning
    # keyword ("explain why"), which together should push it past 'easy'.
    assert result.difficulty in (DifficultyLevel.MEDIUM, DifficultyLevel.HARD)
    assert result.features.has_code_keywords is True
    assert result.features.has_reasoning_keywords is True


def test_long_multistep_reasoning_prompt_is_classified_hard():
    clf = RuleBasedDifficultyClassifier()
    long_prompt = (
        "First, analyze the trade-offs between microservices and a monolith "
        "for a high-traffic e-commerce platform. Then, design a step by step "
        "migration strategy, explain the root cause of common migration "
        "failures, and finally propose an architecture diagram. "
        "Step 1: assess current bottlenecks. Step 2: evaluate database "
        "sharding options. Step 3: outline a rollback plan in case of "
        "failure during the cutover window, including monitoring and "
        "on-call procedures for the engineering team."
    )
    result = clf.classify(long_prompt)

    assert result.difficulty == DifficultyLevel.HARD
    assert result.features.has_multistep_markers is True
    assert result.features.has_reasoning_keywords is True
    assert result.features.prompt_length_words >= 40


def test_confidence_increases_with_more_signals():
    clf = RuleBasedDifficultyClassifier()
    easy = clf.classify("Hi there")
    hard = clf.classify(
        "First, debug this Python stack trace, then explain the root cause, "
        "and finally refactor the function step by step."
    )

    assert hard.confidence > easy.confidence
