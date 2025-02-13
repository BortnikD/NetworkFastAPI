from pydantic import BaseModel
import datetime


class CommentBase(BaseModel):
    text_content: str

    class Config: 
        from_attributes = True


class CommentDB(CommentBase):
    id: int
    user_id: int
    created_at: datetime


class CommentCreate(CommentBase):
    pass


class CommentPublic(CommentBase):
    id: int
    