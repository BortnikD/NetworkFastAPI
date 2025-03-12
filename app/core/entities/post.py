from pydantic import BaseModel


class Post(BaseModel):
    id: int
    user_id: int
    text_content: str
    is_repost: bool = False