from sqlalchemy.ext.asyncio import AsyncEngine

from app.adapters.repositories.profile_repository import ProfileRepository
from app.adapters.api.schemas.profile import ProfilePublic


class ProfileService:
    def __init__(self, db: AsyncEngine):
        self.repository = ProfileRepository(db)
        
        
    async def get_profile_by_id(self, user_id: int) -> ProfilePublic:
        return await self.repository.get_profile_by_id(user_id)