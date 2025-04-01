from pydantic import BaseModel


class User(BaseModel):
    id: int
    username: str
    email: str
    password_hash: str
    first_name: str | None
    last_name: str | None