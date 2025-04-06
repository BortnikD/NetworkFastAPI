from app.infrastructure.database.redis import RedisClient
from app.infrastructure.database.repositories.redis_repository import RedisRepository


async def get_redis() -> RedisRepository:
    client = RedisClient()
    redis = await client.get_redis()
    return RedisRepository(redis)