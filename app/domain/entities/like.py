from pydantic import BaseModel


class Like(BaseModel):
    id: int
    user_id: int
    post_id: int

    class Config:
        from_attributes = True