from pydantic import BaseModel
from typing import Optional, Dict
from uuid import UUID
from enum import Enum

class BadgeCategory(str, Enum):
    COMMUNITY = "community"
    TECHNICAL = "technical"
    PARTICIPATION = "participation"
    QUALITY = "quality"


class BadgeLevel(str, Enum):
    BRONZE = "bronze"
    SILVER = "silver"
    GOLD = "gold"


class BadgeBase(BaseModel):
    name: str
    description: Optional[str]
    criteria: Dict

class BadgeCreate(BadgeBase):
    category: BadgeCategory
    level: BadgeLevel

class BadgeUpdate(BaseModel):
    name: Optional[str]
    description: Optional[str]
    criteria: Optional[Dict]
    category: Optional[BadgeCategory]
    level: Optional[BadgeLevel]

class Badge(BadgeBase):
    id: UUID
    category: BadgeCategory
    level: BadgeLevel

    model_config = {
        "from_attributes": True
    }
