from fastapi import APIRouter

from . import post_controller, user_controller, comment_controller, like_controller


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

router.include_router(
    like_controller.router,
    tags=['likes']
)