from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class PostBase(BaseModel):
    text_content: str
    
    class Config: 
        from_attributes = True


class PostCreate(PostBase):
    user_id: int

 
class PostPublic(PostBase):
    id: int
    user_id: int
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    is_repost: Optional[bool] 


class PostUpdate(PostBase):
    id: int
