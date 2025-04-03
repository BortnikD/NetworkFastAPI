from app.domain.entities.chat import Chat, ChatMessage
from app.domain.dto.chat import ChatCreate
from app.domain.dto.pagination import PaginatedResponse
from app.domain.dto.chat import ChatMessageCreate, ChatMessageUpdate
from app.domain.exceptions.base import AccessError
from app.domain.repositories.chat import IChat
from app.domain.repositories.chat_message import IChatMessage
from app.domain.repositories.redis import IRedis


class ChatService:
    def __init__(self, 
                 chat_port: IChat, 
                 chat_message_port: IChatMessage,
                 cache_port: IRedis
                 ) -> None:
        self.chat_port = chat_port
        self.chat_message_port = chat_message_port
        self.cache_port = cache_port
        self.cache_path = "cache.messages"

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

    async def get_chat_messages(self, user_id: int, chat_id: int, offset: int, limit: int) -> PaginatedResponse:
        if not await self.is_user_chat(user_id, chat_id):
            raise AccessError("You have not access to this chat")

        cache_messages = await self.cache_port.get_cache(f'{self.cache_path}:{chat_id}')
        if cache_messages:
            return PaginatedResponse(**cache_messages)
        else:
            messages = await self.chat_message_port.get_by_chat_id(chat_id, offset, limit)
            await self.cache_port.set_cache(f'{self.cache_path}:{chat_id}', messages)
            return messages


    async def create_message(self, message: ChatMessageCreate) -> ChatMessage | None:
        await self.cache_port.clear_cache(f'{self.cache_path}:{message.chat_id}')
        return await self.chat_message_port.save(message)

    async def update_message(self, message: ChatMessageUpdate, current_user_id: int) -> ChatMessage:
        if message.user_id != current_user_id:
            raise AccessError("You have not access to this chat")
        message = await self.chat_message_port.update(message, current_user_id)
        await self.cache_port.clear_cache(f'{self.cache_path}:{message.chat_id}')
        return message

    async def delete_message(self, message_id: int, current_user_id: int) -> None:
        message = await self.chat_message_port.get_message_by_id(message_id)
        if message.user_id != current_user_id:
            raise AccessError("You have not access to this message")
        await self.chat_message_port.delete(message.id, current_user_id)
        await self.cache_port.clear_cache(f'{self.cache_path}:{message.chat_id}')
