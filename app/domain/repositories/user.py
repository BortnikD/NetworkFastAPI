from abc import ABC, abstractmethod

from app.domain.dto.pagination import PaginatedResponse
from app.domain.entities.user import User
from app.domain.dto.user import UserCreate, UserDB


class IUser(ABC):
    @abstractmethod
    async def save(self, user_create: UserCreate) -> User:
        raise NotImplementedError

    @abstractmethod
    async def get_by_email(self, email: str) -> UserDB:
        raise NotImplementedError

    @abstractmethod
    async def get_all(self, offset: int, limit: int) -> PaginatedResponse:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, user_id: int) -> User:
        raise NotImplementedError
