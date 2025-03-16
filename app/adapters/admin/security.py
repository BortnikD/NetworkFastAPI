import jwt
import logging

from fastapi import Request
from sqladmin.authentication import AuthenticationBackend

from app.adapters.dependencies.services.user import get_user_service
from app.infrastructure.database.database import AsyncSessionLocal
from app.infrastructure.database.models import User
from app.infrastructure.settings.security import verify_password, create_access_token
from app.infrastructure.settings.config import AUTH_KEY, HASHING_ALGORITHM


async def authenticate_user(email: str, password: str) -> User | None:
    async with AsyncSessionLocal() as session:
        user_service = get_user_service(session)
        user = await user_service.get_by_email(email)
        if not user or not verify_password(password, user.password_hash):
            return None
        return user


async def get_user_from_token(token: str) -> User | None:
    try:
        payload = jwt.decode(token, AUTH_KEY, algorithms=[HASHING_ALGORITHM])
        email: str = payload.get("sub")
        if not email:
            return None

        async with AsyncSessionLocal() as session:
            user_service = get_user_service(session)
            user = await user_service.get_by_email(email)
            return user if user and user.is_superuser else None
    except Exception as e:
        logging.error(e)


class AdminAuthenticationBackend(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        """Обрабатывает форму входа и возвращает JWT-токен."""
        try:
            form = await request.form()
            email = form.get("username")
            password = form.get("password")

            if not email or not password:
                logging.warning("Missing email or password in login request.")
                return False

            user = await authenticate_user(email, password)
            if not user or not user.is_superuser:
                logging.warning("Invalid credentials or user is not a superuser.")
                return False

            # Генерация JWT-токена
            token = create_access_token({"sub": user.email})
            response = request.session
            response["token"] = token

            return True
        except Exception as e:
            logging.error(f"Error during login: {e}")
            return False

    async def logout(self, request: Request) -> bool:
        """Удаляет токен из сессии при выходе."""
        request.session.pop("token", None)
        return True

    async def authenticate(self, request: Request) -> bool:
        """Проверяет JWT-токен в сессии или заголовке запроса."""
        try:
            token = request.session.get("token")
            if not token:
                auth_header = request.headers.get("Authorization")
                if auth_header and auth_header.startswith("Bearer "):
                    token = auth_header.split(" ")[1]

            if not token:
                logging.warning("Missing token in session or Authorization header.")
                return False

            user = await get_user_from_token(token)
            return bool(user)
        except Exception as e:
            logging.error(f"Error during authentication: {e}")
            return False