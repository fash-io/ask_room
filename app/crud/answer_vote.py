from sqlalchemy.orm import Session
from uuid import UUID

from app.models import AnswerVote
from app.schemas.vote import VoteCreate


def create_answer_vote(db: Session, vote_data: VoteCreate, user_id: UUID):
    existing_vote = (
        db.query(AnswerVote)
        .filter(AnswerVote.answer_id == vote_data.answer_id, AnswerVote.user_id == user_id)
        .first()
    )
    
    if existing_vote and existing_vote.vote_value == vote_data.vote_value:
        return {"message": "You have already voted on this answer"}

    if existing_vote and existing_vote.vote_value != vote_data.vote_value:
        update_answer_vote(db, existing_vote.id, vote_data)

    vote = AnswerVote(
        user_id=user_id,
        answer_id=vote_data.answer_id,
        vote_value=vote_data.vote_value,
    )
    db.add(vote)
    db.commit()
    db.refresh(vote)

    return {"message": "Vote recorded successfully"}


def update_answer_vote(db: Session, vote_id: UUID, vote_data: VoteCreate):
    # Update an existing vote entry
    vote = db.query(AnswerVote).filter(AnswerVote.id == vote_id).first()
    if vote:
        vote.vote_value = vote_data.vote_value
        db.commit()
        db.refresh(vote)
        return {"message": "Vote updated successfully"}
    return {"message": "Vote not found"}


def get_answer_votes(db: Session, answer_id: UUID):
    # Retrieve all votes for a specific answer
    votes = db.query(AnswerVote).filter(AnswerVote.answer_id == answer_id).all()
    return [{"user_id": vote.user_id, "vote_value": vote.vote_value} for vote in votes]


def get_user_vote_on_answer(db: Session, answer_id: UUID, user_id: UUID):
    # Get the vote by a user on a specific answer
    vote = db.query(AnswerVote).filter(AnswerVote.answer_id == answer_id, AnswerVote.user_id == user_id).first()
    if vote:
        return {"vote_value": vote.vote_value}
    return {"message": "No vote found"}


def delete_answer_vote(db: Session, vote_id: UUID):
    # Delete a specific vote on a answer
    vote = db.query(AnswerVote).filter(AnswerVote.id == vote_id).first()
    if vote:
        db.delete(vote)
        db.commit()
        return {"message": "Vote deleted successfully"}
    return {"message": "Vote not found"}
