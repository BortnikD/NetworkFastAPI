import logging
from fastapi import HTTPException
from sqlalchemy import func, case, distinct
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
        
        
    def __profile_query(self, user_id: int):
        follower_case = case(
            (Subscription.follower_id == user_id, Subscription.id),
            else_=None
        )

        followed_case = case(
            (Subscription.followed_user_id == user_id, Subscription.id),
            else_=None
        )

        query = (
            select(
                User.id,
                User.username,
                User.email,
                User.first_name,
                User.last_name,
                User.is_active,
                func.count(distinct(follower_case)).label("followers_count"),
                func.count(distinct(followed_case)).label("followed_count"),
            )
            .outerjoin(Subscription, (Subscription.follower_id == user_id) | (Subscription.followed_user_id == user_id))
            .filter(User.id == user_id)
            .group_by(User.id)
        )
        return query
        

    async def get_profile_by_id(self, user_id: int) -> ProfilePublic:
        result = await self.db.execute(self.__profile_query(user_id))
        profile_data = result.fetchone()

        if not profile_data:
            logging.warning(f'User with id={user_id} not found')
            raise HTTPException(status_code=404, detail=f'User with id={user_id} not found')

        logging.info(f'Profile user with id={user_id} found successfully')

        return ProfilePublic(
            id=profile_data.id,
            username=profile_data.username,
            email=profile_data.email,
            first_name=profile_data.first_name,
            last_name=profile_data.last_name,
            is_active=profile_data.is_active,
            followers_count=profile_data.followers_count,
            followed_count=profile_data.followed_count
        )