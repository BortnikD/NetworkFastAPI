from fastapi import Depends

from app.infrastructure.database.redis import RedisClient
from app.services.core_services.subscription_service import SubscriptionService
from app.infrastructure.database.repositories.subscription_repository import SubscriptionRepository
from app.infrastructure.database.repositories.redis_repository import RedisRepository
from app.dependencies.db import get_db


async def get_subscription_service(db=Depends(get_db)) -> SubscriptionService:
    subscription = SubscriptionRepository(db)
    client = RedisClient()
    redis = await client.get_redis()
    redis_repo = RedisRepository(redis)
    return SubscriptionService(subscription, redis_repo)