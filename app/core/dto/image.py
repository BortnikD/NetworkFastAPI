from pydantic import BaseModel
from datetime import datetime


class Image(BaseModel):
    id: int
    user_id: int
    post_id: int
    src: str
    created_at: datetime
