import logging

from sqlalchemy import func, or_
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.exceptions.base import AccessError
from app.domain.repository.chat import IChat
from app.domain.dto.chat import ChatCreate
from app.domain.dto.pagination import PaginatedResponse
from app.domain.exceptions.chat import (
    ChatCreateError,
    ChatDoesNotExist,
    MessageDeleteError,
)

from app.infrastructure.database.models.chat import Chat
from app.infrastructure.database.repositories.utils.pages import get_prev_next_pages



class ChatRepository(IChat):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def save(self, chat: ChatCreate) -> Chat:
        new_chat = Chat(**chat.model_dump())
        self.db.add(new_chat)
        try:
            await self.db.commit()
            await self.db.refresh(new_chat)
            logging.info(f"Чат с id={new_chat.id} успешно создан")
            return new_chat
        except IntegrityError as e:
            await self.db.rollback()
            logging.error(f"Ошибка целостности при создании чата: {str(e)}")
            raise ChatCreateError("Ошибка при создании чата")

    async def get_by_id(self, chat_id: int) -> Chat | None:
        chat = await self.db.get(Chat, chat_id)
        if not chat:
            logging.warning(f"Чат с id={chat_id} не существует")
            raise ChatDoesNotExist("Чат не существует")
        logging.info(f"Чат с id={chat_id} найден")
        return chat

    async def get_all_by_user_id(self, user_id: int, offset: int, limit: int) -> PaginatedResponse:
        chat_filter = or_(Chat.first_user_id == user_id, Chat.second_user_id == user_id)

        count_result = await self.db.execute(select(func.count()).where(chat_filter))
        count = count_result.scalar()

        if count == 0:
            logging.warning(f"Чаты с user_id={user_id} не найдены")
            return PaginatedResponse(count=count)

        chats_result = await self.db.execute(
            select(Chat)
            .where(chat_filter)
            .offset(offset)
            .limit(limit)
        )
        chats = chats_result.scalars().all()

        prev_page, next_page = get_prev_next_pages(offset, limit, count, "chats")

        logging.info(f"Чаты с user_id={user_id} найдены")
        return PaginatedResponse(
            count=count,
            prev=prev_page,
            next=next_page,
            results=list(chats),
        )

    async def delete(self, chat_id: int, current_user_id: int) -> None:
        chat = await self.db.get(Chat, chat_id)

        if not chat:
            logging.warning(f"Пользователь id={current_user_id} попытался удалить несуществующий чат")
            raise ChatDoesNotExist("Чат не существует")

        if current_user_id not in (chat.first_user_id, chat.second_user_id):
            logging.warning(f"Пользователь id={current_user_id} пытался удалить чат id={chat_id}, но не является его участником")
            raise AccessError("У вас нет прав доступа")

        try:
            await self.db.delete(chat)
            await self.db.commit()
            logging.info(f"Чат с id={chat_id} удален")
        except SQLAlchemyError as e:
            await self.db.rollback()
            logging.error(f"Ошибка при удалении чата с id={chat_id}: {e}")
            raise MessageDeleteError("Ошибка при удалении чата")
