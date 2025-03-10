import logging
from fastapi import HTTPException
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.database.models.user import User
from app.adapters.api.schemas.user import UserCreate, UserPublic
from app.adapters.api.schemas.pagination import PaginatedResponse
from app.infrastructure.settings.security import pwd_context
from app.core.utils.pages import get_prev_next_pages


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
            raise HTTPException(status_code=400, detail="Пользователь с таким email или username уже существует.")
        except SQLAlchemyError as e:
            await self.db.rollback()
            logging.error(str(e))
            raise ValueError("Ошибка при создании пользователя.")


    async def get_users(self, offset: int, limit: int) -> PaginatedResponse:
        count_result = await self.db.execute(select(func.count()).select_from(User))
        count = count_result.scalar()

        result = await self.db.execute(select(User).offset(offset).limit(limit))
        users = result.scalars().all()

        if users:
            users = [UserPublic.from_orm(user) for user in users]
            prev, next = get_prev_next_pages(offset, limit, count, 'users')
            logging.info(f"users has been issued with count={count}")
            return PaginatedResponse(
                count=count,
                prev=prev,
                next=next,
                results=users
            )
        else:
            logging.warning('users has not been issued')
            return PaginatedResponse(count=count)


    async def get_user_by_id(self, id: int) -> User | None:
        result = await self.db.execute(select(User).filter(User.id == id))
        return result.scalars().first()
