import logging
from fastapi import HTTPException
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.core.config import BASE_URL
from app.core.utils.pages import get_prev_next_pages
from app.database.models.like import Like
from app.api.schemas.like import LikePublic
from app.api.schemas.pagination import PaginatedResponse


class LikeRepository:
    def __init__(self, db: AsyncSession):
        self.db = db


    async def create_like(self, post_id: int, current_user_id: int):
        like = Like(
            user_id=current_user_id,
            post_id=post_id
        )
        self.db.add(like)
        try:
            await self.db.commit()  # Асинхронный commit
            await self.db.refresh(like)  # Асинхронное обновление объекта
            logging.info(f'like with id = {like.id}, user_id={like.user_id}, post_id={post_id} created')
            return like
        except IntegrityError:
            await self.db.rollback()  # Асинхронный rollback
            logging.error(f'like with user_id={current_user_id}, post_id={post_id} not created')
            raise HTTPException(
                status_code=400,
                detail="You have already liked this post"
            )
        except SQLAlchemyError as e:
            logging.error(e)


    async def get_likes_by_post_id(self, post_id: int, offset: int, limit: int) -> PaginatedResponse:
        count_result = await self.db.execute(select(func.count()).filter(Like.post_id == post_id))
        count = count_result.scalar()
        result = await self.db.execute(select(Like).filter(Like.post_id == post_id).offset(offset).limit(limit))
        likes = result.scalars().all()

        if likes:
            likes = [LikePublic.model_validate(like) for like in likes]
            prev, next = get_prev_next_pages(offset, limit, count, 'likes')
            logging.info(f'likes by post_id={post_id} issued, total_count={count}')

            return PaginatedResponse(
                count=count,
                prev=prev,
                next=next,
                results=likes
            )
        else:
            logging.warning(f'likes by post_id={post_id} not issued, total_count={count}')
            return PaginatedResponse(
                count=count
            )


    async def delete_like(self, like_id: int, current_user_id: int):
        result = await self.db.execute(select(Like).filter(Like.id == like_id))
        like = result.scalars().first()

        if not like:
            logging.warning(f'user with id={current_user_id} tried to delete like id={like_id} but it does not exist')
            raise HTTPException(status_code=404, detail=f"Like with id={like_id} does not exist")

        if like.user_id != current_user_id:
            logging.warning(f'user with id={current_user_id} tried to delete like id={like_id}')
            raise HTTPException(status_code=403, detail="You do not have access rights")

        try:
            await self.db.delete(like)
            await self.db.commit()  # Асинхронный commit
        except SQLAlchemyError as e:
            logging.error(f"Error when user id={current_user_id} trying to delete like id={like_id}, error: {e}")
            raise HTTPException(status_code=500, detail=f'Error when trying to delete like id={like_id}')
