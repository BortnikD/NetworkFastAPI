from abc import ABC, abstractmethod

from app.core.dto.pagination import PaginatedResponse
from app.core.entities.like import Like


class ILike(ABC):
    @abstractmethod
    async def save(self, post_id: int, current_user_id: int) -> Like:
        raise NotImplementedError

    @abstractmethod
    async def get_all_by_post_id(self, post_id: int, offset: int, limit: int) -> PaginatedResponse:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, like_id: int, current_user_id: int) -> None:
        raise NotImplementedError