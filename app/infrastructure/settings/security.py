import jwt
from datetime import datetime, timedelta, timezone

from passlib.context import CryptContext

from app.infrastructure.settings.config import AUTH_KEY, HASHING_ALGORITHM

pwd_context = CryptContext(schemes=["bcrypt"], deprecated='auto', bcrypt__default_rounds=12)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, AUTH_KEY, algorithm=HASHING_ALGORITHM)


def decode_access_token(token: str) -> str:
    """Декодирует токен и возвращает пользователя, если токен валиден."""
    payload = jwt.decode(token, AUTH_KEY, algorithms=[HASHING_ALGORITHM])
    email: str = payload.get("sub")
    exp: int = payload.get("exp")

    if not email:
        raise ValueError("Invalid token: missing 'sub' field")

    # Проверяем, не истек ли токен
    if datetime.now(timezone.utc).timestamp() > exp:
        raise ValueError("Token expired")

    return email

