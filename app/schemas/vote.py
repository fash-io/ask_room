from pydantic import BaseModel
from uuid import UUID
import enum


class VoteValue(enum.Enum):
    down = -1
    up = 1


class VoteCreate(BaseModel):
    question_id: UUID
    answer_id: UUID
    vote_value: VoteValue

    class Config:
        orm_mode = True
        
