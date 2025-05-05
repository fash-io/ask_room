from pydantic import BaseModel, constr
from uuid import UUID
from datetime import datetime

# Common fields
class CategoryBase(BaseModel):
    name: constr(min_length=1, max_length=50)

# For creation
class CategoryCreate(CategoryBase):
    pass

# For responses
class CategoryOut(CategoryBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

# For updating
class CategoryUpdate(CategoryBase):
    pass

class CategoryOutWithQuestions(CategoryOut):
    questions: list