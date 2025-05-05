from sqlalchemy.orm import Session
from uuid import UUID
from datetime import datetime
from passlib.context import CryptContext
from rapidfuzz import fuzz

from app.models import User
from app.schemas.user import UserCreate, UserOut


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_user(db: Session, user_data: UserCreate):
    # Check if the username or email already exists
    existing_user = db.query(User).filter(
        (User.username == user_data.username) | (User.email == user_data.email)
    ).first()
    
    if existing_user:
        raise ValueError("Username or Email already exists")
    
    # Hash the user's password
    hashed_password = pwd_context.hash(user_data.password)
    
    # Create new user
    user = User(
        username=user_data.username,
        email=user_data.email,
        display_name=user_data.display_name,
        avatar_url=user_data.avatar_url,
        bio=user_data.bio,
        social_links=user_data.social_links,
        password_hash=hashed_password,
        reputation=0,
        is_active=True,
        role="user",  # Default role can be 'user' or adjust based on your app's needs
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )
    
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_user_by_id(db: Session, user_id: UUID) -> UserOut:
    # Get user by ID and return in UserOut format
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        return user
    return None


def get_user_by_username(db: Session, username: str) -> UserOut:
    # Get user by username and return in UserOut format
    user = db.query(User).filter(User.username == username).first()
    if user:
        return user
    return None


def get_user_by_email(db: Session, email: str) -> UserOut:
    # Get user by email and return in UserOut format
    user = db.query(User).filter(User.email == email).first()
    if user:
        return user
    return None


def update_user(db: Session, user_id: UUID, user_data: UserCreate) -> UserOut:
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        user.username = user_data.username if user_data.username else user.username
        user.email = user_data.email if user_data.email else user.email
        user.display_name = user_data.display_name if user_data.display_name else user.display_name
        user.avatar_url = user_data.avatar_url if user_data.avatar_url else user.avatar_url
        user.bio = user_data.bio if user_data.bio else user.bio
        user.social_links = user_data.social_links if user_data.social_links else user.social_links
        user.updated_at = datetime.utcnow()

        if user_data.password_hash:
            user.password_hash = pwd_context.hash(user_data.password_hash)

        db.commit()
        db.refresh(user)

        return UserOut(**user)
    return None

def update_user_password(db: Session, user_id: UUID, password: str) -> UserOut:
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        user.password_hash = pwd_context.hash(password)
        
    db.commit()
    db.refresh(user)
    return UserOut(**user)


def delete_user(db: Session, user_id: UUID) -> bool:
    # Delete a user by ID
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        db.delete(user)
        db.commit()
        return True
    return False

def get_users_fuzzy(db: Session, query: str):
    users = db.query(User).all()
    matches = [
        q for q in users
        if fuzz.partial_ratio(query.lower(), q.username.lower()) > 70
        or fuzz.partial_ratio(query.lower(), q.display_name.lower()) > 70
    ]
    return matches