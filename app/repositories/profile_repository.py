import logging
from fastapi import HTTPException
from sqlalchemy import func, case, distinct
from sqlalchemy.sql import label
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import (
    User, 
    Subscription
)
from app.api.schemas.profile import ProfilePublic


class ProfileRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
        

    async def _get_subscriptions(self, user_id: int):
        follower_case = case(
            (Subscription.follower_id == user_id, Subscription.id),
            else_=None
        )

        followed_case = case(
            (Subscription.followed_user_id == user_id, Subscription.id),
            else_=None
        )

        subs_result = await self.db.execute(select(
            label('followers_count', func.count(distinct(follower_case))),
            label('followed_count', func.count(distinct(followed_case)))
        ).select_from(Subscription))
        subscriptions = subs_result.fetchone()
        
        if not subscriptions:
            logging.warning(f'User with id={user_id} subscriptions not found')
            raise HTTPException(status_code=404, detail=f'User with id={user_id} subscriptions not found')
        
        return subscriptions
    
    
    async def get_profile_by_id(self, user_id: int) -> ProfilePublic:
        result = await self.db.execute(select(User).filter(User.id == user_id))
        user = result.fetchone()
        if not user:
            logging.warning(f'user with id={user_id} is not found')
            raise HTTPException(status_code=404, detail=f'user with id={user_id} is not found')
        logging.info(f'user with id = {user_id} is found')
        
        subscriptions = await self._get_subscriptions(user.id)
        logging.info(f'Profile user with id={user.id} found successfully')
        
        return ProfilePublic(
            id=user.id,
            username=user.username,
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
            is_active=user.is_active,
            followers_count=subscriptions.followers_count,
            followed_count=subscriptions.followed_count
        )