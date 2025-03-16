from fastapi import Depends

from app.services.core_services.like_service import LikeService
from app.infrastructure.database.repositories.like_repository import LikeRepository
from app.dependencies.db import get_db


def get_like_service(db=Depends(get_db)) -> LikeService:
    like_repo = LikeRepository(db)
    return LikeService(like_repo)