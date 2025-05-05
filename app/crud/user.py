from sqlalchemy.orm import Session
from uuid import UUID
from models import User
from schemas.user import UserCreate, UserUpdate


def create_user(db: Session, user_data: UserCreate):
    # Check if the username or email already exists
    existing_user = (
        db.query(User)
        .filter((User.username == user_data.username) | (User.email == user_data.email))
        .first()
    )

    if existing_user:
        raise ValueError("Username or Email already exists")

    # Create new user
    user = User(
        username=user_data.username,
        email=user_data.email,
        password_hash=user_data.password_hash,  # Should hash password in production
        full_name=user_data.full_name,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_user_by_id(db: Session, user_id: UUID):
    # Get user by ID
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_username(db: Session, username: str):
    # Get user by username
    return db.query(User).filter(User.username == username).first()


def get_user_by_email(db: Session, email: str):
    # Get user by email
    return db.query(User).filter(User.email == email).first()


def update_user(db: Session, user_id: UUID, user_data: UserUpdate):
    # Update user information
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        user.username = user_data.username if user_data.username else user.username
        user.email = user_data.email if user_data.email else user.email
        user.password_hash = (
            user_data.password_hash if user_data.password_hash else user.password_hash
        )
        user.full_name = user_data.full_name if user_data.full_name else user.full_name

        db.commit()
        db.refresh(user)
        return user
    return None


def delete_user(db: Session, user_id: UUID):
    # Delete a user by ID
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        db.delete(user)
        db.commit()
        return True
    return False
