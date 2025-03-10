from abc import ABC, abstractmethod

from app.core.dto.pagination import PaginatedResponse
from app.core.entities.user import User
from app.core.dto.user import UserCreate


class IUser(ABC):
    @abstractmethod
    async def save(self, user_create: UserCreate) -> User | None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_email(self, email: str) -> User | None:
        raise NotImplementedError

    @abstractmethod
    async def get_all(self, offset: int, limit: int) -> PaginatedResponse:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, user_id: int) -> User | None:
        raise NotImplementedError
