from datetime import timedelta
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordRequestForm

from app.database.models.user import User
from app.api.dependencies.db import get_db
from core.services.user_service import UserService
from app.api.dependencies.auth import get_current_active_user
from app.core.security import create_access_token, verify_password
from app.core.config import ACCESS_TOKEN_EXPIRE_DAYS
from app.api.schemas.user import UserPublic
from app.api.schemas.auth import Token

router = APIRouter()


async def authenticate_user(db: AsyncSession, email: str, password: str) -> User | None:
    user = await UserService(db).get_user_by_email(email)
    if not user or not verify_password(password, user.password_hash):
        return None
    return user


@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: AsyncSession = Depends(get_db),
):
    user = await authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)
    access_token = create_access_token(data={"sub": user.email}, expires_delta=access_token_expires)
    return Token(access_token=access_token, token_type="bearer")


@router.get("/users/me/", response_model=UserPublic)
async def read_users_me(
    current_user: Annotated[UserPublic, Depends(get_current_active_user)],
):
    return current_user


