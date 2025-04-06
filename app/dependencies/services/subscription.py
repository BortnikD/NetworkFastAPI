from fastapi import Depends

from app.dependencies.redis import get_redis
from app.services.core_services.subscription_service import SubscriptionService
from app.infrastructure.database.repositories.subscription_repository import SubscriptionRepository
from app.dependencies.db import get_db


async def get_subscription_service(db=Depends(get_db), cache=Depends(get_redis)) -> SubscriptionService:
    repository = SubscriptionRepository(db)
    return SubscriptionService(repository, cache)