from fastapi import APIRouter

from app.api.v1.routes import comment_controller

from . import post_controller, user_controller


router = APIRouter()


router.include_router(
    user_controller.router,
    tags=['users']
)

router.include_router(
    post_controller.router,
    tags=['posts']
)

router.include_router(
    comment_controller.router,
    tags=['comments']
)