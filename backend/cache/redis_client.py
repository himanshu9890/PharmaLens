import hashlib
import json
import logging
from typing import Any

import redis.asyncio as aioredis

from backend.config import settings

logger = logging.getLogger(__name__)

_redis: aioredis.Redis | None = None


async def get_redis() -> aioredis.Redis:
    global _redis
    if _redis is None:
        _redis = aioredis.from_url(settings.redis_url, decode_responses=True)
    return _redis


async def close_redis() -> None:
    global _redis
    if _redis is not None:
        await _redis.aclose()
        _redis = None


def make_cache_key(prefix: str, params: dict) -> str:
    """Deterministic cache key from a prefix and a dict of params."""
    canonical = json.dumps(params, sort_keys=True, default=str)
    digest = hashlib.sha256(canonical.encode()).hexdigest()[:16]
    return f"pharmalens:{prefix}:{digest}"


async def cache_get(key: str) -> Any | None:
    try:
        r = await get_redis()
        value = await r.get(key)
        if value:
            return json.loads(value)
    except Exception as exc:
        logger.warning("Redis cache_get failed for key %s: %s", key, exc)
    return None


async def cache_set(key: str, value: Any, ttl: int = settings.cache_ttl_seconds) -> None:
    try:
        r = await get_redis()
        await r.set(key, json.dumps(value, default=str), ex=ttl)
    except Exception as exc:
        logger.warning("Redis cache_set failed for key %s: %s", key, exc)
