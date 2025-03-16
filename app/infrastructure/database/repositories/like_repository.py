import logging
from fastapi import HTTPException
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.infrastructure.database.repositories.utils.pages import get_prev_next_pages
from app.infrastructure.database.models.like import Like
from app.domain.dto.like import LikePublic
from app.domain.dto.pagination import PaginatedResponse
from app.domain.repository.like import ILike


class LikeRepository(ILike):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def save(self, post_id: int, current_user_id: int) -> Like:
        like = Like(
            user_id=current_user_id,
            post_id=post_id
        )
        self.db.add(like)
        try:
            await self.db.commit()
            await self.db.refresh(like)
            logging.info(f'Like with id={like.id} created by user {like.user_id} for post {post_id}')
            return like
        except IntegrityError:
            await self.db.rollback()
            logging.error(f'Like by user {current_user_id} for post {post_id} already exists')
            raise HTTPException(
                status_code=400,
                detail="You have already liked this post"
            )
        except SQLAlchemyError as e:
            await self.db.rollback()
            logging.error(f"Database error: {str(e)}")
            raise HTTPException(status_code=500, detail="Internal server error")

    async def get_all_by_post_id(self, post_id: int, offset: int, limit: int) -> PaginatedResponse:
        count_result = await self.db.execute(select(func.count()).where(Like.post_id == post_id))
        count = count_result.scalar()

        result = await self.db.execute(
            select(Like).where(Like.post_id == post_id).offset(offset).limit(limit)
        )
        likes = result.scalars().all()

        if not likes:
            logging.warning(f'No likes found for post_id={post_id}')
            return PaginatedResponse(count=count)

        likes_public = [LikePublic.model_validate(like) for like in likes]
        prev, next = get_prev_next_pages(offset, limit, count, 'likes')

        logging.info(f'Fetched {len(likes_public)} likes for post_id={post_id}')
        return PaginatedResponse(
            count=count,
            prev=prev,
            next=next,
            results=likes_public
        )

    async def delete(self, like_id: int, current_user_id: int) -> None:
        result = await self.db.execute(select(Like).where(Like.id == like_id))
        like = result.scalars().first()

        if not like:
            logging.warning(f'User {current_user_id} tried to delete non-existing like {like_id}')
            raise HTTPException(status_code=404, detail=f"Like with id={like_id} does not exist")

        if like.user_id != current_user_id:
            logging.warning(f'User {current_user_id} tried to delete like {like_id} without permission')
            raise HTTPException(status_code=403, detail="You do not have access rights")

        try:
            await self.db.delete(like)
            await self.db.commit()
            logging.info(f'Like {like_id} deleted by user {current_user_id}')
        except SQLAlchemyError as e:
            await self.db.rollback()
            logging.error(f"Error deleting like {like_id}: {str(e)}")
            raise HTTPException(status_code=500, detail=f'Error deleting like id={like_id}')