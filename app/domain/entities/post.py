from datetime import datetime

from pydantic import BaseModel


class Post(BaseModel):
    id: int
    user_id: int
    text_content: str
    is_repost: bool = False
    created_at: datetime | None
    updated_at: datetime | None