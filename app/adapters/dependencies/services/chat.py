from fastapi import Depends

from app.core.services.chat_service import ChatService
from app.adapters.repositories.chat_repositoty import ChatRepository
from app.adapters.repositories.chat_message_repository import ChatMessageRepository
from app.adapters.dependencies.db import get_db


def get_chat_service(db=Depends(get_db)) -> ChatService:
    chat_repo = ChatRepository(db)
    chat_message_repo = ChatMessageRepository(db)
    return ChatService(chat_repo, chat_message_repo)