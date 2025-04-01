import logging

from sqlalchemy import func
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.comment import Comment as CommentEntity
from app.domain.dto.comment import CommentCreate, CommentUpdate
from app.domain.dto.pagination import PaginatedResponse
from app.domain.exceptions.base import AccessError
from app.domain.exceptions.comment import (
    CommentDoesNotExist,
    CommentCreateError,
    CommentUpdateError,
    CommentDeleteError
)
from app.infrastructure.database.repositories.utils.pages import get_prev_next_pages
from app.infrastructure.database.models.comment import Comment as CommentModel


class CommentRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def save(self, comment: CommentCreate, current_user_id: int) -> CommentEntity:
        db_comment = CommentModel(
            text_content=comment.text_content,
            post_id=comment.post_id,
            user_id=current_user_id
        )
        self.db.add(db_comment)
        try:
            await self.db.commit()
            await self.db.refresh(db_comment)
            logging.info("Comment created successfully")
            return CommentEntity.model_validate(db_comment)
        except IntegrityError as e:
            await self.db.rollback()
            logging.error(f"Integrity error: {str(e)}")
            raise CommentCreateError("Error creating comment")

    async def get_all_by_post_id(self, post_id: int, offset: int, limit: int) -> PaginatedResponse:
        count_result = await self.db.execute(select(func.count()).filter(CommentModel.post_id == post_id))
        count = count_result.scalar()

        result = await self.db.execute(
            select(CommentModel).filter(CommentModel.post_id == post_id).offset(offset).limit(limit))
        db_comments = result.scalars().all()

        if not db_comments:
            logging.warning(f"No comments found for post_id={post_id}")
            return PaginatedResponse(count=count)

        comments = [CommentEntity.model_validate(db_comment) for db_comment in db_comments]
        prev_page, next_page = get_prev_next_pages(offset, limit, count, "comments")
        logging.info(f"Fetched {len(comments)} comments for post_id={post_id}")
        return PaginatedResponse(count=count, prev=prev_page, next=next_page, results=comments)

    async def update(self, comment: CommentUpdate, current_user_id: int) -> CommentEntity:
        result = await self.db.execute(select(CommentModel).filter(CommentModel.id == comment.id))
        db_comment = result.scalars().first()

        if not db_comment:
            logging.error(f"Comment with id={comment.id} not found")
            raise CommentDoesNotExist("This comment doesn't exist")
        if db_comment.user_id != current_user_id:
            logging.warning(f"User {current_user_id} has no access to update comment id={comment.id}")
            raise AccessError("You do not have access rights")

        try:
            db_comment.text_content = comment.text_content
            await self.db.commit()
            await self.db.refresh(db_comment)
            logging.info("Comment updated successfully")
            return CommentEntity.model_validate(db_comment)
        except IntegrityError as e:
            await self.db.rollback()
            logging.error(f"Integrity error: {str(e)}")
            raise CommentUpdateError("Error updating comment")

    async def delete(self, comment_id: int, current_user_id: int) -> None:
        result = await self.db.execute(select(CommentModel).filter(CommentModel.id == comment_id))
        db_comment = result.scalars().first()

        if not db_comment:
            logging.error(f"Comment with id={comment_id} not found")
            raise CommentDoesNotExist("This comment doesn't exist")
        if db_comment.user_id != current_user_id:
            logging.warning(f"User {current_user_id} has no access to delete comment id={comment_id}")
            raise AccessError("You do not have access rights")

        try:
            await self.db.delete(db_comment)
            await self.db.commit()
            logging.info("Comment deleted successfully")
        except IntegrityError as e:
            await self.db.rollback()
            logging.error(f"Integrity error: {str(e)}")
            raise CommentDeleteError("Error deleting comment")
