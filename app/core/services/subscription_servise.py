from fastapi import HTTPException

from app.core.dto.pagination import PaginatedResponse
from app.infrastructure.database.models import Subscription
from app.core.interfaces.subscription import ISubscription


class SubscriptionService:
    def __init__(self, subscription_port: ISubscription):
        self.subscription_port = subscription_port

    async def create_subscription(self, follower_id: int, followed_user_id: int) -> Subscription:
        if follower_id == followed_user_id:
            raise HTTPException(status_code=409, detail='You cannot subscribe to yourself')
        return await self.subscription_port.save(follower_id, followed_user_id)
    
    async def get_subscriptions_by_user_id(self, user_id: int, offset: int, limit: int) -> PaginatedResponse:
        return await self.subscription_port.get_subscriptions_by_user_id(user_id, offset, limit)
    
    async def delete_subscription_by_id(self, subscription_id: int, current_user_id: int) -> None:
        await self.subscription_port.delete(subscription_id, current_user_id)