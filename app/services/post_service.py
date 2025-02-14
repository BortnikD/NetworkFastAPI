from sqlalchemy.orm import Session

from app.schemas.post import PostCreate, PostPublic
from app.schemas.pagination import PaginatedResponse
from app.repositories.post_repository import PostRepository


class PostService:
    def __init__(self, db: Session):
        self.post_repository = PostRepository(db)

    def get_posts(self, offset: int, limit: int) -> PaginatedResponse: 
        return self.post_repository.get_posts(offset, limit)

    def create_post(self, post: PostCreate) -> PostPublic:
        return self.post_repository.create_post(post)