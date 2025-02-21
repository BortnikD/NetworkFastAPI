import logging
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.api.schemas.comment import CommentCreate, CommentPublic, CommentUpdate
from app.database.models.comment import Comment
from app.api.schemas.pagination import PaginatedResponse
from app.core.config import BASE_URL


class CommentRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_comment(self, comment: CommentCreate, current_user_id: int) -> Comment:
        db_comment = Comment(
            text_content=comment.text_content,
            post_id=comment.post_id,
            user_id=current_user_id
        )
        self.db.add(db_comment)
        try:
            await self.db.commit() 
            await self.db.refresh(db_comment) 
            logging.info(f'Comment with id = {db_comment.id} by user = {db_comment.user_id} was successfully created')
            return db_comment
        except IntegrityError:
            await self.db.rollback()  
            logging.error(f'Due to some error, the comment with post_id = {comment.post_id} and user_id = {current_user_id} was not created.')
            raise ValueError("Ошибка при попытке создать комментарий")
        
    async def get_comments_by_post_id(self, post_id: int, offset: int, limit: int) -> PaginatedResponse:
        result = await self.db.execute(select(Comment).filter(Comment.post_id == post_id))
        comments_count = len(result.scalars().all())
        result = await self.db.execute(select(Comment).filter(Comment.post_id == post_id).offset(offset).limit(limit))
        comments = result.scalars().all()
        
        if comments:
            comments = [CommentPublic.from_orm(comment) for comment in comments]
            prev_offset = offset - limit if offset > 0 else None
            next_offset = offset + limit if offset + limit < comments_count else None
            logging.info(f"Fetched {len(comments)} comments for post_id = {post_id}, offset = {offset}, limit = {limit}")
            return PaginatedResponse(
                count=comments_count,
                prev=f"{BASE_URL}/api/v1/comments?offset={prev_offset}&limit={limit}" if prev_offset is not None else None,
                next=f"{BASE_URL}/api/v1/comments?offset={next_offset}&limit={limit}" if next_offset is not None else None,
                results=comments
            )
        else:
            logging.warning(f"No comments found for post_id = {post_id}")
            return PaginatedResponse(count=comments_count)
        
    async def update_comment(self, comment: CommentUpdate, current_user_id: int) -> Comment:
        result = await self.db.execute(select(Comment).filter(Comment.id == comment.id))
        db_comment = result.scalars().first()

        if not db_comment:
            logging.error(f"Comment with id = {comment.id} not found for update.")
            raise HTTPException(status_code=404, detail="This comment doesn't exist")
        if db_comment.user_id != current_user_id:
            logging.warning(f"User {current_user_id} attempted to update comment with id = {comment.id}, but does not have access.")
            raise HTTPException(status_code=403, detail="You do not have access rights")
        
        try:
            db_comment.text_content = comment.text_content
            await self.db.commit()  
            logging.info(f"Comment with id = {comment.id} successfully updated")
            return db_comment
        except IntegrityError:
            await self.db.rollback() 
            logging.error(f"IntegrityError while updating comment with id = {comment.id}")
            raise ValueError(f"Problem with updating comment id = {comment.id}")

    async def delete_comment(self, comment_id: int, current_user_id: int):
        result = await self.db.execute(select(Comment).filter(Comment.id == comment_id))
        comment = result.scalars().first()

        if not comment:
            logging.error(f"Comment with id = {comment_id} not found for deletion.")
            raise HTTPException(status_code=404, detail="This comment doesn't exist")
        if comment.user_id != current_user_id:
            logging.warning(f"User {current_user_id} attempted to delete comment with id = {comment_id}, but does not have access.")
            raise HTTPException(status_code=403, detail="You do not have access rights")
        
        try:
            await self.db.delete(comment) 
            await self.db.commit()  
            logging.info(f"Comment with id = {comment_id} successfully deleted")
        except IntegrityError:
            await self.db.rollback()  # Асинхронный rollback
            logging.error(f"IntegrityError while deleting comment with id = {comment_id}")
            raise ValueError(f"Problem with deleting comment id = {comment_id}")
