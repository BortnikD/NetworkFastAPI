from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.comment_repository import CommentRepository
from app.database.models.comment import Comment
from app.schemas.comment import CommentCreate, CommentUpdate
from app.schemas.pagination import PaginatedResponse


class CommentService:
    def __init__(self, db: AsyncSession):
        self.comment_repository = CommentRepository(db)
        
    async def create_comment(self, comment: CommentCreate, current_user_id: int) -> Comment:
        return await self.comment_repository.create_comment(comment, current_user_id)

    async def get_comments_by_post_id(self, post_id: int, offset: int, limit: int) -> PaginatedResponse:
        return await self.comment_repository.get_comments_by_post_id(post_id, offset, limit)
    
    async def update_comment(self, comment: CommentUpdate, current_user_id: int) -> Comment:
        return await self.comment_repository.update_comment(comment, current_user_id)
    
    async def delete_comment(self, comment_id, current_user_id):
        await self.comment_repository.delete_comment(comment_id, current_user_id)