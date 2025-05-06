from fastapi import FastAPI, APIRouter, Depends
from sqlalchemy.orm import Session

from app.routes import badges, answers, category, questions, tag, users, votes
from app.dependencies import get_db
from app.crud import question as crud_question, user as crud_users, tag as crud_tags
from app.models import User
from app.database import SessionLocal

app = FastAPI()
router = APIRouter()

# Include feature routers
app.include_router(badges.router, prefix="/api/badges", tags=["Badges"])
app.include_router(answers.router, prefix="/api/answers", tags=["Answer"])
app.include_router(category.router, prefix="/api/categories", tags=["Category"])
app.include_router(questions.router, prefix="/api/questions", tags=["Question"])
app.include_router(tag.router, prefix="/api/tags", tags=["Tag"])
app.include_router(users.router, prefix="/api/users", tags=["User"])
app.include_router(votes.router, prefix="/votes", tags=["QuestionVote", "AnswerVote"])

# Add search route
@router.get("/search/{query}", tags=["Search"])
def get_search(query: str, db: Session = Depends(get_db)):
    questions = crud_question.search_questions_pg_trgm(db, query)
    users = crud_users.get_users_fuzzy(db, query)
    tags = crud_tags.get_tags_fuzzy(db, query)
    return {"questions": questions, "users": users, "tags": tags}

# ✅ Include the search router
app.include_router(router)

def create_test_user(db: Session):
    if db.query(User).first():  # Check if user exists
        user = User(id="test-id", username="testuser", email="test@example.com", role="admin")
        db.add(user)
        db.commit()
        db.refresh(user)
        
if __name__ == "__main__":
    db = SessionLocal()
    create_test_user(db)