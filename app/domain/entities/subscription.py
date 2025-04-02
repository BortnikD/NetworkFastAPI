from pydantic import BaseModel


class Subscription(BaseModel):
    id: int
    follower_id: int
    followed_user_id: int

    class Config:
        from_attributes = True