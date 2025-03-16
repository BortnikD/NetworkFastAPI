from fastapi import APIRouter, Depends, Query
from typing import Annotated

from app.services.core_services.subscription_service import SubscriptionService
from app.dependencies.auth import get_current_active_user
from app.dependencies.services.subscription import get_subscription_service
from app.domain.dto.pagination import LikePagination
from app.domain.dto.subscription import SubscriptionPublic
from app.infrastructure.database.models import User

router = APIRouter(prefix='/subscriptions')


@router.get('/{user_id}', response_model=list[SubscriptionPublic])
async def get_subscriptions_by_user_id(
    user_id: int,
    pagination: Annotated[LikePagination, Query()],
    service: SubscriptionService = Depends(get_subscription_service)
):
    """Получить список подписок пользователя."""
    return await service.get_subscriptions_by_user_id(user_id, pagination.offset, pagination.limit)


@router.post('/', response_model=SubscriptionPublic)
async def create_subscription(
    followed_user_id: int,
    current_user: User = Depends(get_current_active_user),
    service: SubscriptionService = Depends(get_subscription_service)
):
    """Создать подписку на пользователя."""
    return await service.save(current_user.id, followed_user_id)


@router.delete('/{subscription_id}')
async def delete_subscription(
    subscription_id: int,
    current_user: User = Depends(get_current_active_user),
    service: SubscriptionService = Depends(get_subscription_service)
):
    """Удалить подписку по её ID."""
    return await service.delete(subscription_id, current_user.id)
