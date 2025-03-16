from fastapi import Depends

from app.services.core_services.subscription_service import SubscriptionService
from app.infrastructure.database.repositories.subscription_repository import SubscriptionRepository
from app.dependencies.db import get_db


def get_subscription_service(db=Depends(get_db)) -> SubscriptionService:
    subscription = SubscriptionRepository(db)
    return SubscriptionService(subscription)