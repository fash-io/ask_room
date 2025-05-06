from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID

from app.crud import question as crud_question
from app.schemas.question import Question, QuestionCreate, QuestionOut, PaginatedQuestions
from app.dependencies import get_db

router = APIRouter()

@router.post("/", response_model=QuestionOut)
def create_question_handler(question: QuestionCreate, db: Session = Depends(get_db)):
    try:
        return crud_question.create_question(db, **question.dict())
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Annotated

@router.get("/", response_model=PaginatedQuestions)
def get_questions(
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(gt=0, le=100)] = 10,
    db: Session = Depends(get_db)
):
    return crud_question.get_all_questions(db, skip=skip, limit=limit)

@router.get("/{question_id}", response_model=QuestionOut)
def get_question_by_id(question_id: UUID, db: Session = Depends(get_db)):
    question = crud_question.get_question_by_id(db, question_id)
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    return question

@router.put("/{question_id}", response_model=QuestionOut)
def update_question_handler(question_id: UUID, question: Question, db: Session = Depends(get_db)):
    try:
        return crud_question.update_question(db, question_id, **question.dict())
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{question_id}")
def delete_question_handler(question_id: UUID, db: Session = Depends(get_db)):
    success = crud_question.delete_question(db, question_id)
    if not success:
        raise HTTPException(status_code=404, detail="Question not found")
    return {"message": "Deleted"}

@router.get("/category/{category_id}", response_model=PaginatedQuestions)
def get_questions_by_category_handler(category_id: UUID, db: Session = Depends(get_db)):
    return crud_question.get_questions_by_category(db, category_id)

@router.get("/tag/{tag_id}", response_model=PaginatedQuestions)
def get_questions_by_tag_handler(tag_id: UUID, db: Session = Depends(get_db)):
    return crud_question.get_questions_by_tag(db, tag_id)

@router.get("/search/{query}", response_model=PaginatedQuestions)
def search_questions(query: str, db: Session = Depends(get_db)):
    return crud_question.search_questions_pg_trgm(db, query)

@router.get("/user/{user_id}", response_model=PaginatedQuestions)
def get_questions_by_user_handler(user_id: UUID, db: Session = Depends(get_db)):
    return crud_question.get_questions_by_user(db, user_id)

