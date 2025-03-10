import logging
from fastapi import HTTPException
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.repositories.utils.pages import get_prev_next_pages
from app.infrastructure.database.models import ChatMessage, Chat
from app.core.dto.chat import ChatMessageCreate, ChatMessageUpdate, ChatMessagePublic
from app.core.dto.pagination import PaginatedResponse
from app.core.exceptions.chat import ChatDoesNotExist
from app.core.interfaces.chat_message import IChatMessage


class ChatMessageRepository(IChatMessage):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def save(self, message: ChatMessageCreate) -> ChatMessage | None:
        chat = await self.db.get(Chat, message.chat_id)
        if not chat:
            logging.warning(f"Чат с id={message.chat_id} не существует")
            raise ChatDoesNotExist("Чат не существует")

        new_message = ChatMessage(
            user_id=message.first_user_id,
            chat_id=message.chat_id,
            text=message.text
        )
        self.db.add(new_message)

        try:
            await self.db.commit()
            await self.db.refresh(new_message)
            logging.info(f"Сообщение с id={new_message.id} успешно создано")
            return new_message
        except IntegrityError as e:
            logging.error(f"Ошибка целостности при создании сообщения: {str(e)}")
            raise HTTPException(status_code=400, detail="Ошибка при создании сообщения")

    async def get_by_chat_id(self, chat_id: int, offset: int, limit: int) -> PaginatedResponse:
        count_result = await self.db.execute(select(func.count()).where(ChatMessage.chat_id == chat_id))
        count = count_result.scalar()
        if count == 0:
            logging.warning(f"Сообщения с chat_id={chat_id} не найдены")
            return PaginatedResponse(count=count)

        messages_result = await self.db.execute(
            select(ChatMessage)
            .where(ChatMessage.chat_id == chat_id)
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
            results=[ChatMessagePublic.model_validate(message) for message in messages]
        )

    async def update(self, message: ChatMessageUpdate, current_user_id: int) -> ChatMessage:
        db_message = await self.db.get(ChatMessage, message.id)
        if not db_message:
            logging.warning(f"Сообщение с id={message.id} не существует")
            raise HTTPException(status_code=404, detail="Сообщение не существует")

        # Проверка прав доступа
        if db_message.user_id != current_user_id:
            logging.warning(f"Пользователь с id={current_user_id} не может обновить сообщение id={message.id}")
            raise HTTPException(status_code=403, detail="У вас нет прав для обновления этого сообщения")

        # Проверка изменений
        if db_message.text == message.text:
            logging.info(f"Сообщение с id={message.id} без изменений")
            return db_message

        db_message.text = message.text
        try:
            await self.db.commit()
            logging.info(f"Сообщение с id={message.id} успешно обновлено")
            return db_message
        except SQLAlchemyError as e:
            await self.db.rollback()
            logging.error(f"Ошибка при обновлении сообщения: {str(e)}")
            raise HTTPException(status_code=400, detail="Ошибка при обновлении сообщения")

    async def delete(self, message_id: int, current_user_id: int) -> None:
        message = await self.db.get(ChatMessage, message_id)
        if not message:
            logging.warning(f"Пользователь с id={current_user_id} попытался удалить несуществующее сообщение")
            raise HTTPException(status_code=404, detail="Сообщение не существует")

        chat = message.chat
        if not chat:
            logging.warning(f"Чат для сообщения с id={message_id} не существует")
            raise HTTPException(status_code=404, detail="Чат не существует")

        if chat.first_user_id != current_user_id and chat.second_user_id != current_user_id:
            logging.warning(f"Пользователь с id={current_user_id} не является участником чата для сообщения id={message_id}")
            raise HTTPException(status_code=403, detail="У вас нет прав доступа")

        try:
            await self.db.delete(message)
            await self.db.commit()
            logging.info(f"Сообщение с id={message_id} удалено")
        except SQLAlchemyError as e:
            await self.db.rollback()
            logging.error(f"Ошибка при удалении сообщения с id={message_id}: {e}")
            raise HTTPException(status_code=400, detail="Ошибка при удалении сообщения")
