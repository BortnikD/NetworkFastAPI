from app.domain.dto.profile import ProfilePublic
from app.domain.repositories.profile import IProfile


class ProfileService:
    def __init__(self, profile_port: IProfile):
        self.profile_port = profile_port
        
        
    async def get_by_user_id(self, user_id: int) -> ProfilePublic:
        return await self.profile_port.get_by_user_id(user_id)