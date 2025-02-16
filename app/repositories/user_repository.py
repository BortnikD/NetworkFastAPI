from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from passlib.context import CryptContext
from typing import Optional

from app.database.models.user import User
from app.schemas.user import UserCreate, UserPublic
from app.schemas.pagination import PaginatedResponse
from app.core.config import BASE_URL


class UserRepository:
    def __init__(self, db: Session):
        self.db = db
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated='auto', bcrypt__default_rounds=12)

    def get_user_by_email(self, email: str) -> User | None:
        return self.db.query(User).filter(User.email == email).first()
    
    def create_user(self, user_create: UserCreate) -> Optional[UserPublic]:
        hashed_password = self.pwd_context.hash(user_create.password)
        db_user = User (
            username=user_create.username,
            email=user_create.email,
            first_name=user_create.first_name,
            last_name=user_create.last_name,
            password_hash=hashed_password
        )
        self.db.add(db_user)
        try:
            self.db.commit()
            self.db.refresh(db_user)
            return db_user
        except IntegrityError:
            self.db.rollback()
            raise ValueError("Пользователь с таким email или username уже существует.")

    def get_users(self, offset: int, limit: int) -> PaginatedResponse:
        total_count = self.db.query(User).count()
        users = self.db.query(User).offset(offset).limit(limit).all()
        if users:
            users = [UserPublic.from_orm(user) for user in users]
            prev_offset = offset - limit if offset > 0 else None
            next_offset = offset + limit if offset + limit < total_count else None

            return PaginatedResponse(
                count=total_count,
                prev=f"{BASE_URL}/api/v1/users?offset={prev_offset}&limit={limit}" if prev_offset is not None else None,
                next=f"{BASE_URL}/api/v1/users?offset={next_offset}&limit={limit}" if next_offset is not None else None,
                results=users
            )
        else:
            return PaginatedResponse(
                count=total_count
            )
    
    def get_user_by_id(self, id: int) -> User | None:
        return self.db.query(User).filter(User.id == id).first()