from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.core_services.user_service import UserService
from app.infrastructure.database.repositories.user_repository import UserRepository
from app.dependencies.db import get_db


def get_user_service(db: AsyncSession = Depends(get_db)) -> UserService:
    user_repo = UserRepository(db)
    return UserService(user_repo)