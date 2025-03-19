from fastapi import Depends

from app.services.core_services.chat_service import ChatService
from app.infrastructure.database.repositories.chat_repository import ChatRepository
from app.infrastructure.database.repositories.chat_message_repository import ChatMessageRepository
from app.dependencies.db import get_db


def get_chat_service(db=Depends(get_db)) -> ChatService:
    chat_repo = ChatRepository(db)
    chat_message_repo = ChatMessageRepository(db)
    return ChatService(chat_repo, chat_message_repo)