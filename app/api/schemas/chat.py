from pydantic import BaseModel
from datetime import datetime


class ChatBase(BaseModel):
    first_user_id: int
    second_user_id: int


class ChatCreate(ChatBase):
    pass


class ChatPublic(ChatBase):
    id: int


class ChatMessageBase(BaseModel):
    text: str


class ChatMessageCreate(ChatMessageBase):
    chat_id: int
    first_user_id: int
    second_user_id: int


class ChatMessageUpdate(ChatMessageBase):
    id: int


class ChatMessagePublic(ChatMessageBase):
    id: int
    chat_id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
