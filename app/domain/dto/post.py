from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class PostBase(BaseModel):
    text_content: str
    
    class Config: 
        from_attributes = True


class PostCreate(PostBase):
    user_id: int


class PostUpdate(PostBase):
    id: int
