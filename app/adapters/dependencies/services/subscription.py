from fastapi import Depends

from app.core.services.subscription_service import SubscriptionService
from app.adapters.repositories.subscription_repository import SubscriptionRepository
from app.adapters.dependencies.db import get_db


def get_subscription_service(db=Depends(get_db)) -> SubscriptionService:
    subscription = SubscriptionRepository(db)
    return SubscriptionService(subscription)