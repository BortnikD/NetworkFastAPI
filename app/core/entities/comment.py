from dataclasses import dataclass


@dataclass
class Comment:
    id: int
    user_id: int
    post_id: int
    text_content: str
