from dataclasses import dataclass


@dataclass
class Post:
    id: int
    user_id: int
    text_content: str
    is_repost: bool = False