import logging
from fastapi import HTTPException
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.interfaces.post import IPost
from app.infrastructure.database.models.post import Post
from app.core.dto.post import PostCreate, PostPublic, PostUpdate
from app.core.dto.pagination import PaginatedResponse
from app.adapters.repositories.utils.pages import get_prev_next_pages


class PostRepository(IPost):
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def save(self, post: PostCreate) -> Post:
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
            raise HTTPException(status_code=400, detail="Ошибка при попытке создания поста в бд")

    async def get_all_posts(self, offset: int, limit: int) -> PaginatedResponse:
        count_result = await self.db.execute(select(func.count()).select_from(Post))
        count = count_result.scalar()

        result = await self.db.execute(select(Post).offset(offset).limit(limit).order_by(Post.created_at.desc()))
        posts = result.scalars().all()

        if posts:
            posts = [PostPublic.model_validate(post) for post in posts]
            prev, next = get_prev_next_pages(offset, limit, count, 'posts')
            logging.info(f'posts issued all posts count = {count}')
            return PaginatedResponse(
                count=count,
                prev=prev,
                next=next,
                results=posts
            )
        else:
            logging.warning(f'posts not issued count = {count}')
            return PaginatedResponse(count=count)

    async def get_post(self, post_id: int) -> Post:
        result = await self.db.execute(select(Post).filter(Post.id == post_id))
        post = result.scalars().first()
        if not post:
            logging.error(f'Пост с id {post_id} не найден')
            raise HTTPException(status_code=404, detail=f'Пост с id {post_id} не найден')
        return post

    async def delete(self, post_id: int, current_user_id: int) -> None:
        result = await self.db.execute(select(Post).filter(Post.id == post_id))
        post_to_delete = result.scalars().first()
        if post_to_delete is None:
            logging.warning(f"Пост с id {post_id} не найден")
            raise HTTPException(status_code=404, detail=f"Пост с id {post_id} не найден")
        if post_to_delete.user_id != current_user_id:
            logging.warning(f'user with id = {current_user_id} tried to delete post with id = {post_id}')
            raise HTTPException(status_code=403, detail="You do not have access rights")
        try:
            await self.db.delete(post_to_delete)
            await self.db.commit()
            logging.info(f'success deleted post with id = {post_id}')
        except SQLAlchemyError:
            await self.db.rollback()
            logging.error(f'Ошибка при удалении поста с post_id={post_id}')
            raise HTTPException(status_code=500, detail=f'Ошибка при удалении поста с post_id={post_id}')

    async def update(self, post: PostUpdate, current_user_id: int) -> Post:
        result = await self.db.execute(select(Post).filter(Post.id == post.id))
        db_post = result.scalars().first()
        if db_post is None:
            logging.warning(f"Пост с id {post.id} не найден")
            raise HTTPException(status_code=404, detail=f"Пост с id {post.id} не найден")
        if db_post.user_id != current_user_id:
            logging.warning(f'user with id = {current_user_id} tried to update post with id = {post.id}')
            raise HTTPException(status_code=403, detail="You do not have access rights")
        try:
            db_post.text_content = post.text_content
            await self.db.commit()
            logging.info(f'success updated post with id = {post.id}')
            return db_post
        except IntegrityError:
            await self.db.rollback()
            logging.error(f'Ошибка при изменении поста с post_id={post.id}')
            raise HTTPException(status_code=400, detail=f'Ошибка при изменении поста с post_id={post.id}')
