from fastapi import FastAPI, APIRouter, Depends, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app.routes import badges, answers, category, questions, tag, users, votes, notifications
from app.dependencies import get_db
from app.crud import question as crud_question, user as crud_users, tag as crud_tags
from app.models import User
from app.database import SessionLocal
from app.health import router as health_router
from app.middleware.rate_limiter import standard_limiter, search_limiter

app = FastAPI(
    title="Q&A API",
    description="API for a Q&A platform similar to Stack Overflow",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def add_request_id(request: Request, call_next):
    import uuid
    request_id = str(uuid.uuid4())
    response = await call_next(request)
    response.headers["X-Request-ID"] = request_id
    return response

# Add response time middleware
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    import time
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

router = APIRouter()

app.include_router(badges.router, prefix="/api/badges", tags=["Badges"])
app.include_router(answers.router, prefix="/api/answers", tags=["Answer"])
app.include_router(category.router, prefix="/api/categories", tags=["Category"])
app.include_router(questions.router, prefix="/api/questions", tags=["Question"])
app.include_router(tag.router, prefix="/api/tags", tags=["Tag"])
app.include_router(users.router, prefix="/api/users", tags=["User"])
app.include_router(votes.router, prefix="/api/votes", tags=["QuestionVote", "AnswerVote"])
app.include_router(notifications.router, prefix="/api/notifications", tags=["Notifications"])
app.include_router(health_router, tags=["Health"])

@router.get("/search", tags=["Search"], dependencies=[Depends(search_limiter)])
def get_search(query: str, db: Session = Depends(get_db)):
    questions = crud_question.search_questions_full_text(db, query)
    users = crud_users.get_users_fuzzy(db, query)
    tags = crud_tags.get_tags_fuzzy(db, query)
    return {"questions": questions, "users": users, "tags": tags}

app.include_router(router)

@app.get("/", tags=["Root"])
def read_root():
    return {
        "message": "Welcome to the Q&A API",
        "version": "1.0.0",
        "docs_url": "/docs",
        "redoc_url": "/redoc"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
