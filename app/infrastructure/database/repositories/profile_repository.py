import logging

from sqlalchemy import func, distinct
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.dto.profile import ProfilePublic
from app.domain.repositories.profile import IProfile
from app.domain.exceptions.user import UserDoesNotExist

from app.infrastructure.database.models import User, Subscription


def _profile_query(user_id: int):
    return (
        select(
            User.id,
            User.username,
            User.email,
            User.first_name,
            User.last_name,
            User.is_active,
            func.count(distinct(Subscription.follower_id)).filter(Subscription.followed_user_id == user_id).label(
                "followers_count"),
            func.count(distinct(Subscription.followed_user_id)).filter(Subscription.follower_id == user_id).label(
                "followed_count"),
        )
        .outerjoin(Subscription, (Subscription.follower_id == user_id) | (Subscription.followed_user_id == user_id))
        .filter(User.id == user_id)
        .group_by(User.id)
    )


class ProfileRepository(IProfile):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_user_id(self, user_id: int) -> ProfilePublic:
        result = await self.db.execute(_profile_query(user_id))
        profile_data = result.fetchone()

        if not profile_data:
            logging.warning(f'User with id={user_id} not found')
            raise UserDoesNotExist(f'User with id={user_id} not found')

        logging.info(f'Profile user with id={user_id} found successfully')

        return ProfilePublic(**profile_data.model_dump())
