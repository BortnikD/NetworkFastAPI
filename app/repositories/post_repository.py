from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.database.models.post import Post
from app.schemas.post import PostCreate, PostPublic
from app.schemas.pagination import PaginatedResponse
from app.config import BASE_URL


class PostRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_posts(self, offset: int, limit: int, order_by: Post = Post.created_at.desc()) -> PaginatedResponse:
        total_count = self.db.query(Post).count()
        posts = self.db.query(Post).order_by(order_by).offset(offset).limit(limit).all()
        if posts: 
            posts = [PostPublic.from_orm(post) for post in posts]
            prev_offset = offset - limit if offset > 0 else None
            next_offset = offset + limit if offset + limit < total_count else None

            return PaginatedResponse(
                count=total_count,
                prev=f"{BASE_URL}/api/v1/posts?offset={prev_offset}&limit={limit}" if prev_offset is not None else None,
                next=f"{BASE_URL}/api/v1/posts?offset={next_offset}&limit={limit}" if next_offset is not None else None,
                results=posts
            )
        else:
            return PaginatedResponse(
                count=total_count
            )

    def create_post(self, post: PostCreate) -> PostPublic:
        db_post = Post(
            user_id=post.user_id,
            text_content=post.text_content
        )
        self.db.add(db_post)
        try:
            self.db.commit()
            self.db.refresh(db_post)
            return db_post  
        except IntegrityError:
            self.db.rollback()
            raise ValueError("Ошибка при попытки создания поста в бд")