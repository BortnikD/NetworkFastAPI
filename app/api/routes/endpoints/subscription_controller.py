from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncEngine
from typing import Annotated

from app.core.services.subscription_servise import SubscriptionService
from app.api.dependencies.auth import get_current_active_user
from app.api.dependencies.db import get_db
from app.api.schemas.pagination import LikePagination
from app.database.models import User


router = APIRouter(
    prefix='/subscriptions'
)


@router.get('/{user_id}')
async def get_subscriptions_by_user_id(user_id: int, 
                                       pagination: Annotated[LikePagination, Query()],
                                       db: AsyncEngine = Depends(get_db)
                                       ):
    service = SubscriptionService(db)
    return await service.get_subscriptions_by_user_id(user_id, pagination.offset, pagination.limit)


@router.post('/')
async def create_subscription(followed_user_id: int, 
                              db: AsyncEngine = Depends(get_db), 
                              current_user: User = Depends(get_current_active_user)):
    service = SubscriptionService(db)
    return await service.create_subscription(current_user.id, followed_user_id)


@router.delete('/{subscription_id}')
async def delete_subscription(subscription_id: int,
                              db: AsyncEngine = Depends(get_db), 
                              current_user: User = Depends(get_current_active_user)):
    service = SubscriptionService(db)
    return await service.delete_subscription_by_id(subscription_id, current_user.id)