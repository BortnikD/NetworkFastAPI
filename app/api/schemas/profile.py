from pydantic import BaseModel, EmailStr
from typing import Optional

from app.api.schemas.user import UserPublic


class ProfilePublic(UserPublic):
    followers_count: int
    followed_count: int