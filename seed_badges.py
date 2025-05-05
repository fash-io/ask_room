from uuid import uuid4
from datetime import datetime, timezone
from sqlalchemy.exc import IntegrityError

from app.database import SessionLocal, engine, Base
from app.models import Badge, BadgeLevel, BadgeCategory
# from app.models import *

Base.metadata.create_all(bind=engine)
# Your badge definitions
BADGES = [
    {
        "name": "First Answer",
        "description": "Posted your first answer.",
        "criteria": {"type": "answers_posted", "threshold": 1},
        "category": "participation",
        "level": "bronze",
    },
    {
        "name": "First Approval",
        "description": "Received your first approved answer.",
        "criteria": {"type": "approved_answers", "threshold": 1},
        "category": "quality",
        "level": "bronze",
    },
    {
        "name": "10 Approved Answers",
        "description": "Received 10 approved answers.",
        "criteria": {"type": "approved_answers", "threshold": 10},
        "category": "quality",
        "level": "silver",
    },
    {
        "name": "100 Reputation",
        "description": "Reached 100 reputation points.",
        "criteria": {"type": "reputation", "threshold": 100},
        "category": "community",
        "level": "silver",
    },
    {
        "name": "Question Master",
        "description": "Posted 20 or more questions.",
        "criteria": {"type": "questions_posted", "threshold": 20},
        "category": "participation",
        "level": "silver",
    },
    {
        "name": "Helpful Contributor",
        "description": "Got 20+ upvotes on your answers.",
        "criteria": {"type": "upvotes_received", "threshold": 20},
        "category": "quality",
        "level": "silver",
    },
    {
        "name": "All-Star Contributor",
        "description": "Earned 1,000+ reputation points.",
        "criteria": {"type": "reputation", "threshold": 1000},
        "category": "community",
        "level": "gold",
    },
    {
        "name": "Legendary Contributor",
        "description": "Contributed 500 answers or more.",
        "criteria": {"type": "answers_posted", "threshold": 500},
        "category": "participation",
        "level": "gold",
    },
    {
        "name": "Community Leader",
        "description": "Received 100+ upvotes on answers.",
        "criteria": {"type": "upvotes_received", "threshold": 100},
        "category": "quality",
        "level": "gold",
    },
    {
        "name": "Early Adopter",
        "description": "Joined the platform within the first month of launch.",
        "criteria": {"type": "join_date", "threshold_days": 30},
        "category": "community",
        "level": "bronze",
    },
]

def seed_badges():
    db = SessionLocal()
    for data in BADGES:
        badge = Badge(
            id=uuid4(),
            name=data["name"],
            description=data["description"],
            criteria=data["criteria"],
            category=BadgeCategory(data["category"]),
            level=BadgeLevel(data["level"]),
            created_at=datetime.now(timezone.utc),
        )
        try:
            db.add(badge)
            db.commit()
        except IntegrityError:
            db.rollback()  # Badge already exists—skip
    db.close()

if __name__ == "__main__":
    seed_badges()
    print("✅ Badges seeded successfully.")
