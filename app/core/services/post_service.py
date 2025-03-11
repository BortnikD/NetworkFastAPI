from app.core.dto.post import PostCreate, PostUpdate
from app.core.dto.pagination import PaginatedResponse
from app.core.interfaces.post import IPost
from app.infrastructure.database.models.post import Post


class PostService:
    def __init__(self, post_port: IPost):
        self.post_port = post_port

    async def get_all_posts(self, offset: int, limit: int) -> PaginatedResponse:
        return await self.post_port.get_all_posts(offset, limit)
    
    async def get_post(self, post_id: int) -> Post:
        return await self.post_port.get_post(post_id)

    async def save(self, post: PostCreate) -> Post:
        return await self.post_port.save(post)
    
    async def delete(self, post_id: int, user_id: int) -> None:
        await self.post_port.delete(post_id, user_id)
    
    async def update(self, post: PostUpdate, user_id: int) -> Post:
        return await self.post_port.update(post, user_id)
