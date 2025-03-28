from fastapi import APIRouter, Depends, Query, Body, HTTPException
from typing import Annotated

from app.domain.dto.user import UserPublic
from app.domain.dto.post import PostCreate, PostPublic, PostUpdate
from app.domain.dto.pagination import PaginatedResponse, PostPagination
from app.domain.exceptions.base import AccessError
from app.domain.exceptions.post import (
    PostCreateError,
    PostDoesNotExist,
    PostDeleteError,
    PostUpdateError
)

from app.services.core_services.post_service import PostService
from app.dependencies.auth import get_current_active_user
from app.dependencies.services.post import get_post_service

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
    try:
        post = PostCreate(text_content=text_content, user_id=current_user.id)
        return await post_service.save(post)
    except PostCreateError as e:
        raise HTTPException(status_code=500, detail=e.message)


@router.delete('/{post_id}')
async def delete_post(
    post_id: int,
    current_user: UserPublic = Depends(get_current_active_user),
    post_service: PostService = Depends(get_post_service)
):
    """Удаление поста пользователя."""
    try:
        return await post_service.delete(post_id, current_user.id)
    except PostDoesNotExist as e:
        raise HTTPException(status_code=404, detail=e.message)
    except PostDeleteError as e:
        raise HTTPException(status_code=500, detail=e.message)
    except AccessError as e:
        raise HTTPException(status_code=403, detail=e.message)


@router.patch('/', response_model=PostPublic)
async def update_post(
    post: PostUpdate,
    current_user: UserPublic = Depends(get_current_active_user),
    post_service: PostService = Depends(get_post_service)
):
    """Обновление поста."""
    try:
        return await post_service.update(post, current_user.id)
    except PostDoesNotExist as e:
        raise HTTPException(status_code=404, detail=e.message)
    except PostUpdateError as e:
        raise HTTPException(status_code=500, detail=e.message)
    except AccessError as e:
        raise HTTPException(status_code=403, detail=e.message)
