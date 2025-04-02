from pydantic import BaseModel


class ChatBase(BaseModel):
    first_user_id: int
    second_user_id: int

    class Config:
        from_attributes = True


class ChatCreate(ChatBase):
    pass


class ChatMessageBase(BaseModel):
    text: str

    class Config:
        from_attributes = True


class ChatMessageCreate(ChatMessageBase):
    chat_id: int
    sender_id: int


class ChatMessageUpdate(ChatMessageBase):
    id: int


