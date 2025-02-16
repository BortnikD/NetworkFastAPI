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


class UserDB(UserBase):
    id: int
    password_hash: str
    date_joined: datetime
    last_active_time: datetime
    is_active: bool = False


class UserPublic(UserBase):
    id: int
    is_active: bool = False


class UserIn(UserBase):
    password: str