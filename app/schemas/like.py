from pydantic import BaseModel
from datetime import datetime


class LikeBase(BaseModel):
    post_id: int


class LikeCreate(BaseModel):
    pass


class LikePublic(BaseModel):
    id: int
    user_id: int
    created_at: datetime

