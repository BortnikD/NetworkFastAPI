from fastapi import Depends

from app.services.core_services.comment_service import CommentService
from app.infrastructure.database.repositories.comment_repository import CommentRepository
from app.dependencies.db import get_db


def get_comment_service(db=Depends(get_db)) -> CommentService:
    comment_repo = CommentRepository(db)
    return CommentService(comment_repo)