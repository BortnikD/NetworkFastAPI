from pydantic import BaseModel, EmailStr
from typing import Optional

from app.domain.entities.user import User

 
class UserBase(BaseModel):
    username: str
    email: EmailStr
    first_name: Optional[str] = None
    last_name: Optional[str]  = None

    class Config:
        from_attributes = True


class UserCreate(UserBase):
    password: str


class UserDB(User):
    password_hash: str
