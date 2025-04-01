from pydantic import BaseModel
from datetime import datetime


class LikeBase(BaseModel):
    post_id: int


class LikeCreate(LikeBase):
    pass


