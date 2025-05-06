from uuid import UUID
from sqlalchemy.orm import Session
from rapidfuzz import fuzz
from sqlalchemy import or_, func, text

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
        view_count=0,  # Initialize view count to 0
    )
    
    question.tags = tags 
    
    db.add(question)
    db.commit()
    db.refresh(question)
    return question

# Get a question by ID and increment view count
def get_question_by_id(db: Session, question_id: UUID, increment_view=True):
    question = db.query(Question).filter(Question.id == question_id).first()
    
    if question and increment_view:
        # Increment the view count
        question.view_count += 1
        db.commit()
        
    return question

def get_all_questions(db: Session, skip: int = 0, limit: int = 10):
    total = db.query(Question).count()
    items = db.query(Question).order_by(Question.created_at.desc()).offset(skip).limit(limit).all()
    return {"total": total, "items": items}

def get_questions_by_category(db: Session, category_id: UUID, skip: int = 0, limit: int = 10):
    query = db.query(Question).filter(Question.category_id == category_id)
    total = query.count()
    items = query.order_by(Question.created_at.desc()).offset(skip).limit(limit).all()
    return {"total": total, "items": items}

def get_questions_by_tag(db: Session, tag_id: UUID, skip: int = 0, limit: int = 10):
    query = db.query(Question).join(Question.tags).filter(Tag.id == tag_id)
    total = query.count()
    items = query.order_by(Question.created_at.desc()).offset(skip).limit(limit).all()
    return {"total": total, "items": items}

def get_questions_by_user(db: Session, user_id: UUID, skip: int = 0, limit: int = 10):
    query = db.query(Question).filter(Question.author_id == user_id)
    total = query.count()
    items = query.order_by(Question.created_at.desc()).offset(skip).limit(limit).all()
    return {"total": total, "items": items}

def get_questions_by_title(db: Session, title: str, skip: int = 0, limit: int = 10):
    query = db.query(Question).filter(Question.title.contains(title))
    total = query.count()
    items = query.order_by(Question.created_at.desc()).offset(skip).limit(limit).all()
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

# Basic search using ILIKE
def search_questions_pg_trgm(db: Session, query: str, limit: int = 20):
    return db.query(Question).filter(
        or_(
            Question.title.ilike(f"%{query}%"),
            Question.body.ilike(f"%{query}%")
        )
    ).limit(limit).all()

# Full-text search using PostgreSQL's ts_vector
def search_questions_full_text(db: Session, query: str, limit: int = 20):
    # Convert the query to a tsquery format
    ts_query = ' & '.join(query.split())
    
    # Use the search_vector column for full-text search
    result = db.query(Question).filter(
        Question.search_vector.op('@@')(func.to_tsquery('english', ts_query))
    ).order_by(
        func.ts_rank(Question.search_vector, func.to_tsquery('english', ts_query)).desc()
    ).limit(limit).all()
    
    return result

# Get trending questions (most viewed in the last week)
def get_trending_questions(db: Session, limit: int = 10):
    # Get questions from the last 7 days, ordered by view count
    query = text("""
        SELECT * FROM questions 
        WHERE created_at > NOW() - INTERVAL '7 days'
        ORDER BY view_count DESC
        LIMIT :limit
    """)
    
    result = db.execute(query, {"limit": limit})
    questions = [dict(row) for row in result]
    
    return questions

# Get hot questions (most answered recently)
def get_hot_questions(db: Session, limit: int = 10):
    query = text("""
        SELECT q.*, COUNT(a.id) as answer_count
        FROM questions q
        JOIN answers a ON q.id = a.question_id
        WHERE a.created_at > NOW() - INTERVAL '3 days'
        GROUP BY q.id
        ORDER BY answer_count DESC
        LIMIT :limit
    """)
    
    result = db.execute(query, {"limit": limit})
    questions = [dict(row) for row in result]
    
    return questions
