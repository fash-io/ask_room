# app/routes/badges.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID

from app.crud import badge as crud
from app.schemas import badge
from app.database import get_db

router = APIRouter()

@router.post("/", response_model=badge.Badge)
def create_badge(badge: badge.BadgeCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_badge(db, **badge.dict())
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=list[badge.Badge])
def get_all_badges(db: Session = Depends(get_db)):
    return crud.get_all_badges(db)

@router.get("/{badge_id}", response_model=badge.Badge)
def get_badge(badge_id: UUID, db: Session = Depends(get_db)):
    badge = crud.get_badge(db, badge_id)
    if not badge:
        raise HTTPException(status_code=404, detail="Badge not found")
    return badge

@router.put("/{badge_id}", response_model=badge.Badge)
def update_badge(badge_id: UUID, update: badge.BadgeUpdate, db: Session = Depends(get_db)):
    badge = crud.update_badge(db, badge_id, **update.dict(exclude_unset=True))
    if not badge:
        raise HTTPException(status_code=404, detail="Badge not found")
    return badge

@router.delete("/{badge_id}")
def delete_badge(badge_id: UUID, db: Session = Depends(get_db)):
    success = crud.delete_badge(db, badge_id)
    if not success:
        raise HTTPException(status_code=404, detail="Badge not found")
    return {"message": "Deleted"}
