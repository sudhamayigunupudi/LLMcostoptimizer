"""
router.py
=========

This file implements the ROUTING step of the pipeline: given a difficulty
level (already produced by classifier.py), decide which model tier
(cheap or powerful) should handle the request, and explain why.

WHY THIS IS A SEPARATE FILE FROM classifier.py AND main.py:
  - classifier.py only answers "how hard is this prompt?" -- it knows
    nothing about models or cost.
  - router.py only answers "given that difficulty, which model tier
    should we use?" -- it knows nothing about FastAPI, HTTP, or how to
    actually call an LLM API.
  - main.py (built later) will just glue these together: call the
    classifier, pass its result into the router, then hand the chosen
    tier off to llm_clients.py to make the real API call.

Keeping router.py independent of FastAPI and of llm_clients.py like this
means:
  1) it's trivial to unit test (pure function in, pure object out, no
     network calls or web framework needed),
  2) the mapping rules can be changed/tuned in one place without touching
     any other file,
  3) main.py never contains hard-coded "if difficulty == ... then model
     tier == ..." logic itself -- it just calls `route_request(...)`.

WHERE THIS FILE LIVES:
    LLMcostoptimizer/backend/router.py
"""

from __future__ import annotations

from dataclasses import dataclass

from schemas import DifficultyLevel, ModelTier

# ---------------------------------------------------------------------------
# CONFIGURATION
# ---------------------------------------------------------------------------
# This is the "configurable threshold" the spec asks for: it controls what
# tier a MEDIUM-difficulty request goes to by default. Easy always goes to
# cheap, hard always goes to powerful -- medium is the one tunable case.
#
# Changing this one constant (instead of editing an if/else somewhere)
# changes the routing behavior for every medium-difficulty request.
DEFAULT_MEDIUM_TIER: ModelTier = ModelTier.CHEAP

# The core routing table: difficulty -> model tier. Using a dict here
# (instead of a chain of if/elif statements) is what the spec means by
# "do NOT hard-code this logic in main.py" -- the mapping lives in data,
# in this one file, and is easy to read at a glance or change later.
_ROUTING_TABLE: dict[DifficultyLevel, ModelTier] = {
    DifficultyLevel.EASY: ModelTier.CHEAP,
    DifficultyLevel.MEDIUM: DEFAULT_MEDIUM_TIER,
    DifficultyLevel.HARD: ModelTier.POWERFUL,
}


@dataclass
class RoutingDecision:
    """
    The result of routing a single request.

    A plain @dataclass (rather than a Pydantic BaseModel) is used here on
    purpose: this object never crosses an HTTP boundary by itself (it's an
    internal hand-off between router.py and whatever calls it, e.g. main.py
    or a future evaluator.py), so it doesn't need Pydantic's JSON
    validation/serialization machinery. If a later step needs to return
    this over the API directly, it can be wrapped in a Pydantic schema in
    schemas.py at that point.
    """

    model_tier: ModelTier
    reason: str


def route_request(
    difficulty: DifficultyLevel,
    medium_tier: ModelTier = DEFAULT_MEDIUM_TIER,
) -> RoutingDecision:
    """
    Decide which model tier a request should be routed to.

    Parameters
    ----------
    difficulty: DifficultyLevel
        The difficulty bucket produced by the classifier (easy/medium/hard).
    medium_tier: ModelTier, optional
        Which tier MEDIUM-difficulty requests should go to. Defaults to
        DEFAULT_MEDIUM_TIER (cheap). Exposed as a parameter -- rather than
        only a module-level constant -- so callers (e.g. an evaluator
        comparing different routing strategies) can experiment with
        sending medium requests to the powerful tier instead, without
        editing this file.

    Returns
    -------
    RoutingDecision
        The selected model tier plus a short, human-readable reason.
    """
    if difficulty == DifficultyLevel.EASY:
        return RoutingDecision(
            model_tier=ModelTier.CHEAP,
            reason="Easy requests always route to the cheap model.",
        )

    if difficulty == DifficultyLevel.HARD:
        return RoutingDecision(
            model_tier=ModelTier.POWERFUL,
            reason="Hard requests always route to the powerful model.",
        )

    if difficulty == DifficultyLevel.MEDIUM:
        if medium_tier == ModelTier.POWERFUL:
            reason = (
                "Medium requests are configured to route to the powerful "
                "model (medium_tier=powerful)."
            )
        else:
            reason = (
                "Medium requests default to the cheap model "
                "(medium_tier=cheap)."
            )
        return RoutingDecision(model_tier=medium_tier, reason=reason)

    # This should be unreachable as long as DifficultyLevel only has the
    # three members above, but it's here so the function fails loudly and
    # clearly instead of silently returning something wrong if a new
    # difficulty level is ever added without updating this file.
    raise ValueError(f"Unhandled difficulty level: {difficulty!r}")
