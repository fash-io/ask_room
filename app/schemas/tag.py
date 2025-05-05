from pydantic import BaseModel, EmailStr, constr, HttpUrl
from uuid import UUID
from datetime import datetime
from typing import Optional


# Base schema: shared fields
class UserBase(BaseModel):
    username: constr(min_length=3, max_length=50)
    email: EmailStr
    display_name: Optional[str] = None
    avatar_url: Optional[HttpUrl] = None
    bio: Optional[str] = None
    social_links: Optional[str] = None


# Schema for creating a new user
class UserCreate(UserBase):
    password: constr(min_length=8)


# Schema for user login
class UserLogin(BaseModel):
    username: Optional[constr(min_length=3, max_length=50)] = None
    email: Optional[EmailStr] = None
    password: constr(min_length=8)


# Schema for responses: include IDs and timestamps
class UserOut(UserBase):
    id: UUID
    reputation: int
    created_at: datetime
    updated_at: datetime
    last_login: Optional[datetime]
    is_active: bool
    role: str

    class Config:
        orm_mode = True
