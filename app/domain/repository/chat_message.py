from abc import ABC, abstractmethod

from app.domain.repository.entities.chat import ChatMessage
from app.domain.dto.chat import ChatMessageCreate
from app.domain.dto.pagination import PaginatedResponse
from app.domain.dto.chat import ChatMessageUpdate


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