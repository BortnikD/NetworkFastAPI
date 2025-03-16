from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

 
class UserBase(BaseModel):
    username: str
    email: EmailStr
    first_name: Optional[str] = None
    last_name: Optional[str]  = None

    class Config:
        from_attributes = True


class UserCreate(UserBase):
    password: str


class UserPublic(UserBase):
    id: int
    is_active: bool = False
    is_superuser: bool = False

