from app.core.dto.pagination import PaginatedResponse
from app.infrastructure.database.models.user import User
from app.core.dto.user import UserCreate
from app.core.interfaces.user import IUser


class UserService:
    def __init__(self, user_port: IUser) -> None:
        self.user_port = user_port

    async def create_user(self, user_create: UserCreate) -> User:
        return await self.user_port.save(user_create)

    async def get_users(self, offset: int, limit: int) -> PaginatedResponse:
        return await self.user_port.get_all(offset, limit)
    
    async def get_user_by_id(self, user_id: int) -> User:
        return await self.user_port.get_by_id(user_id)

    async def get_user_by_email(self, email: str) -> User:
        return await self.user_port.get_by_email(email)
