import logging
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from app.core.config import BASE_URL
from app.database.models.like import Like
from app.schemas.like import LikePublic
from app.schemas.pagination import PaginatedResponse


class LikeRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_like(self, post_id: int, current_user_id: int):
        like = Like(
            user_id=current_user_id,
            post_id=post_id
        )
        self.db.add(like)
        try:
            self.db.commit()
            self.db.refresh(like)
            logging.info(f'like with id = {like.id}, user_id={like.user_id}, post_id={post_id} created')
            return like
        except IntegrityError:
            self.db.rollback()
            logging.error(f'like with user_id={current_user_id}, post_id={post_id} not created')
            raise HTTPException(
                status_code=400,
                detail="You have already liked this post"
            )

    def get_likes(self, post_id: int, offset: int, limit: int) -> PaginatedResponse:
        likes_query = self.db.query(Like).filter(Like.post_id == post_id)
        count = likes_query.count()
        likes = likes_query.offset(offset).limit(limit).all()
        if likes:
            likes = [LikePublic.from_orm(like) for like in likes]
            prev_offset = offset - limit if offset > 0 else None
            next_offset = offset + limit if offset + limit < count else None
            logging.info(f'likes by post_id={post_id} issued, total_count={count}')

            return PaginatedResponse(
                count=count,
                prev=f"{BASE_URL}/api/v1/likes?offset={prev_offset}&limit={limit}" if prev_offset is not None else None,
                next=f"{BASE_URL}/api/v1/likes?offset={next_offset}&limit={limit}" if next_offset is not None else None,
                results=likes
            )
        else:
            logging.warning(f'likes by post_id={post_id} not issued, total_count={count}')
            return PaginatedResponse(
                count=count
            )

    def delete_like(self, like_id, current_user_id):
        like = self.db.query(Like).filter(Like.id == like_id).first()
        if not like:
            logging.warning(f'user with id={current_user_id} tried to delete like id={like_id} but it do not exist')
            raise HTTPException(status_code=404, detail=f"Like with id={like_id} do not exist")
        if not current_user_id == like.user_id:
            logging.warning(f'user with id={current_user_id} tried to delete like id={like_id}')
            raise HTTPException(status_code=403, detail="You do not have access rights")
        try:
            self.db.delete(like)
            self.db.commit()
        except SQLAlchemyError as e:
            logging.error(f"Error when user id={current_user_id} trying to delete like id={like_id}, error: {e}")
            raise HTTPException(status_code=500, detail=f'Error when trying to delete like id={like_id}')



