import logging
from fastapi import APIRouter, FastAPI

from .endpoints.http import profile_controller, image_controller, post_controller, user_controller, auth_controller, \
    comment_controller, like_controller, subscription_controller, messages_controller
from .endpoints.websockets import messages
from app.infrastructure.settings.config import BASE_URL


def include_routers(router: APIRouter):
    try:
        router.include_router(user_controller.router, tags=['users'])
        router.include_router(post_controller.router, tags=['posts'])
        router.include_router(comment_controller.router, tags=['comments'])
        router.include_router(like_controller.router, tags=['likes'])
        router.include_router(image_controller.router, tags=['images'])
        router.include_router(subscription_controller.router, tags=['subscriptions'])
        router.include_router(profile_controller.router, tags=['profiles'])
        router.include_router(messages_controller.router, tags=['messages'])
    except Exception as e:
        logging.error(f"Failed to configure routers: {e}")


def include_auth_routers(router: APIRouter):
    try:
        router.include_router(auth_controller.router, tags=['auth'])
    except Exception as e:
        logging.error(f"Failed to configure auth routers: {e}")


def setup_routers(app: FastAPI):
    router = APIRouter()
    auth_router = APIRouter()
    include_routers(router)
    include_auth_routers(auth_router)
    app.include_router(
        router,
        prefix='/api'
    )
    app.include_router(
        auth_controller.router,
        tags=['auth']
    )

    ws_router = APIRouter(
        prefix="/messages"
    )
    ws_router.include_router(messages.router)

    logging.info(f'All routers are configured on {BASE_URL}/docs')