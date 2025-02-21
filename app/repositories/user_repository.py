import logging
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from app.database.models.user import User
from app.api.schemas.user import UserCreate, UserPublic
from app.api.schemas.pagination import PaginatedResponse
from app.core.config import BASE_URL
from app.core.security import pwd_context


class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.pwd_context = pwd_context

    async def get_user_by_email(self, email: str) -> User | None:
        result = await self.db.execute(select(User).filter(User.email == email))
        if not result:
            logging.warning(f'user with email={email} does not exist')
            raise HTTPException(status_code=404, detail="User with this email does not exist")
        logging.info(f"User with email={email} has been issued")
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
        self.db.add(db_user)
        try:
            await self.db.commit()
            await self.db.refresh(db_user)
            logging.info("User is created")
            return db_user
        except IntegrityError:
            await self.db.rollback()
            logging.error(f"An error occurred while creating user")
            raise ValueError("Пользователь с таким email или username уже существует.")
        except SQLAlchemyError as e:
            await self.db.rollback()
            logging.error(str(e))
            raise ValueError("Ошибка при создании пользователя.")

    async def get_users(self, offset: int, limit: int) -> PaginatedResponse:
        result = await self.db.execute(select(User))
        total_count = len(result.scalars().all())

        result = await self.db.execute(select(User).offset(offset).limit(limit))
        users = result.scalars().all()

        if users:
            users = [UserPublic.from_orm(user) for user in users]
            prev_offset = offset - limit if offset > 0 else None
            next_offset = offset + limit if offset + limit < total_count else None
            logging.info(f"users has been issued with count={total_count}")
            return PaginatedResponse(
                count=total_count,
                prev=f"{BASE_URL}/api/v1/users?offset={prev_offset}&limit={limit}" if prev_offset is not None else None,
                next=f"{BASE_URL}/api/v1/users?offset={next_offset}&limit={limit}" if next_offset is not None else None,
                results=users
            )
        else:
            logging.warning('users has not been issued')
            return PaginatedResponse(count=total_count)

    async def get_user_by_id(self, id: int) -> User | None:
        result = await self.db.execute(select(User).filter(User.id == id))
        return result.scalars().first()
