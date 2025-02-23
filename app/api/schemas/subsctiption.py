from pydantic import BaseModel
from datetime import datetime


class SubscriptionBase(BaseModel):
    follower_id: int
    followed_user_id: int

    class Config: 
        from_attributes = True


class SubscriptionPublic(SubscriptionBase):
    id: int
    created_at: datetime