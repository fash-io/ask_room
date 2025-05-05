from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID

from app.crud import question as crud_question
from app.schemas.question import Question, QuestionCreate, QuestionOut
from app.dependencies import get_db

router = APIRouter()

@router.post("/", response_model=QuestionOut)
def create_question_handler(question: QuestionCreate, db: Session = Depends(get_db)):
    try:
        return crud_question.create_question(db, **question.dict())
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=list[QuestionOut])
def get_all_questions_handler(db: Session = Depends(get_db)):
    return crud_question.get_all_questions(db)

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

@router.get("/category/{category_id}", response_model=list[QuestionOut])
def get_questions_by_category_handler(category_id: UUID, db: Session = Depends(get_db)):
    return crud_question.get_questions_by_category(db, category_id)

@router.get("/tag/{tag_id}", response_model=list[QuestionOut])
def get_questions_by_tag_handler(tag_id: UUID, db: Session = Depends(get_db)):
    return crud_question.get_questions_by_tag(db, tag_id)

@router.get("/title/{title}", response_model=list[QuestionOut])
def get_questions_by_title_handler(title: str, db: Session = Depends(get_db)):
    return crud_question.get_questions_by_title(db, title)

@router.get("/user/{user_id}", response_model=list[QuestionOut])
def get_questions_by_user_handler(user_id: UUID, db: Session = Depends(get_db)):
    return crud_question.get_questions_by_user(db, user_id)

