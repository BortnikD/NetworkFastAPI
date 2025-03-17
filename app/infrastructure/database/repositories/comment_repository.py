import logging

from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.domain.repositories.comment import IComment
from app.domain.dto.comment import CommentCreate, CommentPublic, CommentUpdate
from app.domain.dto.pagination import PaginatedResponse
from app.domain.exceptions.base import AccessError
from app.domain.exceptions.comment import (
    CommentDoesNotExist,
    CommentCreateError,
    CommentUpdateError,
    CommentDeleteError
)

from app.infrastructure.database.repositories.utils.pages import get_prev_next_pages
from app.infrastructure.database.models.comment import Comment


class CommentRepository(IComment):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def save(self, comment: CommentCreate, current_user_id: int) -> Comment:
        db_comment = Comment(
            text_content=comment.text_content,
            post_id=comment.post_id,
            user_id=current_user_id
        )
        self.db.add(db_comment)
        try:
            await self.db.commit()
            await self.db.refresh(db_comment)
            logging.info(f"Comment with id = {db_comment.id} by user = {db_comment.user_id} was successfully created")
            return db_comment
        except IntegrityError:
            await self.db.rollback()
            logging.error(f"Error creating comment with post_id = {comment.post_id} and user_id = {current_user_id}.")
            raise CommentCreateError("Error creating comment")

    async def get_all_by_post_id(self, post_id: int, offset: int, limit: int) -> PaginatedResponse:
        count_result = await self.db.execute(select(func.count()).filter(Comment.post_id == post_id))
        count = count_result.scalar()

        result = await self.db.execute(select(Comment).filter(Comment.post_id == post_id).offset(offset).limit(limit))
        comments = result.scalars().all()

        if comments:
            comments = [CommentPublic.model_validate(comment) for comment in comments]
            prev, next = get_prev_next_pages(offset, limit, count, "comments")
            logging.info(f"Fetched {len(comments)} comments for post_id = {post_id}, offset = {offset}, limit = {limit}")
            return PaginatedResponse(count=count, prev=prev, next=next, results=comments)
        else:
            logging.warning(f"No comments found for post_id = {post_id}")
            return PaginatedResponse(count=count)

    async def update(self, comment: CommentUpdate, current_user_id: int) -> Comment:
        result = await self.db.execute(select(Comment).filter(Comment.id == comment.id))
        db_comment = result.scalars().first()

        if not db_comment:
            logging.error(f"Comment with id = {comment.id} not found for update.")
            raise CommentDoesNotExist("This comment doesn't exist")
        if db_comment.user_id != current_user_id:
            logging.warning(f"User {current_user_id} attempted to update comment with id = {comment.id}, but has no access.")
            raise AccessError("You do not have access rights")

        try:
            db_comment.text_content = comment.text_content
            await self.db.commit()
            await self.db.refresh(db_comment)
            logging.info(f"Comment with id = {comment.id} successfully updated")
            return db_comment
        except IntegrityError:
            await self.db.rollback()
            logging.error(f"IntegrityError while updating comment with id = {comment.id}")
            raise CommentUpdateError("Error updating comment")

    async def delete(self, comment_id: int, current_user_id: int) -> None:
        result = await self.db.execute(select(Comment).filter(Comment.id == comment_id))
        comment = result.scalars().first()

        if not comment:
            logging.error(f"Comment with id = {comment_id} not found for deletion.")
            raise CommentDoesNotExist("This comment doesn't exist")
        if comment.user_id != current_user_id:
            logging.warning(f"User {current_user_id} attempted to delete comment with id = {comment_id}, but has no access.")
            raise AccessError("You do not have access rights")

        try:
            await self.db.delete(comment)
            await self.db.commit()
            logging.info(f"Comment with id = {comment_id} successfully deleted")
        except IntegrityError:
            await self.db.rollback()
            logging.error(f"IntegrityError while deleting comment with id = {comment_id}")
            raise CommentDeleteError("Error deleting comment")
