from dataclasses import dataclass


@dataclass
class CreateUserDTO:
    username: str
    email: str
    password: str
    first_name: str | None = None
    last_name: str | None = None


@dataclass
class GetUserDTO:
    id: int | None