from dataclasses import dataclass


@dataclass
class CreateImage:
    user_id: int
    post_id: int
    src: str