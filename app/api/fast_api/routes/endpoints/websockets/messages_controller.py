from fastapi import APIRouter, Depends, Query
from typing import Annotated

from app.services.core_services.chat_service import ChatService
from app.dependencies.services.chat import get_chat_service
from app.dependencies.auth import get_current_active_user
from app.domain.dto.chat import ChatMessageCreateLite, ChatMessageCreate, ChatMessagePublic
from app.domain.dto.pagination import PaginatedResponse, MessagePagination
from app.infrastructure.database.models import User

router = APIRouter(
    prefix='/messages'
)


@router.post('/', response_model=ChatMessagePublic)
async def send_message(message: ChatMessageCreateLite,
                       service: ChatService = Depends(get_chat_service),
                       current_user: User = Depends(get_current_active_user)):
    full_message_data = {**message.model_dump(), "first_user_id": current_user.id}
    full_message = ChatMessageCreate(**full_message_data)
    return await service.create_message(full_message)


@router.get('/{chat_id}')
async def get_messages(chat_id: int,
                       pagination: Annotated[MessagePagination, Query()],
                       service: ChatService = Depends(get_chat_service),
                       current_user: User =  Depends(get_current_active_user)
                      ) -> PaginatedResponse:
    return await service.get_chat_messages(current_user.id, chat_id, pagination.offset, pagination.limit)