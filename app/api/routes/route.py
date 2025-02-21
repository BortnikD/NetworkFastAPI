import logging
from fastapi import APIRouter

from . import post_controller, user_controller, comment_controller, like_controller, image_controller

router = APIRouter()


def include_routers():
    try:
        router.include_router(user_controller.router, tags=['users'])
        router.include_router(post_controller.router, tags=['posts'])
        router.include_router(comment_controller.router, tags=['comments'])
        router.include_router(like_controller.router, tags=['likes'])
        router.include_router(image_controller.router, tags=['images'])
        logging.info('All routers are configured')
    except Exception as e:
        logging.error(f"Failed to configure routers: {e}")
