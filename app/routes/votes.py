from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from uuid import UUID
from typing import  Annotated

from app.dependencies import get_db, get_current_user
from app.schemas.vote import VoteCreate
from app.schemas.answer import AnswerOut
from app.schemas.question import QuestionOut
from app.crud import answer_vote, question_vote

router = APIRouter()


@router.post("/answers/{answer_id}", response_model=AnswerOut)
def upvote_answer_handler(
    vote_data: Annotated[VoteCreate, Depends(VoteCreate.Config)],
    db: Session = Depends(get_db),
    user_id: UUID = Depends(get_current_user),
):
    return answer_vote.create_answer_vote(db, vote_data, user_id)


@router.post("/questions/{question_id}", response_model=QuestionOut)
def upvote_question_handler(
    vote_data: Annotated[VoteCreate, Depends(VoteCreate.Config)],
    db: Session = Depends(get_db),
    user_id: UUID = Depends(get_current_user),
):
    return question_vote.create_question_vote(db, vote_data, user_id)


@router.put("/answers/{answer_id}", response_model=AnswerOut)
def update_answer_vote_handler(
    vote_data: Annotated[VoteCreate, Depends(VoteCreate.Config)],
    db: Session = Depends(get_db),
    user_id: UUID = Depends(get_current_user),
):
    return answer_vote.update_answer_vote(db, vote_data, user_id)


@router.put("/questions/{question_id}", response_model=QuestionOut)
def update_question_vote_handler(
    vote_data: Annotated[VoteCreate, Depends(VoteCreate.Config)],
    db: Session = Depends(get_db),
    user_id: UUID = Depends(get_current_user),
):
    return question_vote.update_question_vote(db, vote_data, user_id)


@router.get("/answers/{answer_id}", response_model=AnswerOut)
def get_answer_votes_handler(answer_id: UUID, db: Session = Depends(get_db)):
    return answer_vote.get_answer_votes(db, answer_id)


@router.get("/questions/{question_id}", response_model=QuestionOut)
def get_question_votes_handler(question_id: UUID, db: Session = Depends(get_db)):
    return question_vote.get_question_votes(db, question_id)


@router.delete("/answers/{vote_id}")
def delete_answer_vote_handler(
    vote_id: UUID,
    db: Session = Depends(get_db),
):
    return answer_vote.delete_answer_vote(db, vote_id)


@router.delete("/questions/{vote_id}")
def delete_question_vote_handler(
    vote_id: UUID,
    db: Session = Depends(get_db),
):
    return question_vote.delete_question_vote(db, vote_id)
