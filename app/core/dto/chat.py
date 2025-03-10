from dataclasses import dataclass


@dataclass
class CreateChatDTO:
    first_user_id: int
    second_user_id: int


@dataclass
class GetChatDTO:
    id: int


@dataclass
class CreateChatMessageDTO:
    chat_id: int
    user_id: int
    text: str


@dataclass
class GetChatMessageDTO:
    id: int


@dataclass
class UpdateChatMessageDTO:
    id: int
    text: str