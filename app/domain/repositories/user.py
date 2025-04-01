from abc import ABC, abstractmethod

from app.domain.dto.pagination import PaginatedResponse
from app.domain.entities import User
from app.domain.dto.user import UserCreate


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
