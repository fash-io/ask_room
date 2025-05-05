from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import List, Optional
from app.schemas.user import UserOut
from app.schemas.tag import TagOut
from app.schemas.category import CategoryOut

class QuestionBase(BaseModel):
    title: str
    body: str
    images: Optional[str] = None
    category_id: UUID
    author_id: UUID
    tags: Optional[List[UUID]] = []

    class Config:
        orm_mode = True

class QuestionCreate(QuestionBase):
    pass

class Question(QuestionBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class QuestionOut(Question):
    author: UserOut
    tags: List[TagOut]
    category: CategoryOut

    class Config:
        orm_mode = True
