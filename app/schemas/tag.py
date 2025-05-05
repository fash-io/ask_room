from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

# Fields common to both create & response
class TagBase(BaseModel):
    name: str

# What the client sends when creating a tag
class TagCreate(TagBase):
    pass

# What we return in API responses
class TagOut(TagBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
