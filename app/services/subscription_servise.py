from sqlalchemy.ext.asyncio import AsyncEngine

from app.api.schemas.pagination import PaginatedResponse
from app.database.models import Subscription
from app.repositories.subscription_repository import SubscriptionRepository


class SubscriptionService:
    def __init__(self, db: AsyncEngine):
        self.subscription_repository = SubscriptionRepository(db)

    async def create_subscription(self, follower_id: int, followed_user_id: int) -> PaginatedResponse:
        return await self.subscription_repository.create_subscription(follower_id, followed_user_id)
    
    async def get_subscriptions_by_user_id(self, user_id: int, offset: int, limit: int) -> Subscription:
        return await self.subscription_repository.get_subscriptions_by_user_id(user_id, offset, limit)
    
    async def delete_subscription_by_id(self, subscription_id: int, current_user_id: int) -> None:
        await self.subscription_repository.delete_subscription_by_id(subscription_id, current_user_id)