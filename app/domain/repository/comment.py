from abc import ABC, abstractmethod

from app.domain.dto.pagination import PaginatedResponse
from app.domain.repository.entities.comment import Comment
from app.domain.dto.comment import CommentCreate, CommentUpdate


class IComment(ABC):
    @abstractmethod
    async def save(self, comment: CommentCreate, current_user_id: int) -> Comment:
        raise NotImplementedError

    @abstractmethod
    async def get_all_by_post_id(self, post_id: int, offset: int, limit: int) -> PaginatedResponse:
        raise NotImplementedError

    @abstractmethod
    async def update(self, comment: CommentUpdate, current_user_id: int) -> Comment:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, comment_id: int, current_user_id: int) -> None:
        raise NotImplementedError