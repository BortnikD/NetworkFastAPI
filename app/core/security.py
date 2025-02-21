from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
import jwt
from app.core.config import AUTH_KEY, HASHING_ALGORITHM

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
