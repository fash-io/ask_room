from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID
from typing import List

from app.database import get_db
from app.schemas.category import CategoryCreate, CategoryOut
from app.crud import category as crud_category

router = APIRouter()


@router.post("/", response_model=CategoryOut, status_code=status.HTTP_201_CREATED)
def create_category(category_data: CategoryCreate, db: Session = Depends(get_db)):
    return crud_category.create_category(db, category_data)


@router.get("/{category_id}", response_model=CategoryOut)
def get_category(category_id: UUID, db: Session = Depends(get_db)):
    category = crud_category.get_category_by_id(db, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


@router.get("/", response_model=List[CategoryOut])
def get_all_categories(db: Session = Depends(get_db)):
    return crud_category.get_categories(db)


@router.put("/{category_id}", response_model=CategoryOut)
def update_category(category_id: UUID, category_data: CategoryCreate, db: Session = Depends(get_db)):
    updated = crud_category.update_category(db, category_id, category_data)
    if not updated:
        raise HTTPException(status_code=404, detail="Category not found")
    return updated


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(category_id: UUID, db: Session = Depends(get_db)):
    deleted = crud_category.delete_category(db, category_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Category not found")
