import logging
from fastapi import HTTPException
from sqlalchemy import func, or_
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.api.schemas.chat import ChatCreate
from app.database.models.chat import Chat
from app.adapters.api.schemas.pagination import PaginatedResponse
from app.core.utils.pages import get_prev_next_pages


class ChatRepository:
    def __init__(self, db: AsyncSession):
        self.db = db


    async def create_chat(self, chat: ChatCreate) -> Chat:
        new_chat = Chat(**chat.model_dump())
        self.db.add(new_chat)
        try:
            await self.db.commit()
            await self.db.refresh(new_chat)
            logging.info(f'Chat with id={new_chat.id} is created successfully')
            return new_chat
        except IntegrityError as e:
            await self.db.rollback()
            logging.error(f"Integrity error while creating chat: {str(e)}")
            raise HTTPException(status_code=400, detail="Error creating chat")


    async def get_chat_by_id(self, chat_id: int) -> Chat | None:
        chat = await self.db.get(Chat, chat_id)
        if not chat:
            logging.warning(f'Chat with id={chat_id} does not exist')
            raise HTTPException(status_code=404, detail="Chat does not exist")
        logging.info(f'Chat with id={chat_id} is found')
        return chat


    async def get_chats_by_user_id(self, user_id: int, offset: int, limit: int) -> PaginatedResponse:
        chat_filter = or_(Chat.first_user_id == user_id, Chat.second_user_id == user_id)

        count_result = await self.db.execute(select(func.count()).where(chat_filter))
        count = count_result.scalar()

        if count == 0:
            logging.warning(f'chats with user_id={user_id} is not found')
            return PaginatedResponse(count=count)

        chats = await self.db.execute(select(Chat)
                                      .where(chat_filter)
                                      .offset(offset)
                                      .limit(limit))
        chats = chats.scalars().all()

        prev_page, next_page = get_prev_next_pages(offset, limit, count, 'chats')

        logging.info(f'chats with user_id={user_id} is found')
        return PaginatedResponse(
            count=count,
            prev=prev_page,
            next=next_page,
            results=list(chats)
        )


    async def delete_chat(self, chat_id: int, current_user_id: int) -> None:
        chat = await self.db.get(Chat, chat_id)

        if current_user_id not in (chat.first_user_id, chat.second_user_id):
            logging.warning(f'user with id={current_user_id} tried to delete chat id={chat_id},'
                            f' but he is not a participant')
            raise HTTPException(status_code=403, detail='You have not access rights')

        if not chat:
            logging.warning(f'The user id={current_user_id} attempted to delete a non-existent chat.')
            raise HTTPException(status_code=404, detail="Chat does not exist")

        try:
            await self.db.delete(chat)
            await self.db.commit()
            logging.info(f'chat id={chat_id} deleted')
        except SQLAlchemyError as e:
            await self.db.rollback()
            logging.error(f'some error by delete chat with id={chat_id}, error = {e}')
            raise HTTPException(status_code=400, detail="error while deleting chat")