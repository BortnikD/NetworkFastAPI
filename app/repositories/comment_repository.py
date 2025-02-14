from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.schemas.comment import CommentCreate, CommentPublic
from app.models.comment import Comment
from app.schemas.pagination import PaginatedResponse
from app.config import BASE_URL


class CommentRepository:
    def __init__(self, db: Session):
        self.db = db
