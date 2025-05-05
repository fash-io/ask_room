from sqlalchemy.orm import Session
from uuid import UUID

from app.schemas.answer import AnswerCreate
from app.models import Answer, Question, AnswerVote, VoteValue

def create_answer(db: Session, answer_data: AnswerCreate, user_id: UUID):
    # Ensure the question exists
    question = db.query(Question).filter(Question.id == answer_data.question_id).first()
    if question is None:
        raise ValueError("Question not found")

    # Create a new answer and add it to the database
    answer = Answer(
        question_id=answer_data.question_id,
        body=answer_data.body,
        author_id=user_id,
    )
    db.add(answer)
    db.commit()
    db.refresh(answer)
    return answer


def get_answer_by_id(db: Session, answer_id: UUID):
    # Retrieve an answer by ID and include vote details
    answer = db.query(Answer).filter(Answer.id == answer_id).first()

    if answer:
        # Get upvotes and downvotes for the answer using the Vote model
        upvotes = (
            db.query(AnswerVote)
            .filter(AnswerVote.answer_id == answer_id, AnswerVote.vote_value == VoteValue.up)
            .count()
        )
        downvotes = (
            db.query(AnswerVote)
            .filter(AnswerVote.answer_id == answer_id, AnswerVote.vote_value == VoteValue.down)
            .count()
        )

        # Include the vote counts in the answer object
        answer.upvotes = upvotes
        answer.downvotes = downvotes

        return answer
    return None


def get_answers_by_question(db: Session, question_id: UUID):
    # Retrieve all answers for a given question
    return db.query(Answer).filter(Answer.question_id == question_id).all()


def get_answers_by_user(db: Session, user_id: UUID):
    # Retrieve all answers by a specific user
    return db.query(Answer).filter(Answer.author_id == user_id).all()


def upvote_answer(db: Session, answer_id: UUID, user_id: UUID):
    # Check if the user has already voted on this answer
    existing_vote = (
        db.query(AnswerVote)
        .filter(AnswerVote.answer_id == answer_id, AnswerVote.user_id == user_id)
        .first()
    )

    if existing_vote:
        if existing_vote.vote_value == VoteValue.up:
            return {"message": "You have already upvoted this answer"}
        elif existing_vote.vote_value == VoteValue.down:
            # Change downvote to upvote
            existing_vote.vote_value = VoteValue.up
            db.commit()
            return {"message": "Downvote changed to upvote"}

    # Create a new upvote entry if no existing vote
    vote = AnswerVote(answer_id=answer_id, user_id=user_id, vote_value=VoteValue.up)
    db.add(vote)
    db.commit()
    db.refresh(vote)

    return {"message": "Upvoted successfully"}


def downvote_answer(db: Session, answer_id: UUID, user_id: UUID):
    # Check if the user has already voted on this answer
    existing_vote = (
        db.query(AnswerVote)
        .filter(AnswerVote.answer_id == answer_id, AnswerVote.user_id == user_id)
        .first()
    )

    if existing_vote:
        if existing_vote.vote_value == VoteValue.down:
            return {"message": "You have already downvoted this answer"}
        elif existing_vote.vote_value == VoteValue.up:
            # Change upvote to downvote
            existing_vote.vote_value = VoteValue.down
            db.commit()
            return {"message": "Upvote changed to downvote"}

    # Create a new downvote entry if no existing vote
    vote = AnswerVote(answer_id=answer_id, user_id=user_id, vote_value=VoteValue.down)
    db.add(vote)
    db.commit()
    db.refresh(vote)

    return {"message": "Downvoted successfully"}


def get_votes_for_answer(db: Session, answer_id: UUID):
    # Get the total upvotes and downvotes for an answer
    upvotes = (
        db.query(AnswerVote)
        .filter(AnswerVote.answer_id == answer_id, AnswerVote.vote_value == VoteValue.up)
        .count()
    )
    downvotes = (
        db.query(AnswerVote)
        .filter(AnswerVote.answer_id == answer_id, AnswerVote.vote_value == VoteValue.down)
        .count()
    )
    return {"upvotes": upvotes, "downvotes": downvotes}


def update_answer(db: Session, answer_id: UUID, answer_data: AnswerCreate):
    # Update an answer's content
    answer = db.query(Answer).filter(Answer.id == answer_id).first()
    if answer:
        answer.body = answer_data.body
        db.commit()
        db.refresh(answer)
        return answer
    return None


def delete_answer(db: Session, answer_id: UUID):
    # Delete an answer
    answer = db.query(Answer).filter(Answer.id == answer_id).first()
    if answer:
        db.delete(answer)
        db.commit()
        return True
    return False

def update_answer_helpful(db: Session, answer: Answer, is_helpful: bool):
    answer.is_helpful = is_helpful
    db.commit()
    db.refresh(answer)
    return answer