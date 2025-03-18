from typing import Annotated

from fastapi import APIRouter, HTTPException, Depends, Query, Path

from app.domain.dto.pagination import UsersPagination, PaginatedResponse
from app.domain.dto.user import UserCreate, UserPublic
from app.domain.exceptions.user import (
    UserDoesNotExist,
    UserIsAlreadyExist,
    UserCreateError
)

from app.services.core_services.user_service import UserService
from app.dependencies.services.user import get_user_service

router = APIRouter(prefix='/users')


@router.post('/', response_model=UserPublic)
async def create_user(
    user_create: UserCreate,
    service: UserService = Depends(get_user_service)
):
    """Создание нового пользователя."""
    try:
        return await service.save(user_create)
    except UserIsAlreadyExist as e:
        raise HTTPException(status_code=409, detail=e.message)
    except UserCreateError as e:
        raise HTTPException(status_code=500, detail=e.message)


@router.get('/', response_model=PaginatedResponse)
async def read_users(
    pagination: Annotated[UsersPagination, Query()],
    service: UserService = Depends(get_user_service)
):
    """Получение списка пользователей с пагинацией."""
    return await service.get_all(pagination.offset, pagination.limit)



@router.get('/{user_id}', response_model=UserPublic)
async def read_user(
    user_id: Annotated[int, Path(gt=0)],
    service: UserService = Depends(get_user_service)
):
    """Получение пользователя по ID."""
    try:
        return await service.get_by_id(user_id)
    except UserDoesNotExist as e:
        raise HTTPException(status_code=404, detail=e.message)
