import logging
from sqlalchemy import func, IntegrityError
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

from app.database.models.subscription import Subscription
from app.api.schemas.pagination import PaginatedResponse
from app.api.schemas.subsctiption import SubscriptionPublic
from app.core.utils.pages import get_prev_next_pages


class SubscriptionRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_subscriptions_by_user_id(self, current_user_id: int, offset: int, limit: int) -> PaginatedResponse:
        count_result = await self.db.execute(select(func.count().filter(Subscription.follower_id == current_user_id)))
        count = count_result.scalars().first()

        result = await self.db.execute(select(Subscription)
                                        .filter(Subscription.follower_id == current_user_id)
                                        .offset(offset)
                                        .limit(limit)
                                       )
        subscriptions = result.scalars().all()

        if subscriptions:
            subscriptions = [SubscriptionPublic.from_orm(sub) for sub in subscriptions]
            prev, next = get_prev_next_pages(offset, limit, count, 'subscriptions')

            logging.info(f'Subscriptions by user_id={current_user_id} issued')
            return PaginatedResponse(
                count=count,
                prev=prev,
                next=next,
                results=subscriptions
            )
        else:
            logging.info(f'Subscriptions by user_id={current_user_id} issued')
            return PaginatedResponse(count=count)



    async def create_subscription(self, current_user_id: int, followed_user_id: int) -> Subscription | None:
        subscription = Subscription(
            follower_id=current_user_id,
            followed_user_id=followed_user_id
            )
        
        self.db.add(subscription)
        try:
            await self.db.commit()
            await self.db.refresh(subscription)
            logging.info(f'Subscription created follower_id={current_user_id} followed_user_id={followed_user_id}')
            return subscription
        except IntegrityError:
            await self.db.rollback
            logging.error('Error creating subscription')
            raise HTTPException(status_code=409, detail='Subscription already exists')
