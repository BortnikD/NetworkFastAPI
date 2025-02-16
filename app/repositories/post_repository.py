from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException

from app.database.models.post import Post
from app.schemas.post import PostCreate, PostPublic, PostUpdate
from app.schemas.pagination import PaginatedResponse
from app.config import BASE_URL


class PostRepository:
    def __init__(self, db: Session) -> None:
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
        
    def get_post_by_id(self, post_id: int) -> Post:
        post = self.db.query(Post).filter(Post.id == post_id).first()
        if not post:
            raise ValueError(f'Пост с id {post_id} не найден')
        return post

    def create_post(self, post: PostCreate) -> Post:
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
        
    def delete_post(self, post_id: int, user_id: int) -> None:
        post_to_delete = self.db.query(Post).filter(Post.id == post_id).first()
        if post_to_delete is None:
            raise ValueError(f"Пост с id {post_id} не найден")
        if not (post_to_delete.user_id == user_id):
            raise HTTPException(status_code=403, detail="You do not have access rights")
        try:
            self.db.delete(post_to_delete)
            self.db.commit()
        except IntegrityError:
            self.db.rollback()
            raise ValueError(f'Ошибка при удаление поста с post_id={post_id}')
        
    def update_post(self, post: PostUpdate, user_id: int) -> Post:
        db_post = self.db.query(Post).filter(Post.id == post.id).first()
        if db_post is None:
            raise ValueError(f"Пост с id {post.id} не найден")
        if not (db_post.user_id == user_id):
            raise HTTPException(status_code=403, detail="You do not have access rights")
        try:
            db_post.text_content = post.text_content
            self.db.commit()
            return db_post
        except IntegrityError:
            self.db.rollback()
            raise ValueError(f'Ошибка при изменении поста с post_id={post.id}')
