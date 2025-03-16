from fastapi import Depends

from app.core.services.post_service import PostService
from app.adapters.repositories.post_repository import PostRepository
from app.adapters.dependencies.db import get_db


def get_post_service(db=Depends(get_db)) -> PostService:
    post_repo = PostRepository(db)
    return PostService(post_repo)