"""
cache.py
========

This file implements a simple, in-memory cache that targets repeated
SYSTEM/CONTEXT prompt blocks specifically -- not whole question/answer
pairs.

WHY CACHE CONTEXT BLOCKS INSTEAD OF FULL ANSWERS:
Caching "have we seen this exact question before, and if so just replay
the old answer" would be wrong for this project: two different questions
that happen to share the same system/context block (e.g. the same long
set of instructions or reference document) still need their own real
answers. What's worth caching is recognizing "we've already seen this
context block before," since large repeated context is often the most
expensive part of a request in terms of tokens. This module only caches
and looks up CONTEXT BLOCKS -- never answers.

WHY THIS IS A SEPARATE FILE:
This module has no idea what a "request," a "model," or an "LLM response"
is -- it only knows about caching one string (a context block) under a
hash of itself. That keeps it trivially testable and reusable, and
matches the same pattern as llm_clients.py/cost.py: pure logic, no
FastAPI, no OpenAI SDK.

DESIGN NOTE -- IN-MEMORY NOW, REDIS-READY LATER:
The cache is stored in a single module-level dict, which is simple and
reliable for an MVP/demo but is lost when the process restarts and isn't
shared across multiple server processes. Every piece of cache logic is
routed through the three functions below (get_cached_context,
cache_context, clear_cache) rather than other files touching a dict
directly -- so swapping the dict for a real Redis client later only
requires changing the internals of this one file.

WHERE THIS FILE LIVES:
    LLMcostoptimizer/backend/cache.py
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass


# ---------------------------------------------------------------------------
# INTERNAL STATE
# ---------------------------------------------------------------------------
# _cache maps a hash of a context block -> the original context text.
# Using a hash (rather than the raw context string) as the dict key keeps
# lookups fast and constant-size regardless of how long the context block
# is, and matches the "use a hash of the context as the cache key"
# requirement directly.
_cache: dict[str, str] = {}

# Running counters for cache hit/miss statistics, used by get_cache_stats().
_hits: int = 0
_misses: int = 0


def _hash_context(context: str) -> str:
    """
    Compute a stable hash key for a context block.

    SHA-256 is used because it's a standard library option (via
    `hashlib`, no extra dependency) that reliably produces the same hash
    for the same input string -- which is exactly what we need for a
    cache key: identical context blocks must always map to the same key.
    """
    return hashlib.sha256(context.encode("utf-8")).hexdigest()


# ---------------------------------------------------------------------------
# PUBLIC API
# ---------------------------------------------------------------------------


def get_cached_context(context: str) -> str | None:
    """
    Look up a context block in the cache.

    Parameters
    ----------
    context: str
        The system/context prompt block to look up.

    Returns
    -------
    str | None
        The cached context text if this exact context block has been
        seen before (a cache hit), or None if it hasn't (a cache miss).
        This call also updates the hit/miss counters used by
        get_cache_stats().
    """
    global _hits, _misses

    key = _hash_context(context)
    cached_value = _cache.get(key)

    if cached_value is not None:
        _hits += 1
    else:
        _misses += 1

    return cached_value


def cache_context(context: str) -> str:
    """
    Store a context block in the cache, keyed by its hash.

    Parameters
    ----------
    context: str
        The system/context prompt block to store.

    Returns
    -------
    str
        The hash key the context was stored under, in case a caller
        wants to reference it directly (e.g. for logging/debugging).
    """
    key = _hash_context(context)
    _cache[key] = context
    return key


def clear_cache() -> None:
    """
    Remove all cached context blocks and reset the hit/miss counters.

    Resetting the counters alongside the cache (rather than only clearing
    entries) keeps this useful as a clean "reset to a fresh demo state"
    function -- calling it gives you both an empty cache and stats that
    start from zero again.
    """
    global _hits, _misses
    _cache.clear()
    _hits = 0
    _misses = 0


# ---------------------------------------------------------------------------
# STATISTICS
# ---------------------------------------------------------------------------


@dataclass
class CacheStats:
    """Hit/miss statistics for the context cache."""

    hits: int
    misses: int
    total_lookups: int
    hit_rate: float  # 0.0-1.0; 0.0 if there have been no lookups yet
    cached_entries: int  # how many distinct context blocks are stored


def get_cache_stats() -> CacheStats:
    """
    Return current cache hit/miss statistics.

    Returns
    -------
    CacheStats
        hits, misses, total_lookups, hit_rate (0.0 if no lookups have
        happened yet, to avoid a divide-by-zero), and how many distinct
        context blocks are currently stored in the cache.
    """
    total_lookups = _hits + _misses
    hit_rate = (_hits / total_lookups) if total_lookups > 0 else 0.0

    return CacheStats(
        hits=_hits,
        misses=_misses,
        total_lookups=total_lookups,
        hit_rate=hit_rate,
        cached_entries=len(_cache),
    )