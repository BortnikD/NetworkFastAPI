from app.core.interfaces.comment import IComment
from app.infrastructure.database.models.comment import Comment
from app.core.dto.comment import CommentCreate, CommentUpdate
from app.core.dto.pagination import PaginatedResponse


class CommentService:
    def __init__(self, comment_port: IComment):
        self.comment_port = comment_port
        
    async def save(self, comment: CommentCreate, current_user_id: int) -> Comment:
        return await self.comment_port.save(comment, current_user_id)

    async def get_all_by_post_id(self, post_id: int, offset: int, limit: int) -> PaginatedResponse:
        return await self.comment_port.get_all_by_post_id(post_id, offset, limit)
    
    async def update(self, comment: CommentUpdate, current_user_id: int) -> Comment:
        return await self.comment_port.update(comment, current_user_id)
    
    async def delete(self, comment_id, current_user_id) -> None:
        await self.comment_port.delete(comment_id, current_user_id)