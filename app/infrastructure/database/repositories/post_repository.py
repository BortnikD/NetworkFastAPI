import logging

from sqlalchemy import func
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

from app.domain.dto.post import PostCreate, PostUpdate
from app.domain.dto.pagination import PaginatedResponse
from app.domain.entities.post import Post as PostEntity
from app.domain.repositories.post import IPost
from app.domain.exceptions.base import AccessError
from app.domain.exceptions.post import (
    PostCreateError,
    PostDoesNotExist,
    PostDeleteError,
    PostUpdateError
)

from app.infrastructure.database.models.post import Post as PostModel
from app.infrastructure.database.repositories.utils.pages import get_prev_next_pages


class PostRepository(IPost):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def save(self, post_create: PostCreate) -> PostEntity:
        db_post = PostModel(
            text_content=post_create.text_content,
            user_id=post_create.user_id
        )
        self.db.add(db_post)

        try:
            await self.db.commit()
            await self.db.refresh(db_post)
            logging.info(f"Post created by user_id={post_create.user_id}")
            return PostEntity.model_validate(db_post)
        except SQLAlchemyError as e:
            await self.db.rollback()
            logging.error(f"Error creating post: {str(e)}")
            raise PostCreateError("Error creating post")

    async def get_all_posts(self, offset: int, limit: int) -> PaginatedResponse:
        count_result = await self.db.execute(select(func.count()).select_from(PostModel))
        count = count_result.scalar()

        result = await self.db.execute(
            select(PostModel)
            .order_by(PostModel.created_at.desc())
            .offset(offset)
            .limit(limit)
        )
        posts = result.scalars().all()

        if posts:
            posts = [PostEntity.model_validate(post) for post in posts]
            prev_page, next_page = get_prev_next_pages(offset, limit, count, 'posts')
            logging.info(f"Posts retrieved with count={count}")
            return PaginatedResponse(
                count=count,
                prev=prev_page,
                next=next_page,
                results=posts
            )
        else:
            logging.warning("No posts found")
            return PaginatedResponse(count=count)

    async def get_post(self, post_id: int) -> PostEntity:
        result = await self.db.execute(
            select(PostModel).filter(PostModel.id == post_id)
        )
        post = result.scalar()
        if not post:
            logging.error(f"Post with id={post_id} not found")
            raise PostDoesNotExist("Post does not exist")
        return PostEntity.model_validate(post)

    async def delete(self, post_id: int, user_id: int) -> None:
        result = await self.db.execute(
            select(PostModel).filter(PostModel.id == post_id)
        )
        post = result.scalar()

        if not post:
            logging.error(f"Post with id={post_id} not found")
            raise PostDoesNotExist("Post does not exist")

        if post.user_id != user_id:
            logging.warning(f"User {user_id} attempted to delete post {post_id} without permission")
            raise AccessError("You don't have permission to delete this post")

        try:
            await self.db.delete(post)
            await self.db.commit()
            logging.info(f"Post {post_id} deleted by user {user_id}")
        except SQLAlchemyError as e:
            await self.db.rollback()
            logging.error(f"Error deleting post: {str(e)}")
            raise PostDeleteError("Error deleting post")

    async def update(self, post_update: PostUpdate, user_id: int) -> PostEntity:
        result = await self.db.execute(
            select(PostModel).filter(PostModel.id == post_update.id)
        )
        post = result.scalar()

        if not post:
            logging.error(f"Post with id={post_update.id} not found")
            raise PostDoesNotExist("Post does not exist")

        if post.user_id != user_id:
            logging.warning(f"User {user_id} attempted to update post {post_update.id} without permission")
            raise AccessError("You don't have permission to update this post")

        try:
            post.text_content = post_update.text_content
            await self.db.commit()
            await self.db.refresh(post)
            logging.info(f"Post {post_update.id} updated by user {user_id}")
            return PostEntity.model_validate(post)
        except SQLAlchemyError as e:
            await self.db.rollback()
            logging.error(f"Error updating post: {str(e)}")
            raise PostUpdateError("Error updating post")
