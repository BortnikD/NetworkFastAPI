from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
    Path,
    Query,
    HTTPException
)

from app.domain.exceptions.chat import ChatDoesNotExist, ChatAlreadyExists
from app.domain.dto.chat import  ChatMessagePublic
from app.domain.dto.pagination import PaginatedResponse, MessagePagination

from app.dependencies.auth import get_current_user
from app.dependencies.services.chat import get_chat_service

from app.services.core_services.chat_service import ChatService

from app.infrastructure.database.models import User

router = APIRouter(prefix='/messages')


@router.post('/start_chat/{target_user_id}', response_model=ChatMessagePublic)
async def start_chat(target_user_id: Annotated[int, Path(gt=0)],
                     user: User = Depends(get_current_user),
                     service: ChatService = Depends(get_chat_service)):
    try:
        return await service.init_chat(user.id, target_user_id)
    except ChatAlreadyExists as e:
        raise HTTPException(status_code=409, detail=e.message)


@router.get("/my_chats")
async def get_my_chats(pagination: Annotated[MessagePagination, Query()],
                       user: User = Depends(get_current_user),
                       message_service: ChatService = Depends(get_chat_service),
                       ) -> PaginatedResponse:
    return await message_service.get_chats_by_user_id(user.id, pagination.offset, pagination.limit)


@router.get('/chats_history/{chat_id}')
async def get_chat_history(chat_id: int,
                           pagination: Annotated[MessagePagination, Query()],
                           user: User = Depends(get_current_user),
                           message_service: ChatService = Depends(get_chat_service)
                           ) -> PaginatedResponse:
    try:
        return await message_service.get_chat_messages(user.id, chat_id, pagination.offset, pagination.limit)
    except ChatDoesNotExist as e:
        raise HTTPException(status_code=404, detail=e.message)