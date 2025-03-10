from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models.like import Like
from app.adapters.api.schemas.pagination import PaginatedResponse
from app.adapters.repositories.like_repository import LikeRepository


class LikeService:
    def __init__(self, db: AsyncSession):
        self.like_repository = LikeRepository(db)

    async def create_like(self, post_id: int, current_user_id: int) -> Like:
        return await self.like_repository.create_like(post_id, current_user_id)

    async def get_likes_by_post_id(self, post_id: int, offset: int, limit: int) -> PaginatedResponse:
        return await self.like_repository.get_likes_by_post_id(post_id, offset, limit)

    async def delete_like(self, like_id: int, current_user_id: int):
        await self.like_repository.delete_like(like_id, current_user_id)