import logging
from fastapi import HTTPException
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.utils.pages import get_prev_next_pages
from app.infrastructure.database.models import ChatMessage
from app.infrastructure.database.models import Chat
from app.adapters.api.schemas.chat import ChatMessageCreate, ChatMessageUpdate, ChatMessagePublic
from app.adapters.api.schemas.pagination import PaginatedResponse
from app.core.exceptions.chat import ChatDoesNotExist


class ChatMessageRepository:
    def __init__(self, db: AsyncSession):
        self.db = db


    async def create_message(self, message: ChatMessageCreate):
        chat = await self.db.get(Chat, message.chat_id)

        if not chat:
            logging.warning(f'Chat with id={message.chat_id} does not exist')
            raise ChatDoesNotExist("Chat does not exist")

        new_message = ChatMessage(
            user_id=message.first_user_id,
            chat_id=message.chat_id,
            text=message.text
        )
        self.db.add(new_message)

        try:
            await self.db.commit()
            await self.db.refresh(new_message)

            logging.info(f'Message with id={new_message.id} is created successfully')
            return new_message
        except IntegrityError as e:
            logging.error(f"Integrity error while creating message: {str(e)}")
            raise HTTPException(status_code=400, detail="Error creating message")


    async def get_messages_by_chat_id(self, chat_id: int, offset: int, limit: int) -> PaginatedResponse:
        count_result = await self.db.execute(select(func.count()).where(ChatMessage.chat_id == chat_id))
        count = count_result.scalar()
        if count == 0:
            logging.warning(f'messages with chat_id={chat_id} is not found')
            return PaginatedResponse(count=count)

        messages = await self.db.execute(select(ChatMessage)
                                         .where(ChatMessage.chat_id == chat_id)
                                         .offset(offset)
                                         .limit(limit))
        messages = messages.scalars().all()

        prev_page, next_page = get_prev_next_pages(offset, limit, count, 'messages')

        logging.info(f'messages with chat_id={chat_id} is found')
        return PaginatedResponse(
            count=count,
            prev=prev_page,
            next=next_page,
            results=[ChatMessagePublic.model_validate(message) for message in messages]
        )


    async def update_message(self, message: ChatMessageUpdate, current_user_id: int) -> ChatMessage:
        db_message = await self.db.get(ChatMessage, message.id)
        if not db_message:
            logging.warning(f'Message with id={message.id} does not exist')
            raise HTTPException(status_code=404, detail="Message does not exist")

        # Проверить права доступа
        if db_message.user_id != current_user_id:
            logging.warning(f'User with id={current_user_id} cannot update message id={message.id}')
            raise HTTPException(status_code=403, detail="You have no rights to update this message")

        # Проверить изменения
        if db_message.text == message.text:
            logging.info(f'Message with id={message.id} has no changes')
            return db_message

        db_message.text = message.text
        try:
            await self.db.commit()
            logging.info(f'Message with id={message.id} is updated successfully')
            return db_message
        except SQLAlchemyError as e:
            await self.db.rollback()  # Очистить транзакцию
            logging.error(f"Error updating message: {str(e)}")
            raise HTTPException(status_code=400, detail="Error updating message")


    async def delete_message(self, message_id: int, current_user_id: int) -> None:
        message = await self.db.get(ChatMessage, message_id)
        if not message:
            logging.warning(f'The user id={current_user_id} attempted to delete a non-existent message.')
            raise HTTPException(status_code=404, detail="Message does not exist")

        chat = message.chat
        if not chat:
            logging.warning(f'Chat for message id={message_id} does not exist')
            raise HTTPException(status_code=404, detail="Chat does not exist")

        if chat.first_user_id != current_user_id and chat.second_user_id != current_user_id:
            logging.warning(f'user with id={current_user_id} tried to delete message id={message_id}, '
                            f'but he is not a participant')
            raise HTTPException(status_code=403, detail='You have not access rights')

        try:
            await self.db.delete(message)
            await self.db.commit()
            logging.info(f'message id={message_id} deleted')
        except SQLAlchemyError as e:
            await self.db.rollback()
            logging.error(f'some error by delete message with id={message_id}, error = {e}')
            raise HTTPException(status_code=400, detail="error while deleting message")
