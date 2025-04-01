import logging

from sqlalchemy import func
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.user import User as UserEntity
from app.domain.repositories.user import IUser
from app.domain.dto.user import UserCreate
from app.domain.dto.pagination import PaginatedResponse
from app.domain.exceptions.user import (
    UserDoesNotExist,
    UserAlreadyExists,
    UserCreateError
)

from app.infrastructure.database.models.user import User as UserModel
from app.infrastructure.settings.security import pwd_context
from app.infrastructure.database.repositories.utils.pages import get_prev_next_pages


class UserRepository(IUser):
    def __init__(self, db: AsyncSession):
        self.db = db
        self.pwd_context = pwd_context

    async def get_by_email(self, email: str) -> UserEntity:
        result = await self.db.execute(select(UserModel).filter(UserModel.email == email))
        if not result:
            logging.warning(f'user with email={email} does not exist')
            raise UserDoesNotExist("User with this email does not exist")
        user_model = result.scalars().first()
        logging.info(f"User with email={email} has been issued")
        return UserEntity.model_validate(user_model)

    async def save(self, user_create: UserCreate) -> UserEntity:
        hashed_password = self.pwd_context.hash(user_create.password)
        db_user = UserModel(
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
            return UserEntity.model_validate(db_user)
        except IntegrityError:
            await self.db.rollback()
            logging.error(f"An error occurred while creating user")
            raise UserAlreadyExists("Пользователь с таким email или username уже существует.")
        except SQLAlchemyError as e:
            await self.db.rollback()
            logging.error(str(e))
            raise UserCreateError("Ошибка при создании пользователя")

    async def get_all(self, offset: int, limit: int) -> PaginatedResponse:
        count_result = await self.db.execute(select(func.count()).select_from(UserModel))
        count = count_result.scalar()

        result = await self.db.execute(select(UserModel).offset(offset).limit(limit))
        users = result.scalars().all()

        if users:
            users = [UserEntity.model_validate(user) for user in users]
            prev_page, next_page = get_prev_next_pages(offset, limit, count, 'users')
            logging.info(f"users has been issued with count={count}")
            return PaginatedResponse(
                count=count,
                prev=prev_page,
                next=next_page,
                results=users
            )
        else:
            logging.warning('users has not been issued')
            return PaginatedResponse(count=count)

    async def get_by_id(self, user_id: int) -> UserEntity:
        result = await self.db.execute(select(UserModel).filter(UserModel.id == user_id))
        user = result.scalars().first()
        if not user:
            logging.error(f'user with id={user_id} does not exist')
            raise UserDoesNotExist("User with this id does not exist")
        logging.info(f"User with id={user_id} has been issued")
        return UserEntity.model_validate(user)
