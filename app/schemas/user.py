from pydantic import BaseModel, EmailStr, constr, HttpUrl
from uuid import UUID
from datetime import datetime
from typing import Optional, List


class BadgeOut(BaseModel):
    id: UUID
    name: str
    description: Optional[str]

    class Config:
        from_attributes = True


class UserBase(BaseModel):
    username: constr(min_length=3, max_length=50)
    email: EmailStr
    display_name: Optional[str] = None
    avatar_url: Optional[HttpUrl] = None
    bio: Optional[str] = None
    social_links: Optional[str] = None

class UserCreate(UserBase):
    password_hash: constr(min_length=8)

class UserUpdate(UserBase):
    username: Optional[str]
    email: Optional[EmailStr]
    # password_hash: Optional[str]

class UserLogin(BaseModel):
    username: Optional[constr(min_length=3, max_length=50)] = None
    email: Optional[EmailStr] = None
    password_hash: constr(min_length=8)

class UserOut(UserBase):
    id: UUID
    reputation: int
    created_at: datetime
    updated_at: datetime
    last_login: Optional[datetime]
    is_active: bool
    role: str
    badges: List[BadgeOut] = []
    # approved_answers: int

    class Config:
        from_attributes = True
