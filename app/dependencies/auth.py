import jwt
from typing import Annotated
from jwt.exceptions import InvalidTokenError
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from app.infrastructure.database.models.user import User
from app.dependencies.services.user import get_user_service
from app.services.use_cases.user_service import UserService
from app.infrastructure.settings.config import AUTH_KEY, HASHING_ALGORITHM


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def get_current_user(
        token: Annotated[str, Depends(oauth2_scheme)],
        service: UserService = Depends(get_user_service)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, AUTH_KEY, algorithms=[HASHING_ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except InvalidTokenError:
        raise credentials_exception

    user = await service.get_by_email(email)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
        current_user: Annotated[User, Depends(get_current_user)],
):
    return current_user