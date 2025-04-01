from abc import ABC, abstractmethod

from app.domain.entities.subscription import Subscription
from app.domain.dto.pagination import PaginatedResponse


class ISubscription(ABC):
    @abstractmethod
    async def save(self, current_user_id: int, followed_user_id: int) -> Subscription:
        raise NotImplementedError

    @abstractmethod
    async def get_subscriptions_by_user_id(self, current_user_id: int, offset: int, limit: int) -> PaginatedResponse:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, subscription_id: int, current_user_id: int) -> None:
        raise NotImplementedError
