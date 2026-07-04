import hashlib
import json
from typing import Optional
from app.core.redis_client import redis_client
from app.core.logging import logger

def _get_cache_key(prompt: str, mode: str, **kwargs) -> str:
    content = f"{prompt.strip().lower()}|{mode}|{json.dumps(kwargs, sort_keys=True)}"
    hash_value = hashlib.sha256(content.encode()).hexdigest()[:16]
    return f"llm_cache:{hash_value}"

async def get_cached_response(prompt: str, mode: str, **kwargs) -> Optional[str]:
    try:
        cache_key = _get_cache_key(prompt, mode, **kwargs)
        cached = await redis_client.get(cache_key)
        if cached:
            logger.info(f"Cache hit for key: {cache_key}")
            return cached
        return None
    except Exception as e:
        logger.warning(f"Cache read error: {e}")
        return None

async def set_cached_response(prompt: str, mode: str, response: str, **kwargs):
    try:
        cache_key = _get_cache_key(prompt, mode, **kwargs)
        # Cache for 1 hour
        await redis_client.set(cache_key, response, expire=3600)
        logger.info(f"Cache set for key: {cache_key}")
    except Exception as e:
        logger.warning(f"Cache write error: {e}")
