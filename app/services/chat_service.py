from sqlalchemy.ext.asyncio import AsyncSession

from api.schemas.chat import ChatCreate
from api.schemas.pagination import PaginatedResponse
from app.repositories.chat_repositoty import ChatRepository
from app.repositories.chat_message_repository import ChatMessageRepository
from app.api.schemas.chat import ChatMessageCreate, ChatMessageUpdate
from app.database.models.chat import Chat, ChatMessage
from app.core.exceptions.chat import ChatDoesNotExist


class ChatService:
    def __init__(self, db: AsyncSession) -> None:
        self.chat_repository = ChatRepository(db)
        self.message_repository = ChatMessageRepository(db)


    async def init_chat(self, current_user_id: int, target_user_id: int) -> Chat:
        chat_create = ChatCreate(first_user_id=current_user_id, second_user_id=target_user_id)
        return await self.chat_repository.create_chat(chat_create)


    async def delete_chat(self, chat_id: int, current_user_id: int) -> None:
        await self.chat_repository.delete_chat(chat_id, current_user_id)


    async def get_chats_by_user_id(self, current_user_id: int, offset: int, limit: int) -> PaginatedResponse:
        return await self.chat_repository.get_chats_by_user_id(current_user_id, offset, limit)


    async def get_chat_messages(self, chat_id: int, offset: int, limit: int) -> PaginatedResponse:
        return await self.message_repository.get_messages_by_chat_id(chat_id, offset, limit)


    async def create_message(self, message: ChatMessageCreate) -> ChatMessage | None:
        try:
            return await self.message_repository.create_message(message)
        except ChatDoesNotExist:
            # Инициализируем чат, если он не существует
            await self.init_chat(message.first_user_id, message.second_user_id)
            # Пытаемся снова создать сообщение
            return await self.message_repository.create_message(message)


    async def update_message(self, message: ChatMessageUpdate, current_user_id: int) -> ChatMessage:
        return await self.message_repository.update_message(message, current_user_id)


    async def delete_message(self, message_id: int, current_user_id: int) -> None:
        await self.message_repository.delete_message(message_id, current_user_id)
