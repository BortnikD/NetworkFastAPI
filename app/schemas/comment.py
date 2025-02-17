from pydantic import BaseModel
from datetime import datetime


class CommentBase(BaseModel):
    text_content: str

    class Config: 
        from_attributes = True


class CommentCreate(CommentBase):
    post_id: int


class CommentUpdate(CommentBase):
    id: int


class CommentPublic(CommentBase):
    id: int
    user_id: int
    post_id: int
    created_at: datetime
    is_repost: bool = False
    