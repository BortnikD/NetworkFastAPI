from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

from app.adapters.api.schemas.chat import ChatCreate
from app.adapters.api.schemas.pagination import PaginatedResponse
from app.adapters.repositories.chat_repositoty import ChatRepository
from app.adapters.repositories.chat_message_repository import ChatMessageRepository
from app.adapters.api.schemas.chat import ChatMessageCreate, ChatMessageUpdate
from app.infrastructure.database.models.chat import Chat, ChatMessage
from app.core.exceptions.chat import ChatDoesNotExist


class ChatService:
    def __init__(self, db: AsyncSession) -> None:
        self.chat_repository = ChatRepository(db)
        self.message_repository = ChatMessageRepository(db)


    async def init_chat(self, current_user_id: int, target_user_id: int) -> Chat:
        chat_create = ChatCreate(first_user_id=current_user_id, second_user_id=target_user_id)
        return await self.chat_repository.create_chat(chat_create)


    async def is_user_chat(self, user_id: int, chat_id: int) -> bool:
        chat = await self.chat_repository.get_chat_by_id(chat_id)
        if not chat:
            return False
        return user_id in (chat.first_user_id, chat.second_user_id)


    async def delete_chat(self, chat_id: int, current_user_id: int) -> None:
        await self.chat_repository.delete_chat(chat_id, current_user_id)


    async def get_chats_by_user_id(self, current_user_id: int, offset: int, limit: int) -> PaginatedResponse:
        return await self.chat_repository.get_chats_by_user_id(current_user_id, offset, limit)


    async def get_chat_messages(self, user_id: int, chat_id: int, offset: int, limit: int) -> PaginatedResponse | None:
        if self.is_user_chat(user_id, chat_id):
            return await self.message_repository.get_messages_by_chat_id(chat_id, offset, limit)
        else:
            raise HTTPException(status_code=403, detail="You have no access rights")


    async def create_message(self, message: ChatMessageCreate) -> ChatMessage | None:
        try:
            return await self.message_repository.create_message(message)
        except ChatDoesNotExist:
            await self.init_chat(message.first_user_id, message.second_user_id)
            return await self.message_repository.create_message(message)


    async def update_message(self, message: ChatMessageUpdate, current_user_id: int) -> ChatMessage:
        return await self.message_repository.update_message(message, current_user_id)


    async def delete_message(self, message_id: int, current_user_id: int) -> None:
        await self.message_repository.delete_message(message_id, current_user_id)
