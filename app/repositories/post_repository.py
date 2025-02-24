from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.database.models.post import Post
from app.api.schemas.post import PostCreate, PostPublic, PostUpdate
from app.api.schemas.pagination import PaginatedResponse
from app.core.utils.pages import get_prev_next_pages


class PostRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get_posts(self, offset: int, limit: int, order_by: Post = Post.created_at.desc()) -> PaginatedResponse:
        result = await self.db.execute(select(Post).order_by(order_by))
        total_count = len(result.scalars().all())
        
        result = await self.db.execute(select(Post).offset(offset).limit(limit).order_by(order_by))
        posts = result.scalars().all()
        
        if posts:
            posts = [PostPublic.model_validate(post) for post in posts]
            prev, next = get_prev_next_pages(offset, limit, total_count, 'posts')

            return PaginatedResponse(
                count=total_count,
                prev=prev,
                next=next,
                results=posts
            )
        else:
            return PaginatedResponse(count=total_count)
        
    async def get_post_by_id(self, post_id: int) -> Post:
        result = await self.db.execute(select(Post).filter(Post.id == post_id))
        post = result.scalars().first()
        if not post:
            raise ValueError(f'Пост с id {post_id} не найден')
        return post

    async def create_post(self, post: PostCreate) -> Post:
        db_post = Post(
            user_id=post.user_id,
            text_content=post.text_content
        )
        self.db.add(db_post)
        try:
            await self.db.commit() 
            await self.db.refresh(db_post)  
            return db_post  
        except IntegrityError:
            await self.db.rollback()  
            raise ValueError("Ошибка при попытке создания поста в бд")

    async def delete_post(self, post_id: int, user_id: int) -> None:
        result = await self.db.execute(select(Post).filter(Post.id == post_id))
        post_to_delete = result.scalars().first()
        if post_to_delete is None:
            raise ValueError(f"Пост с id {post_id} не найден")
        if post_to_delete.user_id != user_id:
            raise HTTPException(status_code=403, detail="You do not have access rights")
        try:
            await self.db.delete(post_to_delete)
            await self.db.commit()  
        except SQLAlchemyError:
            await self.db.rollback() 
            raise ValueError(f'Ошибка при удалении поста с post_id={post_id}')
        
    async def update_post(self, post: PostUpdate, user_id: int) -> Post:
        result = await self.db.execute(select(Post).filter(Post.id == post.id))
        db_post = result.scalars().first()
        if db_post is None:
            raise ValueError(f"Пост с id {post.id} не найден")
        if db_post.user_id != user_id:
            raise HTTPException(status_code=403, detail="You do not have access rights")
        try:
            db_post.text_content = post.text_content
            await self.db.commit() 
            return db_post
        except IntegrityError:
            await self.db.rollback() 
            raise ValueError(f'Ошибка при изменении поста с post_id={post.id}')
