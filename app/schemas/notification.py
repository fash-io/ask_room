from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional
from app.models import NotificationType

class NotificationBase(BaseModel):
    user_id: UUID
    type: NotificationType
    message: str
    link: Optional[str] = None

class NotificationCreate(NotificationBase):
    pass

class NotificationOut(NotificationBase):
    id: UUID
    is_read: bool
    created_at: datetime

    class Config:
        from_attributes = True
