"""
llm_clients.py
===============

This file is the ONLY place in the backend that talks to an external LLM
provider (OpenAI, for now). Its job is to hide away the details of the
OpenAI SDK behind one simple function:

    generate_response(prompt, tier) -> LLMResponse

WHY THIS MODULE IS KEPT SEPARATE FROM classifier.py AND router.py:
  - classifier.py decides "how hard is this?" -- no network calls.
  - router.py decides "which tier should handle it?" -- no network calls.
  - llm_clients.py is the only file that actually calls out to an LLM API.
This means classifier.py and router.py can be unit tested instantly with
no API key and no network access, and if we ever swap providers (e.g. add
Anthropic or a local model), we only need to change this one file -- the
rest of the pipeline (main.py, router.py) keeps working unmodified because
they only depend on the ModelTier enum and this module's public function.

CONFIGURATION (all read from environment variables, never hard-coded):
    OPENAI_API_KEY   -> your OpenAI API key
    CHEAP_MODEL       -> the model name to use for ModelTier.CHEAP
    POWERFUL_MODEL    -> the model name to use for ModelTier.POWERFUL

These are typically set via a `.env` file at the project root (loaded with
python-dotenv) and MUST NOT be committed to version control.

WHERE THIS FILE LIVES:
    LLMcostoptimizer/backend/llm_clients.py
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Optional

from dotenv import load_dotenv
from openai import OpenAI, OpenAIError

from schemas import ModelTier

# Load variables from a .env file (if present) into the process
# environment. This is a no-op if no .env file exists, which keeps this
# module safe to import in any environment (including tests/CI) as long
# as the required env vars are set some other way when actually calling
# generate_response().
load_dotenv()


# ---------------------------------------------------------------------------
# CONFIGURATION: model names per tier, read from environment variables
# ---------------------------------------------------------------------------
# Fallback defaults are provided so the module can be imported (and its
# non-network parts tested) even without a .env file. The *_MODEL env vars
# should be set explicitly for real runs/demos.
CHEAP_MODEL: str = os.environ.get("CHEAP_MODEL", "gpt-4o-mini")
POWERFUL_MODEL: str = os.environ.get("POWERFUL_MODEL", "gpt-4o")

# Maps each ModelTier to the concrete model name that should be called.
# Keeping this as a small dict (data), rather than scattering
# `if tier == ModelTier.CHEAP: model = "..."` checks throughout the code,
# is what makes it easy to add a third tier later without touching the
# calling code in generate_response().
_TIER_TO_MODEL_NAME: dict[ModelTier, str] = {
    ModelTier.CHEAP: CHEAP_MODEL,
    ModelTier.POWERFUL: POWERFUL_MODEL,
}


# ---------------------------------------------------------------------------
# DATA CLASSES for the response this module returns
# ---------------------------------------------------------------------------


@dataclass
class UsageInfo:
    """
    Token usage reported by the LLM provider for a single call.

    This is what cost.py (built in a later step) will use to calculate
    the actual dollar cost of a request -- so it's important these numbers
    come directly from the API response rather than being estimated.
    """

    prompt_tokens: int
    completion_tokens: int
    total_tokens: int


@dataclass
class LLMResponse:
    """The result of a single call to generate_response()."""

    text: str
    model_tier: ModelTier
    model_name: str
    usage: Optional[UsageInfo]  # None if the provider didn't report usage


class LLMClientError(Exception):
    """
    Raised whenever a call to the LLM provider fails for any reason
    (network issue, bad API key, rate limit, invalid model name, etc).

    Wrapping every possible OpenAI SDK exception in this one custom
    exception type means calling code (main.py, evaluator.py, etc.) only
    ever needs to handle ONE exception type from this module, instead of
    needing to know about every specific OpenAI error class.
    """


# ---------------------------------------------------------------------------
# INTERNAL: lazily-created OpenAI client
# ---------------------------------------------------------------------------
# The client is created lazily (on first use, cached in _client) rather
# than at import time. This has two benefits:
#   1) importing this module never fails just because OPENAI_API_KEY isn't
#      set yet (useful in tests that only check the tier/model mapping),
#   2) the API key is read fresh from the environment at call time.
_client: Optional[OpenAI] = None


def _get_client() -> OpenAI:
    """Return a cached OpenAI client, creating it on first use."""
    global _client
    if _client is None:
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            # Deliberately do not include the key itself anywhere here --
            # there is nothing to leak since it's simply missing, but we
            # keep the message generic on principle.
            raise LLMClientError(
                "OPENAI_API_KEY is not set. Add it to your .env file."
            )
        # The SDK reads the key we pass explicitly; we never print or log
        # `api_key` anywhere in this module.
        _client = OpenAI(api_key=api_key)
    return _client


# ---------------------------------------------------------------------------
# PUBLIC API
# ---------------------------------------------------------------------------


def generate_response(prompt: str, tier: ModelTier) -> LLMResponse:
    """
    Send `prompt` to the model configured for `tier` and return the result.

    Parameters
    ----------
    prompt: str
        The text to send to the model.
    tier: ModelTier
        Which configured model tier to use (ModelTier.CHEAP or
        ModelTier.POWERFUL). The concrete model name for each tier comes
        from the CHEAP_MODEL / POWERFUL_MODEL environment variables.

    Returns
    -------
    LLMResponse
        The generated text, which tier/model were used, and token usage
        info if the provider reported it.

    Raises
    ------
    LLMClientError
        If the API key is missing, the model name is misconfigured, or
        the request fails for any other reason (network error, rate
        limit, invalid request, etc). The original error is chained via
        `raise ... from exc` for debugging, but never exposes the API key.
    """
    model_name = _TIER_TO_MODEL_NAME.get(tier)
    if not model_name:
        raise LLMClientError(f"No model configured for tier: {tier!r}")

    client = _get_client()

    try:
        completion = client.chat.completions.create(
            model=model_name,
            messages=[{"role": "user", "content": prompt}],
        )
    except OpenAIError as exc:
        # Catch every OpenAI SDK error (auth, rate limit, bad request,
        # connection issues, etc) and re-raise as our own error type so
        # callers only need to catch LLMClientError. str(exc) from the
        # OpenAI SDK does not include the API key, so this stays safe to
        # log/display.
        raise LLMClientError(
            f"OpenAI API call failed for tier '{tier.value}' "
            f"(model='{model_name}'): {exc}"
        ) from exc
    except Exception as exc:  # noqa: BLE001 - final safety net
        # Catches anything unexpected (e.g. a network layer error not
        # covered by OpenAIError) so a single bad request never crashes
        # the whole request pipeline.
        raise LLMClientError(
            f"Unexpected error calling model tier '{tier.value}' "
            f"(model='{model_name}'): {exc}"
        ) from exc

    text = completion.choices[0].message.content or ""

    usage: Optional[UsageInfo] = None
    if completion.usage is not None:
        usage = UsageInfo(
            prompt_tokens=completion.usage.prompt_tokens,
            completion_tokens=completion.usage.completion_tokens,
            total_tokens=completion.usage.total_tokens,
        )

    return LLMResponse(
        text=text,
        model_tier=tier,
        model_name=model_name,
        usage=usage,
    )