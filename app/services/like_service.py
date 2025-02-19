from sqlalchemy.orm import Session

from app.database.models.like import Like
from app.schemas.pagination import PaginatedResponse
from app.repositories.like_repository import LikeRepository


class LikeService:
    def __init__(self, db: Session):
        self.like_repository = LikeRepository(db)

    def create_like(self, post_id: int, current_user_id: int) -> Like:
        return self.like_repository.create_like(post_id, current_user_id)

    def get_likes_by_post_id(self, post_id: int, offset: int, limit: int) -> PaginatedResponse:
        return self.like_repository.get_likes_by_post_id(post_id, offset, limit)

    def delete_like(self, like_id: int, current_user_id: int):
        self.like_repository.delete_like(like_id, current_user_id)