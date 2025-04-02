from app.domain.dto.pagination import PaginatedResponse
from app.domain.exceptions.user import UserDoesNotExist
from app.domain.dto.user import UserCreate, UserDB
from app.domain.repositories.user import IUser
from app.domain.entities.user import User
from app.infrastructure.settings.security import decode_access_token


class UserService:
    def __init__(self, user_port: IUser) -> None:
        self.user_port = user_port

    async def save(self, user_create: UserCreate) -> User:
        return await self.user_port.save(user_create)

    async def get_all(self, offset: int, limit: int) -> PaginatedResponse:
        return await self.user_port.get_all(offset, limit)
    
    async def get_by_id(self, user_id: int) -> User:
        return await self.user_port.get_by_id(user_id)

    async def _get_by_email(self, email: str) -> UserDB:
        return await self.user_port.get_by_email(email)

    async def _get_by_token(self, token: str) -> UserDB:
        email = decode_access_token(token)
        if not email:
            raise UserDoesNotExist("email is empty")
        user = await self._get_by_email(email)
        return user
