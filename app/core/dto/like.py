from pydantic import BaseModel
from datetime import datetime


class LikeBase(BaseModel):
    post_id: int


class LikeCreate(LikeBase):
    pass


class LikePublic(LikeBase):
    id: int
    user_id: int
    created_at: datetime

