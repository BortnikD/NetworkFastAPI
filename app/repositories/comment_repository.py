from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
import logging

from app.schemas.comment import CommentCreate, CommentPublic, CommentUpdate
from app.database.models.comment import Comment
from app.schemas.pagination import PaginatedResponse
from app.core.config import BASE_URL


class CommentRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_comment(self, comment: CommentCreate, current_user_id: int) -> Comment:
        logging.info(f'{comment.text_content}')
        db_comment = Comment(
            text_content=comment.text_content,
            post_id=comment.post_id,
            user_id=current_user_id
        )
        self.db.add(db_comment)
        try:
            self.db.commit()
            self.db.refresh(db_comment)
            logging.info(f'Comment with id = {db_comment.id} by user = {db_comment.user.username} was successfully created')
            return db_comment
        except IntegrityError:
            logging.error(f'Due to some error, the comment with id = {db_comment.id} was not created.')
            raise ValueError("Ошибка при попытки создать комментарий")
        
    def get_comments_by_post_id(self, post_id: int, offset: int, limit: int) -> PaginatedResponse:
        comments_count = self.db.query(Comment).filter(Comment.post_id == post_id).count()
        comments = self.db.query(Comment).filter(Comment.post_id == post_id).offset(offset).limit(limit).all()
        if comments:
            comments = [CommentPublic.from_orm(comment) for comment in comments]
            prev_offset = offset - limit if offset > 0 else None
            next_offset = offset + limit if offset + limit < comments_count else None
            return PaginatedResponse(
                count=comments_count,
                prev=f"{BASE_URL}/api/v1/comments?offset={prev_offset}&limit={limit}" if prev_offset is not None else None,
                next=f"{BASE_URL}/api/v1/comments?offset={next_offset}&limit={limit}" if next_offset is not None else None,
                results=comments
            )
        else:
            return PaginatedResponse(
                count=comments_count
            )
        
    def update_comment(self, comment: CommentUpdate, current_user_id) -> Comment:
        db_comment = self.db.query(Comment).filter(Comment.id == comment.id).first()
        if not db_comment:
            raise HTTPException(status_code=404, detail="This comment doesn't exist")
        if db_comment.user_id != current_user_id:
            raise HTTPException(status_code=403, detail="You do not have access rights")
        try:
            db_comment.text_content = comment.text_content
            self.db.commit()
            return db_comment
        except IntegrityError:
            self.db.rollback()
            raise ValueError(f"Problem with deleting comment id = {comment.id}")

    def delete_comment(self, comment_id: int, current_user_id: int):
        comment = self.db.query(Comment).filter(Comment.id == comment_id).first()
        if not comment:
            raise HTTPException(status_code=404, detail="This comment doesn't exist")
        if comment.user_id != current_user_id:
            raise HTTPException(status_code=403, detail="You do not have access rights")
        try:
            self.db.delete(comment)
            self.db.commit()
        except IntegrityError:
            self.db.rollback()
            raise ValueError(f"Problem with deleting comment id = {comment_id}")
        
