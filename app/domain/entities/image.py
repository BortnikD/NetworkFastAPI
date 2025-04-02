from pydantic import BaseModel


class Image(BaseModel):
    id: int
    user_id: int
    post_id: int
    src: str

    class Config:
        from_attributes = True
