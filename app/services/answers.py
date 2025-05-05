from app.crud.answer import get_answer_by_id, update_answer_helpful
from app.crud.question import get_question_by_id
from app.services.badges import check_and_award_badges
from sqlalchemy.orm import Session
from uuid import UUID
from fastapi.exceptions import NotFound, Forbidden

def approve_answer(db: Session, answer_id: UUID, current_user_id: UUID):
    answer = get_answer_by_id(db, answer_id)
    if not answer:
        raise NotFound("Answer not found")

    # Ensure only the question author can approve
    question = get_question_by_id(db, answer.question_id)
    if question.author_id != current_user_id:
        raise Forbidden("You are not the author of this question")

    answer = update_answer_helpful(db, answer, True)
    awarded = check_and_award_badges(db, answer.author)

    return answer, awarded
