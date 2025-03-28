from fastapi import Depends

from app.services.core_services.post_service import PostService
from app.infrastructure.database.repositories.post_repository import PostRepository
from app.dependencies.db import get_db


def get_post_service(db=Depends(get_db)) -> PostService:
    post_repo = PostRepository(db)
    return PostService(post_repo)