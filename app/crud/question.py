from uuid import UUID
from sqlalchemy.orm import Session
from rapidfuzz import fuzz
from sqlalchemy import or_

from app.models import Question, Tag
from app.schemas.question import QuestionCreate
# Create a new question
def create_question(db: Session, question_data: QuestionCreate, user_id: UUID):
    tags = db.query(Tag).filter(Tag.id.in_(question_data.tags)).all() 
    
    question = Question(
        title=question_data.title,
        body=question_data.body,
        images=question_data.images,
        category_id=question_data.category_id,
        author_id=user_id,
    )
    
    question.tags = tags 
    
    db.add(question)
    db.commit()
    db.refresh(question)
    return question

# Get a question by ID

def get_question_by_id(db: Session, question_id: UUID):
    return db.query(Question).filter(Question.id == question_id).first()

def get_all_questions(db: Session, skip: int = 0, limit: int = 10):
    total = db.query(Question).count()
    items = db.query(Question).offset(skip).limit(limit).all()
    return {"total": total, "items": items}

def get_questions_by_category(db: Session, category_id: UUID, skip: int = 0, limit: int = 10):
    query = db.query(Question).filter(Question.category_id == category_id)
    total = query.count()
    items = query.offset(skip).limit(limit).all()
    return {"total": total, "items": items}

def get_questions_by_tag(db: Session, tag_id: UUID, skip: int = 0, limit: int = 10):
    query = db.query(Question).join(Question.tags).filter(Tag.id == tag_id)
    total = query.count()
    items = query.offset(skip).limit(limit).all()
    return {"total": total, "items": items}

def get_questions_by_user(db: Session, user_id: UUID, skip: int = 0, limit: int = 10):
    query = db.query(Question).filter(Question.author_id == user_id)
    total = query.count()
    items = query.offset(skip).limit(limit).all()
    return {"total": total, "items": items}

def get_questions_by_title(db: Session, title: str, skip: int = 0, limit: int = 10):
    query = db.query(Question).filter(Question.title.contains(title))
    total = query.count()
    items = query.offset(skip).limit(limit).all()
    return {"total": total, "items": items}


# Update a question
def update_question(db: Session, question_id: UUID, question_data: QuestionCreate):
    question = db.query(Question).filter(Question.id == question_id).first()
    if question:
        question.title = question_data.title
        question.body = question_data.body
        question.images = question_data.images
        question.category_id = question_data.category_id
        
        if question_data.tags is not None:
            tags = db.query(Tag).filter(Tag.id.in_(question_data.tags)).all()
            question.tags = tags 
        
        db.commit()
        db.refresh(question)
        return question
    return None

# Delete a question
def delete_question(db: Session, question_id: UUID):
    question = db.query(Question).filter(Question.id == question_id).first()
    if question:
        db.delete(question)
        db.commit()
        return True
    return False


def search_questions_pg_trgm(db: Session, query: str, limit: int = 20):
    return db.query(Question).filter(
        or_(
            Question.title.ilike(f"%{query}%"),
            Question.body.ilike(f"%{query}%")
        )
    ).limit(limit).all()
