from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID

from app.crud.answer import (
    create_answer as create_answer_crud,
    get_answer_by_id as get_answer_by_id_crud,
    get_answers_by_question,
    get_answers_by_user,
    upvote_answer as upvote_answer_crud,
    downvote_answer as downvote_answer_crud,
    get_votes_for_answer,
    update_answer as update_answer_crud,
    delete_answer as delete_answer_crud,
    update_answer_helpful as update_answer_helpful_crud,
)
from app.models import Answer
from app.schemas.answer import AnswerCreate, AnswerOut
from app.dependencies import get_db, get_current_user

router = APIRouter()

@router.post("/", response_model=AnswerOut)
def create_answer_handler(answer: AnswerCreate, db: Session = Depends(get_db), user_id: UUID = Depends(get_current_user)):
    try:
        new_answer = create_answer_crud(db, answer, user_id)
        from app.services.badges import check_and_award_badges
        from app.crud.user import get_user_by_id
        user = get_user_by_id(db, user_id)
        check_and_award_badges(db, user)
        return new_answer
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/{answer_id}", response_model=AnswerOut)
def get_answer_handler(answer_id: UUID, db: Session = Depends(get_db)):
    answer = get_answer_by_id_crud(db, answer_id)
    if not answer:
        raise HTTPException(status_code=404, detail="Answer not found")
    return answer

@router.get("/question/{question_id}", response_model=list[AnswerOut])
def get_answers_by_question_handler(question_id: UUID, db: Session = Depends(get_db)):
    return get_answers_by_question(db, question_id)

@router.get("/user/{user_id}", response_model=list[AnswerOut])
def get_answers_by_user_handler(user_id: UUID, db: Session = Depends(get_db)):
    return get_answers_by_user(db, user_id)

@router.post("/{answer_id}/upvote")
def upvote_answer_handler(answer_id: UUID, db: Session = Depends(get_db), user_id: UUID = Depends(get_current_user)):
    return upvote_answer_crud(db, answer_id, user_id)

@router.post("/{answer_id}/downvote")
def downvote_answer_handler(answer_id: UUID, db: Session = Depends(get_db), user_id: UUID = Depends(get_current_user)):
    return downvote_answer_crud(db, answer_id, user_id)

@router.get("/{answer_id}/votes")
def get_votes_handler(answer_id: UUID, db: Session = Depends(get_db)):
    return get_votes_for_answer(db, answer_id)

@router.put("/{answer_id}", response_model=AnswerOut)
def update_answer_handler(answer_id: UUID, answer: AnswerCreate, db: Session = Depends(get_db)):
    updated = update_answer_crud(db, answer_id, answer)
    if not updated:
        raise HTTPException(status_code=404, detail="Answer not found")
    return updated

@router.delete("/{answer_id}")
def delete_answer_handler(answer_id: UUID, db: Session = Depends(get_db)):
    success = delete_answer_crud(db, answer_id)
    if not success:
        raise HTTPException(status_code=404, detail="Answer not found")
    return {"message": "Answer deleted"}

@router.put("/{answer_id}/helpful")
def mark_answer_helpful_handler(answer_id: UUID, is_helpful: bool, db: Session = Depends(get_db)):
    answer = db.query(Answer).filter(Answer.id == answer_id).first()
    if not answer:
        raise HTTPException(status_code=404, detail="Answer not found")
    return update_answer_helpful_crud(db, answer, is_helpful)
