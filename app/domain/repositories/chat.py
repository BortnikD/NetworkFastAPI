from abc import abstractmethod, ABC

from app.domain.dto.pagination import PaginatedResponse
from app.domain.entities.chat import Chat
from app.domain.dto.chat import ChatCreate


class IChat(ABC):
    @abstractmethod
    async def save(self, chat: ChatCreate) -> Chat:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, chat_id: int) -> Chat | None:
        raise NotImplementedError

    @abstractmethod
    async def get_all_by_user_id(self, user_id: int, offset: int, limit: int) -> PaginatedResponse:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, chat_id: int, current_user_id: int) -> None:
        raise NotImplementedError