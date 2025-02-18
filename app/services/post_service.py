from sqlalchemy.orm import Session

from app.database.models.post import Post
from app.schemas.post import PostCreate, PostUpdate
from app.schemas.pagination import PaginatedResponse
from app.repositories.post_repository import PostRepository


class PostService:
    def __init__(self, db: Session):
        self.post_repository = PostRepository(db)

    def get_posts(self, offset: int, limit: int) -> PaginatedResponse: 
        return self.post_repository.get_posts(offset, limit)
    
    def get_post_by_id(self, post_id: int) -> Post:
        return self.post_repository.get_post_by_id(post_id)

    def create_post(self, post: PostCreate) -> Post:
        return self.post_repository.create_post(post)
    
    def delete_post(self, post_id: int, user_id: int):
        self.post_repository.delete_post(post_id, user_id)
        return {"detail": f"Post with id {post_id} has been deleted."}
    
    def update_post(self, post: PostUpdate, user_id: int) -> Post:
        return self.post_repository.update_post(post, user_id)
