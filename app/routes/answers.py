from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID
from typing import List

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
from app.models import Answer, User
from app.schemas.answer import AnswerCreate, AnswerOut
from app.dependencies import get_db, get_current_user
from app.services.badges import check_and_award_badges

router = APIRouter()

@router.post("/", response_model=AnswerOut, status_code=status.HTTP_201_CREATED)
def create_answer_handler(
    answer: AnswerCreate, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    """Create a new answer to a question"""
    try:
        new_answer = create_answer_crud(db, answer, current_user.id)
        
        check_and_award_badges(db, current_user)
        
        return new_answer
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/{answer_id}", response_model=AnswerOut)
def get_answer_handler(answer_id: UUID, db: Session = Depends(get_db)):
    """Get a specific answer by ID"""
    answer = get_answer_by_id_crud(db, answer_id)
    if not answer:
        raise HTTPException(status_code=404, detail="Answer not found")
    return answer

@router.get("/question/{question_id}", response_model=List[AnswerOut])
def get_answers_by_question_handler(question_id: UUID, db: Session = Depends(get_db)):
    """Get all answers for a specific question"""
    return get_answers_by_question(db, question_id)

@router.get("/user/{user_id}", response_model=List[AnswerOut])
def get_answers_by_user_handler(user_id: UUID, db: Session = Depends(get_db)):
    """Get all answers by a specific user"""
    return get_answers_by_user(db, user_id)

@router.post("/{answer_id}/upvote")
def upvote_answer_handler(
    answer_id: UUID, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    """Upvote an answer"""
    return upvote_answer_crud(db, answer_id, current_user.id)

@router.post("/{answer_id}/downvote")
def downvote_answer_handler(
    answer_id: UUID, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    """Downvote an answer"""
    return downvote_answer_crud(db, answer_id, current_user.id)

@router.get("/{answer_id}/votes")
def get_votes_handler(answer_id: UUID, db: Session = Depends(get_db)):
    """Get vote counts for an answer"""
    return get_votes_for_answer(db, answer_id)

@router.put("/{answer_id}", response_model=AnswerOut)
def update_answer_handler(
    answer_id: UUID, 
    answer: AnswerCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update an answer (only by the author)"""
    existing_answer = get_answer_by_id_crud(db, answer_id)
    if not existing_answer:
        raise HTTPException(status_code=404, detail="Answer not found")
    
    if str(existing_answer.author_id) != str(current_user.id):
        raise HTTPException(status_code=403, detail="Not authorized to update this answer")
    
    updated = update_answer_crud(db, answer_id, answer)
    if not updated:
        raise HTTPException(status_code=404, detail="Answer not found")
    return updated

@router.delete("/{answer_id}")
def delete_answer_handler(
    answer_id: UUID, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete an answer (only by the author)"""
    existing_answer = get_answer_by_id_crud(db, answer_id)
    if not existing_answer:
        raise HTTPException(status_code=404, detail="Answer not found")
    
    if str(existing_answer.author_id) != str(current_user.id):
        raise HTTPException(status_code=403, detail="Not authorized to delete this answer")
    
    success = delete_answer_crud(db, answer_id)
    if not success:
        raise HTTPException(status_code=404, detail="Answer not found")
    return {"message": "Answer deleted"}

@router.put("/{answer_id}/helpful")
def mark_answer_helpful_handler(
    answer_id: UUID, 
    is_helpful: bool, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Mark an answer as helpful (only by the question author)"""
    answer = db.query(Answer).filter(Answer.id == answer_id).first()
    if not answer:
        raise HTTPException(status_code=404, detail="Answer not found")
    # Get the question to check if current user is the author
    question = db.query(Answer).filter(Answer.id == answer.question_id).first()
    if not question or str(question.author_id) != str(current_user.id):
        raise HTTPException(status_code=403, detail="Only the question author can mark answers as helpful")
    
    updated_answer = update_answer_helpful_crud(db, answer, is_helpful)
    
    # Check for badges for the answer author
    answer_author = db.query(User).filter(User.id == answer.author_id).first()
    if answer_author:
        check_and_award_badges(db, answer_author)
    
    return updated_answer
