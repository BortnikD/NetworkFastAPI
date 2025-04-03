import logging

from sqlalchemy import func
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.chat import ChatMessage as ChatMessageEntity
from app.domain.dto.chat import ChatMessageCreate, ChatMessageUpdate
from app.domain.dto.pagination import PaginatedResponse
from app.domain.repositories.chat_message import IChatMessage
from app.domain.exceptions.base import AccessError
from app.domain.exceptions.chat import (
    ChatDoesNotExist,
    MessageCreateError,
    MessageDoesNotExist,
    MessageUpdateError,
    MessageDeleteError
)

from app.infrastructure.database.repositories.utils.pages import get_prev_next_pages
from app.infrastructure.database.models import ChatMessage as ChatMessageModel, Chat as ChatModel


class ChatMessageRepository(IChatMessage):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def save(self, message: ChatMessageCreate) -> ChatMessageEntity:
        chat = await self.db.get(ChatModel, message.chat_id)
        if not chat:
            logging.warning(f"Чат с id={message.chat_id} не существует")
            raise ChatDoesNotExist("Чат не существует")

        new_message = ChatMessageModel(**message.model_dump())
        self.db.add(new_message)

        try:
            await self.db.commit()
            await self.db.refresh(new_message)
            logging.info(f"Сообщение с id={new_message.id} успешно создано")
            return ChatMessageEntity.model_validate(new_message)
        except IntegrityError as e:
            logging.error(f"Ошибка целостности при создании сообщения: {str(e)}")
            raise MessageCreateError("Ошибка при создании сообщения")

    async def get_by_chat_id(self, chat_id: int, offset: int, limit: int) -> PaginatedResponse:
        count_result = await self.db.execute(select(func.count()).where(ChatMessageModel.chat_id == chat_id))
        count = count_result.scalar()
        if count == 0:
            logging.warning(f"Сообщения с chat_id={chat_id} не найдены")
            return PaginatedResponse(count=count)

        messages_result = await self.db.execute(
            select(ChatMessageModel)
            .where(ChatMessageModel.chat_id == chat_id)
            .offset(offset)
            .limit(limit)
        )
        messages = messages_result.scalars().all()

        prev_page, next_page = get_prev_next_pages(offset, limit, count, 'messages')
        logging.info(f"Сообщения с chat_id={chat_id} найдены")
        return PaginatedResponse(
            count=count,
            prev=prev_page,
            next=next_page,
            results=[ChatMessageEntity.model_validate(message) for message in messages]
        )

    async def get_message_by_id(self, message_id: int) -> ChatMessageEntity:
        message = await self.db.get(ChatMessageModel, message_id)
        if not message:
            logging.warning(f"Сообщение с id={message_id} не найдено")
            raise MessageDoesNotExist("Сообщение не существует")

        logging.info(f"Сообщение с id={message_id} найдено")
        return ChatMessageEntity.model_validate(message)

    async def update(self, message: ChatMessageUpdate, current_user_id: int) -> ChatMessageEntity:
        db_message = await self.db.get(ChatMessageModel, message.id)
        if not db_message:
            logging.warning(f"Сообщение с id={message.id} не существует")
            raise MessageDoesNotExist("Сообщение не существует")

        if db_message.sender_id != current_user_id:
            logging.warning(f"Пользователь с id={current_user_id} не может обновить сообщение id={message.id}")
            raise AccessError("У вас нет прав для обновления этого сообщения")

        if db_message.text == message.text:
            logging.info(f"Сообщение с id={message.id} без изменений")
            return ChatMessageEntity.model_validate(db_message)

        db_message.text = message.text
        try:
            await self.db.commit()
            logging.info(f"Сообщение с id={message.id} успешно обновлено")
            return ChatMessageEntity.model_validate(db_message)
        except SQLAlchemyError as e:
            await self.db.rollback()
            logging.error(f"Ошибка при обновлении сообщения: {str(e)}")
            raise MessageUpdateError("Ошибка при обновлении сообщения")

    async def delete(self, message_id: int, current_user_id: int) -> None:
        message = await self.db.get(ChatMessageModel, message_id)
        if not message:
            logging.warning(f"Пользователь с id={current_user_id} попытался удалить несуществующее сообщение")
            raise MessageDoesNotExist("Сообщение не существует")

        try:
            await self.db.delete(message)
            await self.db.commit()
            logging.info(f"Сообщение с id={message_id} удалено")
        except SQLAlchemyError as e:
            await self.db.rollback()
            logging.error(f"Ошибка при удалении сообщения с id={message_id}: {e}")
            raise MessageDeleteError("Ошибка при удалении сообщения")
