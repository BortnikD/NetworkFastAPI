from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

from app.services.chat_service import ChatService
from app.api.dependencies.auth import get_current_active_user
from app.api.dependencies.db import get_db
from app.api.schemas.chat import ChatMessageCreateLite, ChatMessageCreate, ChatMessagePublic
from app.api.schemas.pagination import PaginatedResponse, MessagePagination
from app.database.models import User

router = APIRouter(
    prefix='/messages'
)


@router.post('/', response_model=ChatMessagePublic)
async def send_message(message: ChatMessageCreateLite,
                       db: AsyncSession = Depends(get_db),
                       current_user: User = Depends(get_current_active_user)):
    service = ChatService(db)
    full_message_data = {**message.model_dump(), "first_user_id": current_user.id}
    full_message = ChatMessageCreate(**full_message_data)
    return await service.create_message(full_message)


@router.get('/{chat_id}')
async def get_messages(chat_id: int,
                       pagination: Annotated[MessagePagination, Query()],
                       db: AsyncSession = Depends(get_db),
                       current_user: User =  Depends(get_current_active_user)
                      ) -> PaginatedResponse:
    service = ChatService(db)
    return await service.get_chat_messages(current_user.id, chat_id, pagination.offset, pagination.limit)