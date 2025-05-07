from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from app.schemas.user import UserOut  
from app.schemas.vote import VoteOut

class AnswerBase(BaseModel):
    body: str
    question_id: UUID
    author_id: UUID 
    is_helpful: bool

    class Config:
        from_attributes = True

class AnswerCreate(AnswerBase):
    pass

class Answer(AnswerBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class AnswerOut(Answer):
    author: UserOut  
    votes: list[VoteOut]
    class Config:
        from_attributes = True
