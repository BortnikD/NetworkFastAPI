from fastapi import APIRouter, HTTPException, Depends, Query, Path
from sqlalchemy.orm import Session
from typing import Annotated

from app.schemas.pagination import PaginatedResponse, PostPagination
from app.schemas.post import PostCreate, PostPublic, PostUpdate
from app.services import post_service
from app.services.post_service import PostService
from app.dependecies.db import get_db

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
async def create_post(post: PostCreate, db: Session = Depends(get_db)):
    post_service = PostService(db)
    try:
        post = post_service.create_post(post)
        return post
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    

@router.delete('/{post_id}')
async def delete_post(post_id: int, db: Session = Depends(get_db)) -> None:
    post_service = PostService(db)
    try:
        detail = post_service.delete_post(post_id)  
        return detail
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.patch('/', response_model=PostPublic)
async def update_post(post: PostUpdate, db: Session = Depends(get_db)):
    post_service = PostService(db)
    try:
        post = post_service.update_post(post)
        return post
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))