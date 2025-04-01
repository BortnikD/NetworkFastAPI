from pydantic import BaseModel


class Comment(BaseModel):
    id: int
    user_id: int
    post_id: int
    text_content: str
