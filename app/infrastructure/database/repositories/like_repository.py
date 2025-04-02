import logging

from sqlalchemy import func
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.domain.dto.pagination import PaginatedResponse
from app.domain.repositories.like import ILike
from app.domain.entities.like import Like as LikeEntity
from app.domain.exceptions.base import AccessError
from app.domain.exceptions.like import (
    AlreadyLikedPost,
    LikeDoesNotExist,
    LikeDeleteError,
)

from app.infrastructure.database.repositories.utils.pages import get_prev_next_pages
from app.infrastructure.database.models.like import Like as LikeModel


class LikeRepository(ILike):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def save(self, post_id: int, current_user_id: int) -> LikeEntity:
        like = LikeModel(
            user_id=current_user_id,
            post_id=post_id
        )
        self.db.add(like)
        try:
            await self.db.commit()
            await self.db.refresh(like)
            logging.info(f'Like with id={like.id} created by user {like.user_id} for post {post_id}')
            return LikeEntity.model_validate(like)
        except IntegrityError:
            await self.db.rollback()
            logging.error(f'Like by user {current_user_id} for post {post_id} already exists')
            raise AlreadyLikedPost("You have already liked this post")

    async def get_all_by_post_id(self, post_id: int, offset: int, limit: int) -> PaginatedResponse:
        count_result = await self.db.execute(select(func.count()).where(LikeModel.post_id == post_id))
        count = count_result.scalar()

        result = await self.db.execute(
            select(LikeModel).where(LikeModel.post_id == post_id).offset(offset).limit(limit)
        )
        likes = result.scalars().all()

        if not likes:
            logging.warning(f'No likes found for post_id={post_id}')
            return PaginatedResponse(count=count)

        likes_entities = [LikeEntity.model_validate(like) for like in likes]
        prev_page, next_page = get_prev_next_pages(offset, limit, count, 'likes')

        logging.info(f'Fetched {len(likes_entities)} likes for post_id={post_id}')
        return PaginatedResponse(
            count=count,
            prev=prev_page,
            next=next_page,
            results=likes_entities
        )

    async def delete(self, like_id: int, current_user_id: int) -> None:
        result = await self.db.execute(select(LikeModel).where(LikeModel.id == like_id))
        like = result.scalars().first()

        if not like:
            logging.warning(f'User {current_user_id} tried to delete non-existing like {like_id}')
            raise LikeDoesNotExist(f"Like with id={like_id} does not exist")

        if like.user_id != current_user_id:
            logging.warning(f'User {current_user_id} tried to delete like {like_id} without permission')
            raise AccessError("You do not have access rights")

        try:
            await self.db.delete(like)
            await self.db.commit()
            logging.info(f'Like {like_id} deleted by user {current_user_id}')
        except SQLAlchemyError as e:
            logging.error(f"error deleting like: {e}")
            raise LikeDeleteError("error deleting like")
