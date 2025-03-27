from redis.asyncio import Redis

from app.infrastructure.settings.config import REDIS_URL


class RedisClient:
    _redis: Redis | None = None

    @classmethod
    def get_redis(cls) -> Redis:
        if cls._redis is None:
            cls._redis = Redis.from_url(REDIS_URL, decode_responses=True)
        return cls._redis

    @classmethod
    async def close(cls) -> None:
        if cls._redis:
            await cls._redis.close()
            cls._redis = None