from sqlalchemy.orm import Session
from uuid import UUID

from app.models import QuestionVote, Question, User, VoteValue
from app.schemas.vote import VoteCreate


def create_question_vote(db: Session, vote_data: VoteCreate, user_id: UUID):
    # Ensure the question exists
    if not vote_data.question_id:
        return {"message": "Question ID is required"}
        
    question = db.query(Question).filter(Question.id == vote_data.question_id).first()
    if not question:
        return {"message": "Question not found"}
    
    # Check if user has already voted on this question
    existing_vote = (
        db.query(QuestionVote)
        .filter(QuestionVote.question_id == vote_data.question_id, QuestionVote.user_id == user_id)
        .first()
    )
    
    # Convert string enum to database enum
    vote_value = VoteValue.up if vote_data.vote_value == "up" else VoteValue.down
    
    if existing_vote:
        # If vote is the same, return message
        if existing_vote.vote_value.name == vote_data.vote_value:
            return {"message": f"You have already {vote_data.vote_value}voted this question"}
        
        # Update existing vote
        existing_vote.vote_value = vote_value
        db.commit()
        db.refresh(existing_vote)
        return {"message": f"Vote changed to {vote_data.vote_value}vote"}
    
    # Create new vote
    vote = QuestionVote(
        user_id=user_id,
        question_id=vote_data.question_id,
        vote_value=vote_value,
    )
    db.add(vote)
    db.commit()
    db.refresh(vote)

    # Update user reputation
    question_author = db.query(User).filter(User.id == question.author_id).first()
    if question_author:
        # Upvote increases reputation by 5, downvote decreases by 1
        if vote_data.vote_value == "up":
            question_author.reputation += 5
        else:
            question_author.reputation = max(0, question_author.reputation - 1)
        db.commit()

    return {"message": f"{vote_data.vote_value.capitalize()}voted successfully"}


def update_question_vote(db: Session, vote_id: UUID, vote_data: VoteCreate):
    # Update an existing vote entry
    vote = db.query(QuestionVote).filter(QuestionVote.id == vote_id).first()
    if vote:
        # Convert string enum to database enum
        vote_value = VoteValue.up if vote_data.vote_value == "up" else VoteValue.down
        vote.vote_value = vote_value
        db.commit()
        db.refresh(vote)
        return {"message": "Vote updated successfully"}
    return {"message": "Vote not found"}


def get_question_votes(db: Session, question_id: UUID):
    # Retrieve all votes for a specific question
    votes = db.query(QuestionVote).filter(QuestionVote.question_id == question_id).all()
    return [{"user_id": vote.user_id, "vote_value": vote.vote_value.name} for vote in votes]


def get_user_vote_on_question(db: Session, question_id: UUID, user_id: UUID):
    # Get the vote by a user on a specific question
    vote = db.query(QuestionVote).filter(QuestionVote.question_id == question_id, QuestionVote.user_id == user_id).first()
    if vote:
        return {"vote_value": vote.vote_value.name}
    return {"message": "No vote found"}


def delete_question_vote(db: Session, vote_id: UUID):
    # Delete a specific vote on a question
    vote = db.query(QuestionVote).filter(QuestionVote.id == vote_id).first()
    if vote:
        db.delete(vote)
        db.commit()
        return {"message": "Vote deleted successfully"}
    return {"message": "Vote not found"}
