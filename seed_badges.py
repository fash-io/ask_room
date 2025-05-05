from app.database import SessionLocal
from app.models import Badge
from sqlalchemy.exc import IntegrityError

from uuid import uuid4
from datetime import datetime

BADGES = [
    {"name": "First Answer", "description": "Posted your first answer."},
    {"name": "First Approval", "description": "Received your first approved answer."},
    {"name": "10 Approved Answers", "description": "Received 10 approved answers."},
    {"name": "100 Reputation", "description": "Reached 100 reputation points."},
    {"name": "Question Master", "description": "Posted 10 or more questions."},
    {"name": "Helpful Contributor", "description": "Got 20+ upvotes on your answers."},
]


def seed_badges():
    db = SessionLocal()
    for badge_data in BADGES:
        badge = Badge(
            id=uuid4(),
            name=badge_data["name"],
            description=badge_data["description"],
            created_at=datetime.utcnow(),
        )
        try:
            db.add(badge)
            db.commit()
        except IntegrityError:
            db.rollback()  # Badge already exists, ignore
    db.close()


if __name__ == "__main__":
    seed_badges()
    print("Badges seeded successfully.")
