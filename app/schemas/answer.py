from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from app.schemas.user import UserOut  

class AnswerBase(BaseModel):
    body: str
    question_id: UUID
    author_id: UUID 

    class Config:
        orm_mode = True

class AnswerCreate(AnswerBase):
    pass

class Answer(AnswerBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class AnswerOut(Answer):
    author: UserOut  # nested author object
    upvotes: int
    downvotes: int

    class Config:
        orm_mode = True
