from fastapi import APIRouter, Query, Depends
from typing import Annotated

from app.infrastructure.database.models.user import User
from app.dependencies.auth import get_current_active_user
from app.services.core_services.like_service import LikeService
from app.domain.dto.pagination import LikePagination, PaginatedResponse
from app.domain.dto.like import LikePublic, LikeCreate
from app.dependencies.services.like import get_like_service

router = APIRouter(prefix='/likes')


@router.get('/{post_id}', response_model=PaginatedResponse)
async def read_likes(
    post_id: int,
    pagination: Annotated[LikePagination, Query()],
    like_service: LikeService = Depends(get_like_service)
):
    """Получение списка лайков по ID поста."""
    return await like_service.get_all_by_post_id(post_id, pagination.offset, pagination.limit)


@router.post('/', response_model=LikePublic)
async def create_like(
    like: LikeCreate,
    current_user: User = Depends(get_current_active_user),
    like_service: LikeService = Depends(get_like_service)
):
    """Создание лайка для поста."""
    return await like_service.save(like.post_id, current_user.id)


@router.delete('/{post_id}')
async def delete_like(
    post_id: int,
    current_user: User = Depends(get_current_active_user),
    like_service: LikeService = Depends(get_like_service)
):
    """Удаление лайка с поста."""
    return await like_service.delete(post_id, current_user.id)
