"""
schemas.py
==========

This file defines the "data contracts" for the whole backend using Pydantic.

WHAT IS PYDANTIC, BRIEFLY:
Pydantic lets you define a Python class where each attribute has a declared
type (str, int, float, etc). When you create an instance of that class,
Pydantic automatically checks the data matches those types, and raises a
clear error if it doesn't. FastAPI uses these same classes to:
  1) validate incoming JSON request bodies,
  2) auto-generate API docs,
  3) serialize outgoing responses back to JSON.

So defining these models now means every other file (classifier, router,
main, etc.) can import them and know exactly what shape of data to expect,
instead of passing around loosely-structured dicts.

WHERE THIS FILE LIVES:
    LLMcostoptimizer/backend/schemas.py
"""

from __future__ import annotations

from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# ENUMS
# ---------------------------------------------------------------------------
# An Enum (enumeration) is a fixed, named set of allowed values. Using one
# here instead of a plain string means:
#   - no typos like "esay" or "Hard" vs "hard" slipping through the code,
#   - editors/IDEs can autocomplete the valid options,
#   - FastAPI will show the exact allowed values in the auto-generated docs.


class DifficultyLevel(str, Enum):
    """How hard the classifier thinks a request is to answer well."""

    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"


class ModelTier(str, Enum):
    """
    Which model tier a request should be routed to.

    Only two tiers for now (per the hackathon requirements): a cheap model
    and a powerful model. The router (built in a later step) will decide
    which tier a given DifficultyLevel maps to.
    """

    CHEAP = "cheap"
    POWERFUL = "powerful"


# ---------------------------------------------------------------------------
# CLASSIFIER SCHEMAS
# ---------------------------------------------------------------------------


class ClassificationFeatures(BaseModel):
    """
    The raw, individual signals the classifier measured about a prompt.

    Keeping these as separate named fields (instead of just a final score)
    is what makes the classifier "transparent" -- anyone (including a
    hackathon judge) can look at this object and see exactly *why* a prompt
    was scored the way it was, rather than trusting a black box.
    """

    prompt_length_chars: int = Field(
        ..., description="Total number of characters in the prompt."
    )
    prompt_length_words: int = Field(
        ..., description="Total number of words in the prompt."
    )
    has_code_keywords: bool = Field(
        ..., description="Whether coding-related keywords were detected."
    )
    has_reasoning_keywords: bool = Field(
        ...,
        description="Whether multi-step reasoning / analysis keywords were detected.",
    )
    has_multistep_markers: bool = Field(
        ...,
        description=(
            "Whether the prompt looks like it asks for multiple steps or "
            "sub-tasks (e.g. numbered lists, 'and then', 'first ... then')."
        ),
    )
    raw_score: float = Field(
        ..., description="The weighted numeric score before it was bucketed into a DifficultyLevel."
    )


class ClassificationResult(BaseModel):
    """
    What the classifier returns for a single prompt.

    difficulty  -> the final bucketed label (easy/medium/hard)
    confidence  -> how confident the classifier is in that label, from 0.0 to 1.0
    explanation -> a short, human-readable reason (for demoing to judges)
    features    -> the raw ClassificationFeatures used to reach the decision
    """

    difficulty: DifficultyLevel
    confidence: float = Field(..., ge=0.0, le=1.0)
    explanation: str
    features: ClassificationFeatures


# ---------------------------------------------------------------------------
# FUTURE /optimize ENDPOINT SCHEMAS (stubbed now, wired up in a later step)
# ---------------------------------------------------------------------------
# These are declared now because classifier.py's output will eventually
# feed into these, but the router/cache/cost logic behind them is NOT
# implemented yet -- that happens in router.py, cache.py, and cost.py,
# which we are intentionally holding off on per your instructions.


class OptimizeRequest(BaseModel):
    """The body a client sends to POST /optimize."""

    prompt: str = Field(..., description="The user's LLM request/prompt.")
    system_context: Optional[str] = Field(
        default=None,
        description=(
            "Optional repeated system/context block (e.g. a system prompt). "
            "This is what the cache (built later) will target."
        ),
    )


class OptimizeResponse(BaseModel):
    """
    The body returned from POST /optimize.

    Several fields are Optional right now because the components that
    populate them (router, cache, cost tracker) don't exist yet. They will
    be filled in as those pieces are built in later steps.
    """

    classification: ClassificationResult
    selected_model_tier: Optional[ModelTier] = None
    cache_hit: Optional[bool] = None
    input_tokens: Optional[int] = None
    output_tokens: Optional[int] = None
    estimated_cost_usd: Optional[float] = None
    answer: Optional[str] = None
