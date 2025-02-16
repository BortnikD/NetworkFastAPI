from fastapi import APIRouter, HTTPException, Depends, Query, Path, Body
from sqlalchemy.orm import Session
from typing import Annotated

from app.schemas.user import UserPublic
from app.schemas.post import PostCreate, PostPublic, PostUpdate
from app.schemas.pagination import PaginatedResponse, PostPagination
from app.services.post_service import PostService
from app.dependecies.db import get_db
from app.dependecies.auth import get_current_active_user

router = APIRouter(
    prefix='/posts'
)


@router.get('/', response_model=PaginatedResponse)
async def read_posts(pagination: Annotated[PostPagination, Query()],
                    db: Session = Depends(get_db)):
    post_service = PostService(db)
    try:
        posts = post_service.get_posts(pagination.offset, pagination.limit)
        return posts
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@router.post('/', response_model=PostPublic)
async def create_post(text_content: str = Body(),
                    db: Session = Depends(get_db),
                    current_user: UserPublic = Depends(get_current_active_user)):
    post_service = PostService(db)
    try:
        post = PostCreate(text_content=text_content, user_id=current_user.id)
        post = post_service.create_post(post)
        return post
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    

@router.delete('/{post_id}')
async def delete_post(post_id: int, db: Session = Depends(get_db),
                      current_user: UserPublic = Depends(get_current_active_user)) -> None:
    post_service = PostService(db)
    
    try:
        detail = post_service.delete_post(post_id, current_user.id)  
        return detail
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.patch('/', response_model=PostPublic)
async def update_post(post: PostUpdate, db: Session = Depends(get_db),
                      current_user: UserPublic = Depends(get_current_active_user)):
    post_service = PostService(db)
    try:
        post = post_service.update_post(post, current_user.id)
        return post
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))