from fastapi import HTTPException

from app.core.dto.chat import ChatCreate
from app.core.dto.pagination import PaginatedResponse
from app.core.interfaces.chat import IChat
from app.core.interfaces.chat_message import IChatMessage
from app.core.dto.chat import ChatMessageCreate, ChatMessageUpdate
from app.infrastructure.database.models.chat import Chat, ChatMessage
from app.core.exceptions.chat import ChatDoesNotExist


class ChatService:
    def __init__(self, chat_port: IChat, chat_message_port: IChatMessage) -> None:
        self.chat_port = chat_port
        self.chat_message_port = chat_message_port


    async def init_chat(self, current_user_id: int, target_user_id: int) -> Chat:
        chat_create = ChatCreate(first_user_id=current_user_id, second_user_id=target_user_id)
        return await self.chat_port.save(chat_create)


    async def is_user_chat(self, user_id: int, chat_id: int) -> bool:
        chat = await self.chat_port.get_by_id(chat_id)
        if not chat:
            return False
        return user_id in (chat.first_user_id, chat.second_user_id)


    async def delete_chat(self, chat_id: int, current_user_id: int) -> None:
        await self.chat_port.delete(chat_id, current_user_id)


    async def get_chats_by_user_id(self, current_user_id: int, offset: int, limit: int) -> PaginatedResponse:
        return await self.chat_port.get_all_by_user_id(current_user_id, offset, limit)


    async def get_chat_messages(self, user_id: int, chat_id: int, offset: int, limit: int) -> PaginatedResponse | None:
        if self.is_user_chat(user_id, chat_id):
            return await self.chat_message_port.get_by_chat_id(chat_id, offset, limit)
        else:
            raise HTTPException(status_code=403, detail="You have no access rights")


    async def create_message(self, message: ChatMessageCreate) -> ChatMessage | None:
        try:
            return await self.chat_message_port.save(message)
        except ChatDoesNotExist:
            await self.init_chat(message.first_user_id, message.second_user_id)
            return await self.chat_message_port.save(message)


    async def update_message(self, message: ChatMessageUpdate, current_user_id: int) -> ChatMessage:
        return await self.chat_message_port.update(message, current_user_id)


    async def delete_message(self, message_id: int, current_user_id: int) -> None:
        await self.chat_message_port.delete(message_id, current_user_id)
