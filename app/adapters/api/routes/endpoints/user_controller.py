from fastapi import APIRouter, HTTPException, Depends, Query, Path
from typing import Annotated

from app.core.dto.pagination import UsersPagination, PaginatedResponse
from app.core.dto.user import UserCreate, UserPublic
from app.core.services.user_service import UserService
from app.adapters.api.dependencies.services.user import get_user_service

router = APIRouter(prefix='/users')


@router.post('/', response_model=UserPublic)
async def create_user(
    user_create: UserCreate,
    service: UserService = Depends(get_user_service)
):
    """Создание нового пользователя."""
    try:
        return await service.create_user(user_create)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get('/', response_model=PaginatedResponse)
async def read_users(
    pagination: Annotated[UsersPagination, Query()],
    service: UserService = Depends(get_user_service)
):
    """Получение списка пользователей с пагинацией."""
    try:
        return await service.get_users(pagination.offset, pagination.limit)
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get('/{user_id}', response_model=UserPublic)
async def read_user(
    user_id: Annotated[int, Path(gt=0)],
    service: UserService = Depends(get_user_service)
):
    """Получение пользователя по ID."""
    try:
        return await service.get_user_by_id(user_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
