from dataclasses import dataclass


@dataclass
class CreateLikeDTO:
    user_id: int
    post_id: int


@dataclass
class GetLikeDTO:
    id: int