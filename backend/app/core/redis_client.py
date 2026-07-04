import redis.asyncio as redis
import json
from typing import Optional, Any
from app.core.config import settings
from app.core.logging import logger

class RedisClient:
    def __init__(self):
        self._redis: Optional[redis.Redis] = None

    async def connect(self):
        """Connect to Redis."""
        try:
            self._redis = redis.from_url(
                settings.REDIS_URL,
                decode_responses=True,
            )
            await self._redis.ping()
            logger.info("Connected to Redis")
        except Exception as e:
            logger.error(f"Failed to connect to Redis: {e}")
            raise

    async def disconnect(self):
        """Disconnect from Redis."""
        if self._redis:
            await self._redis.close()
            logger.info("Disconnected from Redis")

    @property
    def client(self) -> redis.Redis:
        if not self._redis:
            raise RuntimeError("Redis client not connected. Call connect() first.")
        return self._redis

    async def get(self, key: str) -> Optional[str]:
        """Get value from Redis."""
        return await self.client.get(key)

    async def set(self, key: str, value: str, expire: Optional[int] = None):
        """Set value in Redis with optional expiration in seconds."""
        await self.client.set(key, value, ex=expire)

    async def delete(self, key: str):
        """Delete key from Redis."""
        await self.client.delete(key)

    async def exists(self, key: str) -> bool:
        """Check if key exists."""
        return await self.client.exists(key) > 0

    async def increment(self, key: str, amount: int = 1) -> int:
        """Increment a counter."""
        return await self.client.incrby(key, amount)

    async def expire(self, key: str, seconds: int):
        """Set expiration on a key."""
        await self.client.expire(key, seconds)

    async def zadd(self, key: str, mapping: dict):
        """Add to sorted set."""
        await self.client.zadd(key, mapping)

    async def zremrangebyscore(self, key: str, min_score: float, max_score: float):
        """Remove from sorted set by score."""
        await self.client.zremrangebyscore(key, min_score, max_score)

    async def zcard(self, key: str) -> int:
        """Get cardinality of sorted set."""
        return await self.client.zcard(key)

    async def zcount(self, key: str, min_score: float, max_score: float) -> int:
        """Count elements in sorted set by score range."""
        return await self.client.zcount(key, min_score, max_score)

    async def set_json(self, key: str, value: Any, expire: Optional[int] = None):
        """Store JSON-serializable data."""
        await self.client.set(key, json.dumps(value), ex=expire)

    async def get_json(self, key: str) -> Optional[Any]:
        """Get JSON-serializable data."""
        data = await self.client.get(key)
        return json.loads(data) if data else None

# Global Redis client instance
redis_client = RedisClient()

async def get_redis() -> RedisClient:
    """Get Redis client instance."""
    return redis_client
