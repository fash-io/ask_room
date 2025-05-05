from models import Answer, Question
from schemas.answer import AnswerCreate
from sqlalchemy.orm import Session
from uuid import UUID


def create_answer(db: Session, answer_data: AnswerCreate, user_id: UUID):
    question = db.query(Question).filter(Question.id == answer_data.question_id).first()
    if question is None:
        raise ValueError("Question not found")
    answer = Answer(
        question_id=answer_data.question_id,
        body=answer_data.body,
        author_id=user_id,
    )
    db.add(answer)
    db.commit()
    db.refresh(answer)
    return answer
