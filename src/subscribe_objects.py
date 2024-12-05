from pydantic import BaseModel
from typing import List

class Subscriber(BaseModel):
    user_email: str
    user_destination: List[str]
    sunny_threshold: List[int]
    time_window: List[int]
    num_allowed_destination: int = 3

class Subscription(BaseModel):
    email: str
    # location1: str
    # location2: str | None = None
    # location3: str | None = None
    locations: List[str]
    sunny_threshold: int = 2
    time_window: int = 7 