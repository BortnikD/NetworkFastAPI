from pydantic import BaseModel
from datetime import datetime


class ChatBase(BaseModel):
    first_user_id: int
    second_user_id: int


class ChatCreate(ChatBase):
    pass


class ChatPublic(ChatBase):
    id: int


class ChatMessage(BaseModel):
    id: int
    chat_id: int
    user_id: int
    text: str
    created_at: datetime
    updated_at: datetime