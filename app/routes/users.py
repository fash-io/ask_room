from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID
from typing import List

from app.schemas.user import UserCreate, UserOut,UserUpdate
from app.crud import user as crud_user
from app.dependencies import get_db, get_current_user
from app.models import User

router = APIRouter()


@router.post("/", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def create_user(user_data: UserCreate, db: Session = Depends(get_db)):
    try:
        return crud_user.create_user(db, user_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/me", response_model=UserOut)
async def get_current_user_route(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return current_user

@router.put("/me")
async def update_current_user_route(user_data: UserOut, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    updated_user = crud_user.update_user(db, current_user.id, user_data)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user


@router.patch("/me/password")
def change_password(
    pswrd: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    upd = crud_user.update_user_password(db, current_user.id, pswrd)
    if not upd:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "Password updated"}
    

@router.get("/{user_id}", response_model=UserOut)
def get_user_by_id(user_id: UUID, db: Session = Depends(get_db)):
    user = crud_user.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.get("/username/{username}", response_model=UserOut)
def get_user_by_username(username: str, db: Session = Depends(get_db)):
    user = crud_user.get_user_by_username(db, username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.get("/email/{email}", response_model=UserOut)
def get_user_by_email(email: str, db: Session = Depends(get_db)):
    user = crud_user.get_user_by_email(db, email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/search/{query}", response_model=List[UserOut])
def search_users(query: str, db: Session = Depends(get_db)):
    users = crud_user.get_users_fuzzy(db, query)
    if len(users):
        return users
    raise HTTPException(status_code=404, detail="No users found")

@router.put("/{user_id}", response_model=UserOut)
def update_user(user_id: UUID, user_data: UserUpdate, db: Session = Depends(get_db)):
    updated_user = crud_user.update_user(db, user_id, user_data)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: UUID, db: Session = Depends(get_db)):
    deleted = crud_user.delete_user(db, user_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="User not found")
