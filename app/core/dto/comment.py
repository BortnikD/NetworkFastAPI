from dataclasses import dataclass


@dataclass
class CreateCommentDTO:
    user_id: int
    post_id: int
    text_content: str


@dataclass
class UpdateCommentDTO:
    id: int
    text_content: str


@dataclass
class GetCommentsDTO:
    post_id: int