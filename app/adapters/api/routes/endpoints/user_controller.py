from fastapi import APIRouter, HTTPException, Depends, Query, Path
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

from app.core.dto.pagination import UsersPagination, PaginatedResponse
from app.core.dto import UserCreate, UserPublic
from app.core.services.user_service import UserService
from app.adapters.api.dependencies.db import get_db

router = APIRouter(
    prefix='/users'
)


@router.post('/', response_model=UserPublic)
async def create_user(user_create: UserCreate, db: AsyncSession = Depends(get_db)):
    user_service = UserService(db)
    try: 
        user = await user_service.create_user(user_create)
        return user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))



@router.get('/', response_model=PaginatedResponse)
async def read_users(pagination: Annotated[UsersPagination, Query()], db: AsyncSession = Depends(get_db)):
    user_service = UserService(db)
    try:
        users = await user_service.get_users(pagination.offset, pagination.limit)
        return users
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@router.get('/{user_id}', response_model=UserPublic)
async def read_user(user_id: Annotated[int, Path(gt=0)], db: AsyncSession = Depends(get_db)):
    user_service = UserService(db)
    try:
        user = await user_service.get_user_by_id(user_id)
        return user
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))