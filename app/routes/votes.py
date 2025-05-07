from fastapi import APIRouter, Depends, HTTPException, Body, Request
from sqlalchemy.orm import Session
from uuid import UUID
from typing import Dict, Any

from app.dependencies import get_db, get_current_user
from app.schemas.vote import VoteCreate
from app.crud import answer_vote, question_vote

router = APIRouter()


@router.post("/answers/{answer_id}")
async def vote_answer(
    answer_id: UUID,
    vote_value: str = Body(..., embed=True),
    db: Session = Depends(get_db),
    current_user: UUID = Depends(get_current_user),
):
    """Vote on an answer (upvote or downvote)"""
    vote_data = VoteCreate(answer_id=answer_id, vote_value=vote_value)
    return answer_vote.create_answer_vote(db, vote_data, current_user)


@router.post("/questions/{question_id}")
async def vote_question(
    question_id: UUID,
    vote_value: str = Body(..., embed=True),
    db: Session = Depends(get_db),
    current_user: UUID = Depends(get_current_user),
):
    """Vote on a question (upvote or downvote)"""
    vote_data = VoteCreate(question_id=question_id, vote_value=vote_value)
    return question_vote.create_question_vote(db, vote_data, current_user)


@router.get("/answers/{answer_id}")
async def get_answer_votes_handler(
    answer_id: UUID, 
    db: Session = Depends(get_db)
):
    """Get all votes for an answer"""
    return answer_vote.get_answer_votes(db, answer_id)


@router.get("/questions/{question_id}")
async def get_question_votes_handler(
    question_id: UUID, 
    db: Session = Depends(get_db)
):
    """Get all votes for a question"""
    return question_vote.get_question_votes(db, question_id)


@router.get("/answers/{answer_id}/user")
async def get_user_vote_on_answer_handler(
    answer_id: UUID, 
    db: Session = Depends(get_db),
    current_user: UUID = Depends(get_current_user),
):
    """Get the current user's vote on an answer"""
    return answer_vote.get_user_vote_on_answer(db, answer_id, current_user)


@router.get("/questions/{question_id}/user")
async def get_user_vote_on_question_handler(
    question_id: UUID, 
    db: Session = Depends(get_db),
    current_user: UUID = Depends(get_current_user),
):
    """Get the current user's vote on a question"""
    return question_vote.get_user_vote_on_question(db, question_id, current_user)


@router.delete("/answers/{vote_id}")
async def delete_answer_vote_handler(
    vote_id: UUID,
    db: Session = Depends(get_db),
    current_user: UUID = Depends(get_current_user),
):
    """Delete a vote on an answer"""
    return answer_vote.delete_answer_vote(db, vote_id)


@router.delete("/questions/{vote_id}")
async def delete_question_vote_handler(
    vote_id: UUID,
    db: Session = Depends(get_db),
    current_user: UUID = Depends(get_current_user),
):
    """Delete a vote on a question"""
    return question_vote.delete_question_vote(db, vote_id)
