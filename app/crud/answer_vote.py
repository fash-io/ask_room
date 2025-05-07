from sqlalchemy.orm import Session
from uuid import UUID

from app.models import AnswerVote, Answer, User, VoteValue
from app.schemas.vote import VoteCreate


def create_answer_vote(db: Session, vote_data: VoteCreate, user_id: UUID):
    # Ensure the answer exists
    if not vote_data.answer_id:
        return {"message": "Answer ID is required"}
        
    answer = db.query(Answer).filter(Answer.id == vote_data.answer_id).first()
    if not answer:
        return {"message": "Answer not found"}
    
    # Check if user has already voted on this answer
    existing_vote = (
        db.query(AnswerVote)
        .filter(AnswerVote.answer_id == vote_data.answer_id, AnswerVote.user_id == user_id)
        .first()
    )
    
    # Convert string enum to database enum
    vote_value = VoteValue.up if vote_data.vote_value == "up" else VoteValue.down
    
    if existing_vote:
        # If vote is the same, return message
        if existing_vote.vote_value.name == vote_data.vote_value:
            return {"message": f"You have already {vote_data.vote_value}voted this answer"}
        
        # Update existing vote
        existing_vote.vote_value = vote_value
        db.commit()
        db.refresh(existing_vote)
        return {"message": f"Vote changed to {vote_data.vote_value}vote"}
    
    # Create new vote
    vote = AnswerVote(
        user_id=user_id,
        answer_id=vote_data.answer_id,
        vote_value=vote_value,
    )
    db.add(vote)
    db.commit()
    db.refresh(vote)

    # Update user reputation
    answer_author = db.query(User).filter(User.id == answer.author_id).first()
    if answer_author:
        # Upvote increases reputation by 10, downvote decreases by 2
        if vote_data.vote_value == "up":
            answer_author.reputation += 10
        else:
            answer_author.reputation = max(0, answer_author.reputation - 2)
        db.commit()

    return {"message": f"{vote_data.vote_value.capitalize()}voted successfully"}


def update_answer_vote(db: Session, vote_id: UUID, vote_data: VoteCreate):
    # Update an existing vote entry
    vote = db.query(AnswerVote).filter(AnswerVote.id == vote_id).first()
    if vote:
        # Convert string enum to database enum
        vote_value = VoteValue.up if vote_data.vote_value == "up" else VoteValue.down
        vote.vote_value = vote_value
        db.commit()
        db.refresh(vote)
        return {"message": "Vote updated successfully"}
    return {"message": "Vote not found"}


def get_answer_votes(db: Session, answer_id: UUID):
    # Retrieve all votes for a specific answer
    votes = db.query(AnswerVote).filter(AnswerVote.answer_id == answer_id).all()
    return [{"user_id": vote.user_id, "vote_value": vote.vote_value.name} for vote in votes]


def get_user_vote_on_answer(db: Session, answer_id: UUID, user_id: UUID):
    # Get the vote by a user on a specific answer
    vote = db.query(AnswerVote).filter(AnswerVote.answer_id == answer_id, AnswerVote.user_id == user_id).first()
    if vote:
        return {"vote_value": vote.vote_value.name}
    return {"message": "No vote found"}


def delete_answer_vote(db: Session, vote_id: UUID):
    # Delete a specific vote on a answer
    vote = db.query(AnswerVote).filter(AnswerVote.id == vote_id).first()
    if vote:
        db.delete(vote)
        db.commit()
        return {"message": "Vote deleted successfully"}
    return {"message": "Vote not found"}
