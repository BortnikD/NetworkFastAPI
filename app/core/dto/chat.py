from pydantic import BaseModel
from datetime import datetime


class ChatBase(BaseModel):
    first_user_id: int
    second_user_id: int

    class Config:
        from_attributes = True


class ChatCreate(ChatBase):
    pass


class ChatPublic(ChatBase):
    id: int


class ChatMessageBase(BaseModel):
    text: str

    class Config:
        from_attributes = True


class ChatMessageCreateLite(ChatMessageBase):
    chat_id: int
    second_user_id: int


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
