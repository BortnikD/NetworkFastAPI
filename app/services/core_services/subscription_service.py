from app.domain.dto.pagination import PaginatedResponse
from app.domain.entities.subscription import Subscription
from app.domain.repositories.redis import IRedis
from app.domain.repositories.subscription import ISubscription
from app.domain.exceptions.subscription import SelfSubscriptionError


class SubscriptionService:
    def __init__(self,
                 subscription_port: ISubscription,
                 cache_port: IRedis
                 ):
        self.subscription_port = subscription_port
        self.cache_port = cache_port
        self.cache_path = "cache.subscriptions"

    async def save(self, follower_id: int, followed_user_id: int) -> Subscription:
        if follower_id == followed_user_id:
            raise SelfSubscriptionError('You cannot subscribe to yourself')
        result =  await self.subscription_port.save(follower_id, followed_user_id)
        await self.cache_port.clear_cache(f'{self.cache_path}:{follower_id}:*')
        await self.cache_port.clear_cache(f'{self.cache_path}:{followed_user_id}:*')
        return result

    async def get_subscriptions_by_user_id(self, user_id: int, offset: int, limit: int) -> PaginatedResponse:
        cache_key = f'{self.cache_path}:{user_id}:{offset}:{limit}'
        subscriptions = await self.cache_port.get_cache(cache_key)
        if subscriptions:
            return PaginatedResponse(**subscriptions)
        subscriptions = await self.subscription_port.get_subscriptions_by_user_id(user_id, offset, limit)
        await self.cache_port.set_cache(cache_key, subscriptions)
        return subscriptions

    async def delete(self, subscription_id: int, current_user_id: int) -> None:
        await self.subscription_port.delete(subscription_id, current_user_id)
        await self.cache_port.clear_cache(f'{self.cache_path}:{current_user_id}:*')
