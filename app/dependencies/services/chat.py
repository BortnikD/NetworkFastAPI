from fastapi import Depends

from app.services.use_cases.chat_service import ChatService
from app.infrastructure.database.repositories.chat_repository import ChatRepository
from app.infrastructure.database.repositories.chat_message_repository import ChatMessageRepository
from app.infrastructure.database.repositories.redis_repository import RedisRepository
from app.infrastructure.database.redis import RedisClient
from app.dependencies.db import get_db


async def get_chat_service(db=Depends(get_db)) -> ChatService:
    chat_repo = ChatRepository(db)
    chat_message_repo = ChatMessageRepository(db)
    client = RedisClient()
    redis = await client.get_redis()
    redis_repo = RedisRepository(redis)
    return ChatService(chat_repo, chat_message_repo, redis_repo)