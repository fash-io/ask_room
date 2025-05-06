from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID


from app.dependencies import get_current_user
from app.database import get_db
from app.crud import notification as crud_notification
from app.schemas.notification import NotificationOut, NotificationCreate
from app.models import User

router = APIRouter()

@router.get("/", response_model=dict)
async def get_notifications(
    skip: int = 0,
    limit: int = 20,
    unread_only: bool = False,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get notifications for the current user"""
    return crud_notification.get_notifications_for_user(
        db, current_user.id, skip, limit, unread_only
    )

@router.get("/count", response_model=dict)
async def get_unread_count(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get the count of unread notifications for the current user"""
    count = crud_notification.get_unread_notification_count(db, current_user.id)
    return {"count": count}

@router.post("/{notification_id}/read", response_model=NotificationOut)
async def mark_as_read(
    notification_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Mark a notification as read"""
    notification = crud_notification.mark_notification_as_read(db, notification_id)
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    
    # Ensure the notification belongs to the current user
    if notification.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to access this notification")
    
    return notification

@router.post("/read-all", response_model=dict)
async def mark_all_as_read(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Mark all notifications as read for the current user"""
    return crud_notification.mark_all_notifications_as_read(db, current_user.id)

@router.delete("/{notification_id}", response_model=dict)
async def delete_notification(
    notification_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete a notification"""
    # First check if the notification exists and belongs to the current user
    notification = db.query(crud_notification.Notification).filter(
        crud_notification.Notification.id == notification_id,
        crud_notification.Notification.user_id == current_user.id
    ).first()
    
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    
    success = crud_notification.delete_notification(db, notification_id)
    if success:
        return {"message": "Notification deleted successfully"}
    
    raise HTTPException(status_code=500, detail="Failed to delete notification")
