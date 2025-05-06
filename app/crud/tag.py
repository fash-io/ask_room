from sqlalchemy.orm import Session
from uuid import UUID
from datetime import datetime
from rapidfuzz import fuzz

from app.models import Tag
from app.schemas.tag import TagCreate, TagOut

def create_tag(db: Session, tag_data: TagCreate) -> TagOut:
    # Create a new tag
    tag = Tag(
        name=tag_data.name,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )
    db.add(tag)
    db.commit()
    db.refresh(tag)

    return TagOut(
        id=tag.id,
        name=tag.name,
        created_at=tag.created_at,
        updated_at=tag.updated_at,
    )


def get_tag_by_id(db: Session, tag_id: UUID) -> TagOut:
    # Get a tag by its ID
    tag = db.query(Tag).filter(Tag.id == tag_id).first()
    if tag:
        return TagOut(
            id=tag.id,
            name=tag.name,
            created_at=tag.created_at,
            updated_at=tag.updated_at,
        )
    return None


def get_tags(db: Session) -> list[TagOut]:
    # Get all tags
    tags = db.query(Tag).all()
    return [
        TagOut(
            id=tag.id,
            name=tag.name,
            created_at=tag.created_at,
            updated_at=tag.updated_at,
        )
        for tag in tags
    ]


def update_tag(db: Session, tag_id: UUID, tag_data: TagCreate) -> TagOut:
    # Update a tag's information
    tag = db.query(Tag).filter(Tag.id == tag_id).first()
    if tag:
        tag.name = tag_data.name if tag_data.name else tag.name
        tag.updated_at = datetime.utcnow()

        db.commit()
        db.refresh(tag)

        return TagOut(
            id=tag.id,
            name=tag.name,
            created_at=tag.created_at,
            updated_at=tag.updated_at,
        )
    return None


def delete_tag(db: Session, tag_id: UUID) -> bool:
    # Delete a tag by ID
    tag = db.query(Tag).filter(Tag.id == tag_id).first()
    if tag:
        db.delete(tag)
        db.commit()
        return True
    return False

def get_tags_fuzzy(db: Session, query: str):
    tags = db.query(Tag).all()
    matches = [
        q for q in tags
        if fuzz.partial_ratio(query.lower(), q.name.lower()) > 70
    ]
    return matches
