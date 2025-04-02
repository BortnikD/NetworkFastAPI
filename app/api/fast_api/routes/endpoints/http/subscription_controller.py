from fastapi import APIRouter, Depends, Query, HTTPException
from typing import Annotated

from app.domain.dto.pagination import LikePagination, PaginatedResponse
from app.domain.entities.subscription import Subscription
from app.domain.exceptions.base import AccessError
from app.domain.exceptions.subscription import (
    SubscriptionAlreadyExists,
    SubscriptionDoesNotExist,
    SubscriptionDeleteError, SelfSubscriptionError
)

from app.services.core_services.subscription_service import SubscriptionService
from app.dependencies.auth import get_current_active_user
from app.dependencies.services.subscription import get_subscription_service
from app.infrastructure.database.models import User

router = APIRouter(prefix='/subscriptions')


@router.get('/{user_id}')
async def get_subscriptions_by_user_id(
        user_id: int,
        pagination: Annotated[LikePagination, Query()],
        service: SubscriptionService = Depends(get_subscription_service)
        ) -> PaginatedResponse:
    """Получить список подписок пользователя."""
    try:
        return await service.get_subscriptions_by_user_id(user_id, pagination.offset, pagination.limit)
    except SubscriptionDoesNotExist as e:
        raise HTTPException(status_code=404, detail=e.message)


@router.post('/')
async def create_subscription(
        followed_user_id: int,
        current_user: User = Depends(get_current_active_user),
        service: SubscriptionService = Depends(get_subscription_service)
        ) -> Subscription:
    """Создать подписку на пользователя."""
    try:
        return await service.save(current_user.id, followed_user_id)
    except SubscriptionAlreadyExists as e:
        raise HTTPException(status_code=409, detail=e.message)
    except SelfSubscriptionError as e:
        raise HTTPException(status_code=409, detail=e.message)


@router.delete('/{subscription_id}')
async def delete_subscription(
        subscription_id: int,
        current_user: User = Depends(get_current_active_user),
        service: SubscriptionService = Depends(get_subscription_service)
        ) -> None:
    """Удалить подписку по её ID."""
    try:
        return await service.delete(subscription_id, current_user.id)
    except SubscriptionDoesNotExist as e:
        raise HTTPException(status_code=404, detail=e.message)
    except SubscriptionDeleteError as e:
        raise HTTPException(status_code=404, detail=e.message)
    except AccessError as e:
        raise HTTPException(status_code=403, detail=e.message)
