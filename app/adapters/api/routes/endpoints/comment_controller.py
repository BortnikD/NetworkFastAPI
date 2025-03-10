from fastapi import APIRouter, Depends, HTTPException, Path, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

from app.infrastructure.database.models.user import User
from app.adapters.api.dependencies.auth import get_current_active_user
from app.adapters.api.dependencies.db import get_db
from app.core.dto.pagination import CommentPagination, PaginatedResponse
from app.core.dto.comment import CommentCreate, CommentPublic, CommentUpdate
from app.core.services.comment_service import CommentService

router = APIRouter(
    prefix='/comments'
)


@router.post('/', response_model=CommentPublic)
async def create_comments(comment: CommentCreate, current_user: User = Depends(get_current_active_user), db: AsyncSession = Depends(get_db)):
    comment_service = CommentService(db)
    try: 
        return await comment_service.create_comment(comment, current_user.id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get('/{post_id}')
async def read_comments(pagination: Annotated[CommentPagination, Query()],
                       post_id: int = Path(gt=0),
                       db: AsyncSession = Depends(get_db)) -> PaginatedResponse:
    comment_service = CommentService(db)
    try:
        return await comment_service.get_comments_by_post_id(post_id, pagination.offset, pagination.limit)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.patch('/', response_model=CommentPublic)
async def update_comments(comment: CommentUpdate, current_user: User = Depends(get_current_active_user), db: AsyncSession = Depends(get_db)):
    comment_service = CommentService(db)
    try:
        return await comment_service.update_comment(comment, current_user.id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete('/{comment_id}')
async def delete_comment(comment_id: int, current_user: User = Depends(get_current_active_user), db: AsyncSession = Depends(get_db)):
    comment_service = CommentService(db)
    try:
        return await comment_service.delete_comment(comment_id, current_user.id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
