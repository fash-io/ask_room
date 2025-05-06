from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from uuid import UUID
from typing import Optional, List, Annotated

from app.crud import question as crud_question
from app.schemas.question import QuestionCreate, QuestionOut, PaginatedQuestions
from app.dependencies import get_current_user
from app.database import get_db
from app.middleware.rate_limiter import standard_limiter

router = APIRouter()

@router.post("/", response_model=QuestionOut)
def create_question_handler(question: QuestionCreate, db: Session = Depends(get_db), current_user: UUID = Depends(get_current_user)):
    try:
        return crud_question.create_question(db, question, current_user)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=PaginatedQuestions)
def get_questions(
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(gt=0, le=100)] = 10,
    db: Session = Depends(get_db)
):
    return crud_question.get_all_questions(db, skip=skip, limit=limit)

@router.get("/trending", response_model=List[QuestionOut])
def get_trending_questions(
    limit: Annotated[int, Query(gt=0, le=50)] = 10,
    db: Session = Depends(get_db)
):
    """Get trending questions based on view count in the last week"""
    return crud_question.get_trending_questions(db, limit=limit)

@router.get("/hot", response_model=List[QuestionOut])
def get_hot_questions(
    limit: Annotated[int, Query(gt=0, le=50)] = 10,
    db: Session = Depends(get_db)
):
    """Get hot questions based on recent answer activity"""
    return crud_question.get_hot_questions(db, limit=limit)

@router.get("/{question_id}", response_model=QuestionOut)
def get_question_by_id(
    question_id: UUID, 
    increment_view: bool = True,
    db: Session = Depends(get_db)
):
    question = crud_question.get_question_by_id(db, question_id, increment_view=increment_view)
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    return question

@router.put("/{question_id}", response_model=QuestionOut)
def update_question_handler(
    question_id: UUID, 
    question: QuestionCreate, 
    db: Session = Depends(get_db),
    current_user: UUID = Depends(get_current_user)
):
    # First check if the user is the author of the question
    existing_question = crud_question.get_question_by_id(db, question_id, increment_view=False)
    if not existing_question:
        raise HTTPException(status_code=404, detail="Question not found")
    
    if str(existing_question.author_id) != str(current_user):
        raise HTTPException(status_code=403, detail="Not authorized to update this question")
    
    try:
        return crud_question.update_question(db, question_id, question)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{question_id}")
def delete_question_handler(
    question_id: UUID, 
    db: Session = Depends(get_db),
    current_user: UUID = Depends(get_current_user)
):
    # First check if the user is the author of the question
    existing_question = crud_question.get_question_by_id(db, question_id, increment_view=False)
    if not existing_question:
        raise HTTPException(status_code=404, detail="Question not found")
    
    if str(existing_question.author_id) != str(current_user):
        raise HTTPException(status_code=403, detail="Not authorized to delete this question")
    
    success = crud_question.delete_question(db, question_id)
    if not success:
        raise HTTPException(status_code=404, detail="Question not found")
    return {"message": "Question deleted successfully"}

@router.get("/category/{category_id}", response_model=PaginatedQuestions)
def get_questions_by_category_handler(
    category_id: UUID, 
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(gt=0, le=100)] = 10,
    db: Session = Depends(get_db)
):
    return crud_question.get_questions_by_category(db, category_id, skip=skip, limit=limit)

@router.get("/tag/{tag_id}", response_model=PaginatedQuestions)
def get_questions_by_tag_handler(
    tag_id: UUID, 
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(gt=0, le=100)] = 10,
    db: Session = Depends(get_db)
):
    return crud_question.get_questions_by_tag(db, tag_id, skip=skip, limit=limit)

@router.get("/search/{query}", response_model=List[QuestionOut], dependencies=[Depends(standard_limiter)])
def search_questions(
    query: str, 
    method: Optional[str] = "full-text",
    limit: Annotated[int, Query(gt=0, le=50)] = 20,
    db: Session = Depends(get_db)
):
    """
    Search questions using either full-text search or trigram similarity
    
    - method: 'full-text' (default) or 'trigram'
    """
    if method == "full-text":
        return crud_question.search_questions_full_text(db, query, limit=limit)
    else:
        return crud_question.search_questions_pg_trgm(db, query, limit=limit)

@router.get("/user/{user_id}", response_model=PaginatedQuestions)
def get_questions_by_user_handler(
    user_id: UUID, 
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(gt=0, le=100)] = 10,
    db: Session = Depends(get_db)
):
    return crud_question.get_questions_by_user(db, user_id, skip=skip, limit=limit)
