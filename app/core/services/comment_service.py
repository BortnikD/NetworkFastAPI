from app.core.interfaces.comment import IComment
from app.infrastructure.database.models.comment import Comment
from app.core.dto.comment import CommentCreate, CommentUpdate
from app.core.dto.pagination import PaginatedResponse


class CommentService:
    def __init__(self, comment_port: IComment):
        self.comment_port = comment_port
        
    async def create_comment(self, comment: CommentCreate, current_user_id: int) -> Comment:
        return await self.comment_port.save(comment, current_user_id)

    async def get_comments_by_post_id(self, post_id: int, offset: int, limit: int) -> PaginatedResponse:
        return await self.comment_port.get_all_by_post_id(post_id, offset, limit)
    
    async def update_comment(self, comment: CommentUpdate, current_user_id: int) -> Comment:
        return await self.comment_port.update(comment, current_user_id)
    
    async def delete_comment(self, comment_id, current_user_id) -> None:
        await self.comment_port.delete(comment_id, current_user_id)