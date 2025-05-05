from pydantic import BaseModel
from uuid import UUID
from enum import Enum
from datetime import datetime


# Enum to represent the vote values
class VoteValue(str, Enum):
    up = "up"
    down = "down"


# Base schema: shared fields for Vote
class VoteBase(BaseModel):
    user_id: UUID
    vote_value: VoteValue


# Schema for creating a new Vote
class VoteCreate(VoteBase):
    pass


# Schema for updating a Vote
class VoteUpdate(VoteBase):
    pass


# Schema for a Vote response
class VoteOut(VoteBase):
    id: UUID
    target_id: UUID  # ID of the post or answer being voted on
    created_at: datetime

    class Config:
        orm_mode = True
