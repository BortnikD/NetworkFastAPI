from dataclasses import dataclass


@dataclass
class CreateSubscriptionDTO:
    follower_id: int
    followed_user_id: int


@dataclass
class GetSubscriptionDTO:
    id: int