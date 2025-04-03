from datetime import timedelta
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.dependencies.services.user import get_user_service
from app.services.core_services.user_service import UserService
from app.dependencies.auth import get_current_active_user
from app.infrastructure.settings.security import create_access_token, verify_password
from app.infrastructure.settings.config import ACCESS_TOKEN_EXPIRE_DAYS
from app.domain.dto.user import UserDB
from app.domain.entities.user import User as UserEntity
from app.domain.dto.auth import Token

router = APIRouter()


async def authenticate_user(
    email: str,
    password: str,
    user_service: UserService = Depends(get_user_service)
    ) -> UserDB | None:
    user = await user_service._get_by_email(email)
    if not user or not verify_password(password, user.password_hash):
        return None
    return user


@router.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    user_service: UserService = Depends(get_user_service)
    ) -> Token:
    user = await authenticate_user(form_data.username, form_data.password, user_service)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)
    access_token = create_access_token(data={"sub": user.email}, expires_delta=access_token_expires)
    return Token(access_token=access_token, token_type="bearer")


@router.get("/users/me/")
async def read_users_me(
    current_user: UserDB = Depends(get_current_active_user),
    user_service: UserService = Depends(get_user_service)
    ) -> UserEntity:
    """Получает информацию о текущем авторизованном пользователе."""
    user = await user_service.get_by_id(current_user.id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
