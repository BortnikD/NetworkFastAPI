from app.infrastructure.database.models.like import Like
from app.core.dto.pagination import PaginatedResponse
from app.core.interfaces.like import ILike


class LikeService:
    def __init__(self, like_port: ILike):
        self.like_port = like_port

    async def create_like(self, post_id: int, current_user_id: int) -> Like:
        return await self.like_port.save(post_id, current_user_id)

    async def get_likes_by_post_id(self, post_id: int, offset: int, limit: int) -> PaginatedResponse:
        return await self.like_port.get_all_by_post_id(post_id, offset, limit)

    async def delete_like(self, like_id: int, current_user_id: int):
        await self.like_port.delete(like_id, current_user_id)