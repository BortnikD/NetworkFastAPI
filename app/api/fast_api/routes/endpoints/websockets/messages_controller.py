from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
    Path,
    Query,
    WebSocket,
    WebSocketDisconnect,
    HTTPException
)

from app.domain.exceptions.chat import ChatDoesNotExist, ChatAlreadyExists
from app.domain.exceptions.user import UserDoesNotExist
from app.domain.dto.chat import ChatMessageCreate, ChatMessagePublic
from app.domain.dto.pagination import PaginatedResponse, MessagePagination

from app.dependencies.auth import get_current_user
from app.dependencies.services.user import get_user_service
from app.dependencies.services.chat import get_chat_service

from app.services.core_services.chat_service import ChatService
from app.services.core_services.user_service import UserService

from app.infrastructure.database.models import User
from app.api.fast_api.routes.endpoints.websockets.manager import websocket_manager

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
                           user: User = Depends(get_current_user),
                           message_service: ChatService = Depends(get_chat_service)
                           ) -> PaginatedResponse:
    try:
        return await message_service.get_chat_messages(user.id, chat_id)
    except ChatDoesNotExist as e:
        raise HTTPException(status_code=404, detail=e.message)


@router.websocket('/')
async def send_message(websocket: WebSocket,
                       user_service: UserService = Depends(get_user_service),
                       message_service: ChatService = Depends(get_chat_service)):
    token = websocket.query_params.get("token")
    chat_id = int(websocket.query_params.get("chat_id"))
    if not token or not chat_id:
        await websocket.close(code=1008)
        return

    try:
        user = await user_service.get_by_token(token)
    except UserDoesNotExist:
        await websocket.close(code=1008)
        return

    await websocket_manager.connect(websocket, chat_id, user.id)

    try:
        while True:
            data = await websocket.receive_text()
            await websocket_manager.broadcast(data, chat_id, user.id)
            message = ChatMessageCreate(chat_id=chat_id,
                                        sender_id=user.id,
                                        text=data)
            try:
                await message_service.create_message(message)
            except ChatDoesNotExist:
                await websocket.close(code=1008)
    except WebSocketDisconnect:
        websocket_manager.disconnect(chat_id, user.id)
