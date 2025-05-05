from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional

# Common fields
class CategoryBase(BaseModel):
    name: str
    description: Optional[str] = None


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
