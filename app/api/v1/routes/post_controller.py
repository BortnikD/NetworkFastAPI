from fastapi import APIRouter, HTTPException, Depends, Query, Path
from sqlalchemy.orm import Session
from typing import Annotated

from app.schemas.pagination import PaginatedResponse, PostPagination
from app.schemas.post import PostCreate, PostPublic
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