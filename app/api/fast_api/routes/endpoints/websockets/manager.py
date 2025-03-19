from fastapi import WebSocket


class WebsocketManager:
    def __init__(self):
        self.active_connections: dict[int, dict[int, WebSocket]] = {}

    async def connect(self, websocket: WebSocket, chat_id: int, user_id: int):
        await websocket.accept()
        if chat_id not in self.active_connections:
            self.active_connections[chat_id] = {}
        self.active_connections[chat_id][user_id] = websocket

    def disconnect(self, chat_id: int, user_id: int):
        if chat_id in self.active_connections and user_id in self.active_connections[chat_id]:
            del self.active_connections[chat_id][user_id]
            if not self.active_connections[chat_id]:
                del self.active_connections[chat_id]

    async def broadcast(self, message: str, chat_id: int, sender_id: int):
        if chat_id in self.active_connections:
            for user_id, connection in self.active_connections[chat_id].items():
                message_with_class = {
                    "text": message,
                    "sender_id": sender_id,
                }
                await connection.send_json(message_with_class)


websocket_manager = WebsocketManager()