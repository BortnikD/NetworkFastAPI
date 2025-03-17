from app.domain.dto.pagination import PaginatedResponse
from app.infrastructure.database.models.user import User
from app.domain.dto.user import UserCreate
from app.domain.repositories.user import IUser


class UserService:
    def __init__(self, user_port: IUser) -> None:
        self.user_port = user_port

    async def save(self, user_create: UserCreate) -> User:
        return await self.user_port.save(user_create)

    async def get_all(self, offset: int, limit: int) -> PaginatedResponse:
        return await self.user_port.get_all(offset, limit)
    
    async def get_by_id(self, user_id: int) -> User:
        return await self.user_port.get_by_id(user_id)

    async def get_by_email(self, email: str) -> User:
        return await self.user_port.get_by_email(email)
