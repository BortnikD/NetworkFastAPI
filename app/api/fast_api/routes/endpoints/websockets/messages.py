from fastapi import (
    APIRouter,
    Depends,
    WebSocket,
    WebSocketDisconnect
)

from app.domain.exceptions.chat import ChatDoesNotExist
from app.domain.exceptions.user import UserDoesNotExist
from app.domain.dto.chat import ChatMessageCreate

from app.dependencies.services.user import get_user_service
from app.dependencies.services.chat import get_chat_service

from app.services.core_services.chat_service import ChatService
from app.services.core_services.user_service import UserService

from app.api.fast_api.routes.endpoints.websockets.manager import websocket_manager

router = APIRouter()


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
