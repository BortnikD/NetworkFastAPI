import logging

from sqlalchemy import func
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from app.domain.repositories.subscription import ISubscription
from app.domain.dto.pagination import PaginatedResponse
from app.domain.entities.subscription import Subscription as SubscriptionEntity
from app.domain.exceptions.base import AccessError
from app.domain.exceptions.subscription import (
    SubscriptionAlreadyExists,
    SubscriptionDoesNotExist,
    SubscriptionDeleteError
)

from app.infrastructure.database.models.subscription import Subscription as SubscriptionModel
from app.infrastructure.database.repositories.utils.pages import get_prev_next_pages


class SubscriptionRepository(ISubscription):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_subscriptions_by_user_id(self,
                                           current_user_id: int,
                                           offset: int,
                                           limit: int) -> PaginatedResponse:
        count_result = await self.db.execute(
            select(func.count()).filter(SubscriptionModel.follower_id == current_user_id)
        )
        count = count_result.scalars().first()

        result = await self.db.execute(
            select(SubscriptionModel)
            .filter(SubscriptionModel.follower_id == current_user_id)
            .offset(offset)
            .limit(limit)
        )
        subscriptions = result.scalars().all()

        if subscriptions:
            subscriptions = [SubscriptionEntity.model_validate(sub) for sub in subscriptions]
            prev_page, next_page = get_prev_next_pages(offset, limit, count, 'subscriptions')

            logging.info(f'Subscriptions by user_id={current_user_id} issued')
            return PaginatedResponse(
                count=count,
                prev=prev_page,
                next=next_page,
                results=subscriptions
            )
        else:
            logging.info(f'Subscriptions by user_id={current_user_id} issued')
            return PaginatedResponse(count=count)

    async def save(self, current_user_id: int, followed_user_id: int) -> SubscriptionEntity:
        subscription = SubscriptionModel(
            follower_id=current_user_id,
            followed_user_id=followed_user_id
        )

        self.db.add(subscription)
        try:
            await self.db.commit()
            await self.db.refresh(subscription)
            logging.info(f'Subscription created follower_id={current_user_id} followed_user_id={followed_user_id}')
            return SubscriptionEntity.model_validate(subscription)
        except IntegrityError:
            await self.db.rollback()
            logging.error('Error creating subscription')
            raise SubscriptionAlreadyExists('Subscription already exists')

    async def delete(self, subscription_id: int, current_user_id: int) -> None:
        result = await self.db.execute(
            select(SubscriptionModel).filter(SubscriptionModel.id == subscription_id)
        )
        subscription = result.scalar()

        if not subscription:
            logging.warning(f'The user id={current_user_id} attempted to delete a non-existent subscription.')
            raise SubscriptionDoesNotExist("Subscription does not exist")

        if not subscription.follower_id == current_user_id:
            logging.warning(f'user with id={current_user_id} tried to delete subscription id={subscription_id}')
            raise AccessError('You have not access rights')

        try:
            await self.db.delete(subscription)
            await self.db.commit()
            logging.info(f'subscription id={subscription_id} deleted')
        except SQLAlchemyError as e:
            logging.error(f'some error by delete subscription with id={subscription_id}, error = {e}')
            raise SubscriptionDeleteError("error deleting subscription")
