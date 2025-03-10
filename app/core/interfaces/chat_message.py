from abc import ABC, abstractmethod

from app.core.entities.chat import ChatMessage
from app.core.dto.chat import ChatMessageCreate
from app.core.dto.pagination import PaginatedResponse
from app.core.dto.chat import ChatMessageUpdate


class IChatMessage(ABC):
    @abstractmethod
    async def save(self, message: ChatMessageCreate) -> ChatMessage | None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_chat_id(self, chat_id: int, offset: int, limit: int) -> PaginatedResponse:
        raise NotImplementedError

    @abstractmethod
    async def update(self, message: ChatMessageUpdate, current_user_id: int) -> ChatMessage:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, message_id: int, current_user_id: int) -> None:
        raise NotImplementedError