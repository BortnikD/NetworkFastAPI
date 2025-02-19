import logging
from fastapi import APIRouter, Depends, HTTPException, Path, Query
from sqlalchemy.orm import Session
from typing import Annotated

from app.database.models.user import User
from app.dependecies.auth import get_current_active_user
from app.dependecies.db import get_db
from app.schemas.pagination import CommentPagination, PaginatedResponse
from app.schemas.comment import CommentCreate, CommentPublic, CommentUpdate
from app.services.comment_service import CommentService

router = APIRouter(
    prefix='/comments'
)


@router.post('/', response_model=CommentPublic)
async def create_comments(comment: CommentCreate, current_user: User = Depends(get_current_active_user), db: Session = Depends(get_db)):
    comment_service = CommentService(db)
    try: 
        return comment_service.create_comment(comment, current_user.id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get('/{post_id}')
async def read_comments(pagination: Annotated[CommentPagination, Query()],
                       post_id: int = Path(gt=0),
                       db: Session = Depends(get_db)) -> PaginatedResponse:
    comment_service = CommentService(db)
    try:
        return comment_service.get_comments_by_post_id(post_id, pagination.offset, pagination.limit)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.patch('/', response_model=CommentPublic)
async def update_comments(comment: CommentUpdate, current_user: User = Depends(get_current_active_user), db: Session = Depends(get_db)):
    comment_service = CommentService(db)
    try:
        return comment_service.update_comment(comment, current_user.id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete('/{comment_id}')
async def delete_comment(comment_id: int, current_user: User = Depends(get_current_active_user), db: Session = Depends(get_db)):
    comment_service = CommentService(db)
    try:
        return comment_service.delete_comment(comment_id, current_user.id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
