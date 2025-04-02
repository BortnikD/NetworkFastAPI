from datetime import datetime

from pydantic import BaseModel


class Chat(BaseModel):
    id: int
    first_user_id: int
    second_user_id: int

    class Config:
        from_attributes = True


class ChatMessage(BaseModel):
    id: int
    chat_id: int
    user_id: int
    text: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True