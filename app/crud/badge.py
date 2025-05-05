from typing import List, Optional
from uuid import UUID

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.models import Badge, BadgeCategory, BadgeLevel, User



def create_badge(
    db: Session,
    *,
    name: str,
    description: Optional[str],
    criteria: dict,
    category: BadgeCategory,
    level: BadgeLevel
) -> Badge:
    """
    Create a new Badge.
    Raises IntegrityError if a badge with the same name already exists.
    """
    badge = Badge(
        name=name,
        description=description,
        criteria=criteria,
        category=category,
        level=level,
    )
    db.add(badge)
    db.commit()
    db.refresh(badge)
    return badge


def get_badge(db: Session, badge_id: UUID) -> Optional[Badge]:
    """Retrieve a badge by its UUID."""
    return db.query(Badge).filter(Badge.id == badge_id).first()


def get_all_badges(db: Session) -> List[Badge]:
    """Retrieve all badges."""
    return db.query(Badge).order_by(Badge.name).all()


def get_badges_by_category(
    db: Session, category: BadgeCategory
) -> List[Badge]:
    """Retrieve badges filtered by category."""
    return (
        db.query(Badge)
        .filter(Badge.category == category)
        .order_by(Badge.level, Badge.name)
        .all()
    )


def get_badges_by_level(
    db: Session, level: BadgeLevel
) -> List[Badge]:
    """Retrieve badges filtered by level."""
    return (
        db.query(Badge)
        .filter(Badge.level == level)
        .order_by(Badge.category, Badge.name)
        .all()
    )


def update_badge(
    db: Session,
    badge_id: UUID,
    *,
    name: Optional[str] = None,
    description: Optional[str] = None,
    criteria: Optional[dict] = None,
    category: Optional[BadgeCategory] = None,
    level: Optional[BadgeLevel] = None,
) -> Optional[Badge]:
    """
    Update fields of an existing badge. Returns the updated badge or None if not found.
    """
    badge = db.query(Badge).filter(Badge.id == badge_id).first()
    if not badge:
        return None

    if name is not None:
        badge.name = name
    if description is not None:
        badge.description = description
    if criteria is not None:
        badge.criteria = criteria
    if category is not None:
        badge.category = category
    if level is not None:
        badge.level = level

    db.commit()
    db.refresh(badge)
    return badge


def delete_badge(db: Session, badge_id: UUID) -> bool:
    """
    Delete a badge by its UUID.
    Returns True if deleted, False if not found.
    """
    badge = db.query(Badge).filter(Badge.id == badge_id).first()
    if not badge:
        return False

    db.delete(badge)
    db.commit()
    return True


def user_has_badge(db: Session, user_id: UUID, badge_id: UUID) -> bool:
    """
    Check if a user already has a particular badge.
    """
    # Assumes `user_badges` association is set up
    return (
        db.query(Badge)
        .join(Badge.users)
        .filter(Badge.id == badge_id, Badge.users.any(id=user_id))
        .count()
        > 0
    )


def award_badge(db: Session, user_id: UUID, badge_id: UUID) -> None:
    """
    Award a badge to a user (inserts into the association table).
    Does nothing if the user already has the badge.
    """
    if not user_has_badge(db, user_id, badge_id):
        badge = db.query(Badge).filter(Badge.id == badge_id).first()
        user = db.query(User).filter(User.id == user_id).first()
        if badge and user:
            user.badges.append(badge)
            db.commit()
