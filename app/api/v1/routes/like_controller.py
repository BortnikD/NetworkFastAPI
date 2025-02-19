from fastapi import APIRouter, Query, Body
from fastapi.params import Depends
from sqlalchemy.orm import Session
from typing import Annotated

from app.database.models.user import User
from app.dependecies.db import get_db
from app.dependecies.auth import get_current_active_user
from app.services.like_service import LikeService
from app.schemas.pagination import LikePagination, PaginatedResponse
from app.schemas.like import LikePublic, LikeCreate

router = APIRouter(
    prefix='/likes'
)


@router.get('/{post_id}', response_model=PaginatedResponse)
async def read_likes(post_id: int, pagination: Annotated[LikePagination, Query()], db: Session = Depends(get_db)):
    like_service = LikeService(db)
    return like_service.get_likes_by_post_id(post_id, pagination.offset, pagination.limit)


@router.post('/', response_model=LikePublic)
async def create_like(like: LikeCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    like_service = LikeService(db)
    return like_service.create_like(like.post_id, current_user.id)


@router.delete('/{post_id}')
async def delete_like(post_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    like_service = LikeService(db)
    return like_service.delete_like(post_id, current_user.id)