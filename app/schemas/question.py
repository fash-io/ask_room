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
        from_attributes = True

class QuestionCreate(QuestionBase):
    pass

class Question(QuestionBase):
    id: UUID
    created_at: datetime
    updated_at: datetime
    view_count: int = 0  # Added view_count field

    class Config:
        from_attributes = True

class QuestionOut(Question):
    author: UserOut
    tags: List[TagOut]
    category: CategoryOut

    class Config:
        from_attributes = True

class PaginatedQuestions(BaseModel):
    total: int
    items: List[QuestionOut]
