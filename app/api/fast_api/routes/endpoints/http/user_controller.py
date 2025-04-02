from typing import Annotated

from fastapi import APIRouter, HTTPException, Depends, Query, Path

from app.domain.dto.pagination import UsersPagination, PaginatedResponse
from app.domain.dto.user import UserCreate
from app.domain.entities.user import User
from app.domain.exceptions.user import (
    UserDoesNotExist,
    UserAlreadyExists,
    UserCreateError
)

from app.services.core_services.user_service import UserService
from app.dependencies.services.user import get_user_service

router = APIRouter(prefix='/users')


@router.post('/')
async def create_user(
    user_create: UserCreate,
    service: UserService = Depends(get_user_service)
    ) -> User:
    """Создание нового пользователя."""
    try:
        return await service.save(user_create)
    except UserAlreadyExists as e:
        raise HTTPException(status_code=409, detail=e.message)
    except UserCreateError as e:
        raise HTTPException(status_code=500, detail=e.message)


@router.get('/')
async def read_users(
    pagination: Annotated[UsersPagination, Query()],
    service: UserService = Depends(get_user_service)
    ) -> PaginatedResponse:
    """Получение списка пользователей с пагинацией."""
    return await service.get_all(pagination.offset, pagination.limit)



@router.get('/{user_id}')
async def read_user(
    user_id: Annotated[int, Path(gt=0)],
    service: UserService = Depends(get_user_service)
    ) -> User:
    """Получение пользователя по ID."""
    try:
        return await service.get_by_id(user_id)
    except UserDoesNotExist as e:
        raise HTTPException(status_code=404, detail=e.message)
