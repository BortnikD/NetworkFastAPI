from dataclasses import dataclass


@dataclass
class Chat:
    id: int
    first_user_id: int
    second_user_id: int


@dataclass
class ChatMessage:
    id: int
    chat_id: int
    user_id: int
    text: str
