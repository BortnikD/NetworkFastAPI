from fastapi import APIRouter, HTTPException, Depends, Query, Body
from typing import Annotated

from app.core.dto.user import UserPublic
from app.core.dto.post import PostCreate, PostPublic, PostUpdate
from app.core.dto.pagination import PaginatedResponse, PostPagination
from app.core.services.post_service import PostService
from app.adapters.api.dependencies.auth import get_current_active_user
from app.adapters.api.dependencies.services.post import get_post_service

router = APIRouter(prefix='/posts')


@router.get('/', response_model=PaginatedResponse)
async def read_posts(
    pagination: Annotated[PostPagination, Query()],
    post_service: PostService = Depends(get_post_service)
):
    """Получение списка постов с пагинацией."""
    return await post_service.get_all_posts(pagination.offset, pagination.limit)


@router.post('/', response_model=PostPublic)
async def create_post(
    text_content: str = Body(...),
    current_user: UserPublic = Depends(get_current_active_user),
    post_service: PostService = Depends(get_post_service)
):
    """Создание нового поста."""
    post = PostCreate(text_content=text_content, user_id=current_user.id)
    return await post_service.save(post)


@router.delete('/{post_id}')
async def delete_post(
    post_id: int,
    current_user: UserPublic = Depends(get_current_active_user),
    post_service: PostService = Depends(get_post_service)
):
    """Удаление поста пользователя."""
    return await post_service.delete(post_id, current_user.id)


@router.patch('/', response_model=PostPublic)
async def update_post(
    post: PostUpdate,
    current_user: UserPublic = Depends(get_current_active_user),
    post_service: PostService = Depends(get_post_service)
):
    """Обновление поста."""
    return await post_service.update(post, current_user.id)
