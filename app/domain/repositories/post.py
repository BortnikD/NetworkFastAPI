from abc import ABC, abstractmethod

from app.domain.dto.pagination import PaginatedResponse
from app.domain.entities import Post
from app.domain.dto.post import PostCreate, PostUpdate


class IPost(ABC):
    @abstractmethod
    async def save(self, post: PostCreate) -> Post:
        raise NotImplementedError

    @abstractmethod
    async def get_all_posts(self, offset: int, limit: int) -> PaginatedResponse:
        raise NotImplementedError

    @abstractmethod
    async def get_post(self, post_id: int) -> Post:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, post_id: int, current_user_id: int) -> None:
        raise NotImplementedError

    @abstractmethod
    async def update(self, post: PostUpdate, current_user_id: int) -> Post:
        raise NotImplementedError