from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID
from typing import List

from app.dependencies import get_db
from app.schemas.tag import TagCreate, TagOut
from app.crud import tag as crud_tag

router = APIRouter()


@router.post("/", response_model=TagOut, status_code=status.HTTP_201_CREATED)
def create_tag(tag_data: TagCreate, db: Session = Depends(get_db)):
    try:
        return crud_tag.create_tag(db, tag_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{tag_id}", response_model=TagOut)
def get_tag_by_id(tag_id: UUID, db: Session = Depends(get_db)):
    tag = crud_tag.get_tag_by_id(db, tag_id)
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    return tag


@router.get("/", response_model=List[TagOut])
def get_tags(db: Session = Depends(get_db)):
    return crud_tag.get_tags(db)


@router.put("/{tag_id}", response_model=TagOut)
def update_tag(tag_id: UUID, tag_data: TagCreate, db: Session = Depends(get_db)):
    updated_tag = crud_tag.update_tag(db, tag_id, tag_data)
    if not updated_tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    return updated_tag


@router.delete("/{tag_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_tag(tag_id: UUID, db: Session = Depends(get_db)):
    deleted = crud_tag.delete_tag(db, tag_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Tag not found")
