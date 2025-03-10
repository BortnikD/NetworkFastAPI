from fastapi import Depends

from app.core.services.user_service import UserService
from app.adapters.repositories.user_repository import UserRepository
from app.adapters.api.dependencies.db import get_db


def get_user_service(db=Depends(get_db)) -> UserService:
    user_repo = UserRepository(db)
    return UserService(user_repo)