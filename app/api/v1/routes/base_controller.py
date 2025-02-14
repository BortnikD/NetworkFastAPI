from fastapi import APIRouter

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