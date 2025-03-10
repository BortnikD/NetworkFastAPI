from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.database.models.post import Post
from app.adapters.api.schemas.post import PostCreate, PostUpdate
from app.adapters.api.schemas.pagination import PaginatedResponse
from app.adapters.repositories.post_repository import PostRepository


class PostService:
    def __init__(self, db: AsyncSession):
        self.post_repository = PostRepository(db)

    async def get_posts(self, offset: int, limit: int) -> PaginatedResponse: 
        return await self.post_repository.get_posts(offset, limit)
    
    async def get_post_by_id(self, post_id: int) -> Post:
        return await self.post_repository.get_post_by_id(post_id)

    async def create_post(self, post: PostCreate) -> Post:
        return await self.post_repository.create_post(post)
    
    async def delete_post(self, post_id: int, user_id: int):
        await self.post_repository.delete_post(post_id, user_id)
        return {"detail": f"Post with id {post_id} has been deleted."}
    
    async def update_post(self, post: PostUpdate, user_id: int) -> Post:
        return await self.post_repository.update_post(post, user_id)
