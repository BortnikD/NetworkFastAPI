import logging
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from passlib.context import CryptContext

from app.database.models.user import User
from app.schemas.user import UserCreate, UserPublic
from app.schemas.pagination import PaginatedResponse
from app.core.config import BASE_URL


class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated='auto', bcrypt__default_rounds=12)

    async def get_user_by_email(self, email: str) -> User | None:
        result = await self.db.execute(select(User).filter(User.email == email))
        return result.scalars().first()
    
    async def create_user(self, user_create: UserCreate) -> User:
        hashed_password = self.pwd_context.hash(user_create.password)
        db_user = User(
            username=user_create.username,
            email=user_create.email,
            first_name=user_create.first_name,
            last_name=user_create.last_name,
            password_hash=hashed_password
        )
        logging.info(db_user)
        self.db.add(db_user)
        try:
            await self.db.commit() 
            await self.db.refresh(db_user) 
            return db_user
        except IntegrityError:
            await self.db.rollback()  
            raise ValueError("Пользователь с таким email или username уже существует.")

    async def get_users(self, offset: int, limit: int) -> PaginatedResponse:
        result = await self.db.execute(select(User))
        total_count = len(result.scalars().all())

        result = await self.db.execute(select(User).offset(offset).limit(limit))
        users = result.scalars().all()

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
            return PaginatedResponse(count=total_count)

    async def get_user_by_id(self, id: int) -> User | None:
        result = await self.db.execute(select(User).filter(User.id == id))
        return result.scalars().first()
