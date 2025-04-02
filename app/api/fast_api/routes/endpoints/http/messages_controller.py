from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
    Path,
    Query,
    HTTPException
)

from app.domain.exceptions.base import AccessError
from app.domain.exceptions.chat import (
    ChatDoesNotExist,
    ChatAlreadyExists,
    MessageDeleteError,
    MessageDoesNotExist,
    MessageUpdateError
)
from app.domain.dto.chat import ChatMessageUpdate
from app.domain.dto.pagination import PaginatedResponse, MessagePagination
from app.domain.entities.chat import Chat, ChatMessage

from app.dependencies.auth import get_current_user
from app.dependencies.services.chat import get_chat_service
from app.services.core_services.chat_service import ChatService
from app.infrastructure.database.models import User

router = APIRouter(prefix='/messages')


@router.post('/start_chat/{target_user_id}')
async def start_chat(target_user_id: Annotated[int, Path(gt=0)],
                     user: User = Depends(get_current_user),
                     service: ChatService = Depends(get_chat_service)
                     ) -> Chat:
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
    except AccessError as e:
        raise HTTPException(status_code=403, detail=e.message)


@router.delete('/delete_chat/{chat_id}')
async def delete_chat(chat_id: int,
                      user: User = Depends(get_current_user),
                      message_service: ChatService = Depends(get_chat_service)
                      ) -> None:
    try:
        await message_service.delete_chat(user.id, chat_id)
    except ChatDoesNotExist as e:
        raise HTTPException(status_code=404, detail=e.message)
    except AccessError as e:
        raise HTTPException(status_code=403, detail=e.message)
    except MessageDeleteError as e:
        raise HTTPException(status_code=400, detail=e.message)


@router.patch('/update_message/{message_id}')
async def update_message(message: ChatMessageUpdate,
                         user: User = Depends(get_current_user),
                         message_service: ChatService = Depends(get_chat_service)
                         ) -> ChatMessage:
    try:
        return await message_service.update_message(message, user.id)
    except MessageDoesNotExist as e:
        raise HTTPException(status_code=404, detail=e.message)
    except AccessError as e:
        raise HTTPException(status_code=403, detail=e.message)
    except MessageUpdateError as e:
        raise HTTPException(status_code=400, detail=e.message)


@router.delete('/delete_message/{message_id}')
async def delete_message(message_id: int,
                         user: User = Depends(get_current_user),
                         message_service: ChatService = Depends(get_chat_service)
                         ) -> None:
    try:
        await message_service.delete_message(message_id, user.id)
    except MessageDoesNotExist as e:
        raise HTTPException(status_code=404, detail=e.message)
    except AccessError as e:
        raise HTTPException(status_code=403, detail=e.message)
    except MessageDeleteError as e:
        raise HTTPException(status_code=400, detail=e.message)