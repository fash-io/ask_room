from sqlalchemy.orm import Session
from uuid import UUID

from app.models import QuestionVote, VoteValue
from app.schemas.vote import VoteCreate


def create_question_vote(db: Session, vote_data: VoteCreate, user_id: UUID):
    # Ensure the question exists
    existing_vote = (
        db.query(QuestionVote)
        .filter(QuestionVote.question_id == vote_data.question_id, QuestionVote.user_id == user_id)
        .first()
    )
    if existing_vote:
        return {"message": "You have already voted on this question"}

    # Create a new vote entry
    vote = QuestionVote(
        user_id=user_id,
        question_id=vote_data.question_id,
        vote_value=vote_data.vote_value,
    )
    db.add(vote)
    db.commit()
    db.refresh(vote)

    return {"message": "Vote recorded successfully"}


def update_question_vote(db: Session, vote_id: UUID, vote_data: VoteCreate):
    # Update an existing vote entry
    vote = db.query(QuestionVote).filter(QuestionVote.id == vote_id).first()
    if vote:
        vote.vote_value = vote_data.vote_value
        db.commit()
        db.refresh(vote)
        return {"message": "Vote updated successfully"}
    return {"message": "Vote not found"}


def get_question_votes(db: Session, question_id: UUID):
    # Retrieve all votes for a specific question
    votes = db.query(QuestionVote).filter(QuestionVote.question_id == question_id).all()
    return [{"user_id": vote.user_id, "vote_value": vote.vote_value} for vote in votes]


def get_user_vote_on_question(db: Session, question_id: UUID, user_id: UUID):
    # Get the vote by a user on a specific question
    vote = db.query(QuestionVote).filter(QuestionVote.question_id == question_id, QuestionVote.user_id == user_id).first()
    if vote:
        return {"vote_value": vote.vote_value}
    return {"message": "No vote found"}


def delete_question_vote(db: Session, vote_id: UUID):
    # Delete a specific vote on a question
    vote = db.query(QuestionVote).filter(QuestionVote.id == vote_id).first()
    if vote:
        db.delete(vote)
        db.commit()
        return {"message": "Vote deleted successfully"}
    return {"message": "Vote not found"}
