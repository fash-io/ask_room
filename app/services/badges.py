from app.crud.badge import get_all_badges, user_has_badge, award_badge
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timezone
from models import Badge, User


def check_and_award_badges(db: Session, user: User) -> List[Badge]:
    earned = []
    
    now = datetime.now(timezone.utc)
    days_since_join = (now - user.created_at).days

    # Calculate user stats
    stats = {
        "answers_posted": len(user.answers),
        "approved_answers": user.approved_answers_count,
        "reputation": user.reputation,
        "questions_posted": len(user.questions),
        "upvotes_received": user.answer_votes.filter_by(vote_value="upvote").count(), 
        "join_date": days_since_join
    }

    for badge in get_all_badges(db):
        crit = badge.criteria or {}
        badge_type = crit.get("type")

        if badge_type == "join_date":
            threshold_days = crit.get("threshold_days", 0)
            if days_since_join <= threshold_days:
                if not user_has_badge(db, user.id, badge.id):
                    award_badge(db, user.id, badge.id)
                    earned.append(badge)

        elif badge_type in stats:
            user_stat = stats[badge_type]
            threshold = crit.get("threshold", 0)
            if user_stat >= threshold:
                if not user_has_badge(db, user.id, badge.id):
                    award_badge(db, user.id, badge.id)
                    earned.append(badge)


    return earned
