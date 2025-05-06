from sqlalchemy.orm import Session
from uuid import UUID
from datetime import datetime

from app.models import Notification, NotificationType, User
from app.schemas.notification import NotificationCreate, NotificationOut

def create_notification(db: Session, notification_data: NotificationCreate):
    """Create a new notification for a user"""
    notification = Notification(
        user_id=notification_data.user_id,
        type=notification_data.type,
        message=notification_data.message,
        link=notification_data.link,
        created_at=datetime.utcnow(),
    )
    db.add(notification)
    db.commit()
    db.refresh(notification)
    return notification

def get_notifications_for_user(db: Session, user_id: UUID, skip: int = 0, limit: int = 20, unread_only: bool = False):
    """Get notifications for a specific user with pagination"""
    query = db.query(Notification).filter(Notification.user_id == user_id)
    
    if unread_only:
        query = query.filter(Notification.is_read == False)
    
    total = query.count()
    notifications = query.order_by(Notification.created_at.desc()).offset(skip).limit(limit).all()
    
    return {
        "total": total,
        "items": notifications
    }

def mark_notification_as_read(db: Session, notification_id: UUID):
    """Mark a specific notification as read"""
    notification = db.query(Notification).filter(Notification.id == notification_id).first()
    if notification:
        notification.is_read = True
        db.commit()
        db.refresh(notification)
        return notification
    return None

def mark_all_notifications_as_read(db: Session, user_id: UUID):
    """Mark all notifications for a user as read"""
    db.query(Notification).filter(
        Notification.user_id == user_id,
        Notification.is_read == False
    ).update({"is_read": True})
    db.commit()
    return {"message": "All notifications marked as read"}

def delete_notification(db: Session, notification_id: UUID):
    """Delete a specific notification"""
    notification = db.query(Notification).filter(Notification.id == notification_id).first()
    if notification:
        db.delete(notification)
        db.commit()
        return True
    return False

def get_unread_notification_count(db: Session, user_id: UUID):
    """Get the count of unread notifications for a user"""
    return db.query(Notification).filter(
        Notification.user_id == user_id,
        Notification.is_read == False
    ).count()

def notify_new_answer(db: Session, question_author_id: UUID, question_id: UUID, question_title: str, answer_id: UUID):
    """Create a notification when a new answer is posted to a user's question"""
    notification = Notification(
        user_id=question_author_id,
        type=NotificationType.answer_posted,
        message=f"Someone answered your question: '{question_title}'",
        link=f"/questions/{question_id}#answer-{answer_id}",
        created_at=datetime.utcnow(),
    )
    db.add(notification)
    db.commit()
    return notification

def notify_answer_accepted(db: Session, answer_author_id: UUID, question_id: UUID, question_title: str):
    """Create a notification when a user's answer is accepted"""
    notification = Notification(
        user_id=answer_author_id,
        type=NotificationType.answer_accepted,
        message=f"Your answer was accepted for the question: '{question_title}'",
        link=f"/questions/{question_id}",
        created_at=datetime.utcnow(),
    )
    db.add(notification)
    db.commit()
    return notification

def notify_badge_earned(db: Session, user_id: UUID, badge_name: str, badge_id: UUID):
    """Create a notification when a user earns a badge"""
    notification = Notification(
        user_id=user_id,
        type=NotificationType.badge_earned,
        message=f"Congratulations! You earned the '{badge_name}' badge",
        link=f"/badges/{badge_id}",
        created_at=datetime.utcnow(),
    )
    db.add(notification)
    db.commit()
    return notification
