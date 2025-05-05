from sqlalchemy.orm import Session
from uuid import UUID
from datetime import datetime

from app.models import Category
from app.schemas.category import CategoryCreate, CategoryOut

def create_category(db: Session, category_data: CategoryCreate) -> CategoryOut:
    # Create a new category
    category = Category(
        name=category_data.name,
        description=category_data.description,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )
    db.add(category)
    db.commit()
    db.refresh(category)

    return CategoryOut(
        id=category.id,
        name=category.name,
        description=category.description,
        created_at=category.created_at,
        updated_at=category.updated_at,
    )


def get_category_by_id(db: Session, category_id: UUID) -> CategoryOut:
    # Get a category by its ID
    category = db.query(Category).filter(Category.id == category_id).first()
    if category:
        return CategoryOut(
            id=category.id,
            name=category.name,
            description=category.description,
            created_at=category.created_at,
            updated_at=category.updated_at,
        )
    return None


def get_categories(db: Session) -> list[CategoryOut]:
    # Get all categories
    categories = db.query(Category).all()
    return [
        CategoryOut(
            id=category.id,
            name=category.name,
            description=category.description,
            created_at=category.created_at,
            updated_at=category.updated_at,
        )
        for category in categories
    ]


def update_category(db: Session, category_id: UUID, category_data: CategoryCreate) -> CategoryOut:
    # Update a category's information
    category = db.query(Category).filter(Category.id == category_id).first()
    if category:
        category.name = category_data.name if category_data.name else category.name
        category.description = category_data.description if category_data.description else category.description
        category.updated_at = datetime.utcnow()

        db.commit()
        db.refresh(category)

        return CategoryOut(
            id=category.id,
            name=category.name,
            description=category.description,
            created_at=category.created_at,
            updated_at=category.updated_at,
        )
    return None


def delete_category(db: Session, category_id: UUID) -> bool:
    # Delete a category by ID
    category = db.query(Category).filter(Category.id == category_id).first()
    if category:
        db.delete(category)
        db.commit()
        return True
    return False

def get_categories_fuzzy(db: Session, query: str) -> list[CategoryOut]:
    # Get all categories that match the query
    categories = db.query(Category).filter(Category.name.contains(query)).all()
    return [
        CategoryOut(
            id=category.id,
            name=category.name,
            description=category.description or "",
            created_at=category.created_at,
            updated_at=category.updated_at,
        )
        for category in categories
    ]