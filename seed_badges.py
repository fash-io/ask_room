from uuid import uuid4
from datetime import datetime, timezone
from sqlalchemy.exc import IntegrityError

from app.database import SessionLocal, engine, Base
from app.models import Badge, BadgeLevel, BadgeCategory

Base.metadata.create_all(bind=engine)
BADGES = [
    # Participation Badges
    {
        "name": "First Question",
        "description": "Asked your first question",
        "criteria": {"type": "questions_posted", "threshold": 1},
        "category": BadgeCategory.participation,
        "level": BadgeLevel.bronze,
        "icon": "help-circle"
    },
    {
        "name": "First Answer",
        "description": "Posted your first answer",
        "criteria": {"type": "answers_posted", "threshold": 1},
        "category": BadgeCategory.participation,
        "level": BadgeLevel.bronze,
        "icon": "message-circle"
    },
    {
        "name": "Curious Mind",
        "description": "Asked 10 questions",
        "criteria": {"type": "questions_posted", "threshold": 10},
        "category": BadgeCategory.participation,
        "level": BadgeLevel.silver,
        "icon": "help-circle"
    },
    {
        "name": "Prolific Asker",
        "description": "Asked 50 questions",
        "criteria": {"type": "questions_posted", "threshold": 50},
        "category": BadgeCategory.participation,
        "level": BadgeLevel.gold,
        "icon": "help-circle"
    },
    {
        "name": "Helpful Hand",
        "description": "Posted 25 answers",
        "criteria": {"type": "answers_posted", "threshold": 25},
        "category": BadgeCategory.participation,
        "level": BadgeLevel.silver,
        "icon": "message-circle"
    },
    {
        "name": "Knowledge Sharer",
        "description": "Posted 100 answers",
        "criteria": {"type": "answers_posted", "threshold": 100},
        "category": BadgeCategory.participation,
        "level": BadgeLevel.gold,
        "icon": "message-circle"
    },
    
    # Quality Badges
    {
        "name": "First Approval",
        "description": "Received your first approved answer",
        "criteria": {"type": "approved_answers", "threshold": 1},
        "category": BadgeCategory.quality,
        "level": BadgeLevel.bronze,
        "icon": "check-circle"
    },
    {
        "name": "Quality Contributor",
        "description": "Received 10 approved answers",
        "criteria": {"type": "approved_answers", "threshold": 10},
        "category": BadgeCategory.quality,
        "level": BadgeLevel.silver,
        "icon": "check-circle"
    },
    {
        "name": "Expert Advice",
        "description": "Received 50 approved answers",
        "criteria": {"type": "approved_answers", "threshold": 50},
        "category": BadgeCategory.quality,
        "level": BadgeLevel.gold,
        "icon": "award"
    },
    {
        "name": "Well Received",
        "description": "Got 10+ upvotes on your answers",
        "criteria": {"type": "upvotes_received", "threshold": 10},
        "category": BadgeCategory.quality,
        "level": BadgeLevel.bronze,
        "category": BadgeCategory.quality,
        "level": BadgeLevel.bronze,
        "icon": "thumbs-up"
    },
    {
        "name": "Helpful Contributor",
        "description": "Got 20+ upvotes on your answers",
        "criteria": {"type": "upvotes_received", "threshold": 20},
        "category": BadgeCategory.quality,
        "level": BadgeLevel.silver,
        "icon": "thumbs-up"
    },
    {
        "name": "Community Leader",
        "description": "Received 100+ upvotes on answers",
        "criteria": {"type": "upvotes_received", "threshold": 100},
        "category": BadgeCategory.quality,
        "level": BadgeLevel.gold,
        "icon": "star"
    },
    
    # Community Badges
    {
        "name": "Respected",
        "description": "Reached 100 reputation points",
        "criteria": {"type": "reputation", "threshold": 100},
        "category": BadgeCategory.community,
        "level": BadgeLevel.bronze,
        "icon": "users"
    },
    {
        "name": "Trusted",
        "description": "Reached 500 reputation points",
        "criteria": {"type": "reputation", "threshold": 500},
        "category": BadgeCategory.community,
        "level": BadgeLevel.silver,
        "icon": "users"
    },
    {
        "name": "All-Star Contributor",
        "description": "Earned 1,000+ reputation points",
        "criteria": {"type": "reputation", "threshold": 1000},
        "category": BadgeCategory.community,
        "level": BadgeLevel.gold,
        "icon": "award"
    },
    {
        "name": "Early Adopter",
        "description": "Joined the platform within the first month of launch",
        "criteria": {"type": "join_date", "threshold_days": 30},
        "category": BadgeCategory.community,
        "level": BadgeLevel.bronze,
        "icon": "clock"
    },
    
    # Achievement Badges
    {
        "name": "Streak: Week",
        "description": "Visited the site for 7 consecutive days",
        "criteria": {"type": "consecutive_days", "threshold": 7},
        "category": BadgeCategory.achievement,
        "level": BadgeLevel.bronze,
        "icon": "calendar"
    },
    {
        "name": "Streak: Month",
        "description": "Visited the site for 30 consecutive days",
        "criteria": {"type": "consecutive_days", "threshold": 30},
        "category": BadgeCategory.achievement,
        "level": BadgeLevel.silver,
        "icon": "calendar"
    },
    {
        "name": "Taxonomist",
        "description": "Created a tag that was used by 10 questions",
        "criteria": {"type": "tags_created", "threshold": 10},
        "category": BadgeCategory.achievement,
        "level": BadgeLevel.silver,
        "icon": "tag"
    },
    {
        "name": "Editor",
        "description": "Made 10 edits to improve posts",
        "criteria": {"type": "edits_made", "threshold": 10},
        "category": BadgeCategory.achievement,
        "level": BadgeLevel.bronze,
        "icon": "edit"
    },
    
    # Moderation Badges
    {
        "name": "Custodian",
        "description": "Completed first moderation task",
        "criteria": {"type": "moderation_tasks", "threshold": 1},
        "category": BadgeCategory.moderation,
        "level": BadgeLevel.bronze,
        "icon": "shield"
    },
    {
        "name": "Guardian",
        "description": "Completed 100 moderation tasks",
        "criteria": {"type": "moderation_tasks", "threshold": 100},
        "category": BadgeCategory.moderation,
        "level": BadgeLevel.silver,
        "icon": "shield"
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
            category=data["category"],
            level=data["level"],
            icon=data.get("icon"),
            created_at=datetime.now(timezone.utc),
        )
        try:
            db.add(badge)
            db.commit()
            print(f"Added badge: {badge.name}")
        except IntegrityError:
            db.rollback()  # Badge already exists—skip
            print(f"Badge already exists: {badge.name}")
    db.close()

if __name__ == "__main__":
    seed_badges()
    print("✅ Badges seeded successfully.")
