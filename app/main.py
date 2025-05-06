from fastapi import FastAPI, APIRouter, Depends, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app.routes import (
    badges,
    answers,
    category,
    questions,
    tag,
    users,
    votes,
    notifications,
)
from app.database import get_db
from app.crud import question as crud_question, user as crud_users, tag as crud_tags
from app.health import router as health_router
from aioredis import from_url, Redis
from app.middleware.rate_limiter import RateLimiter
import os

app = FastAPI(
    title="Q&A API",
    description="API for a Q&A platform similar to Stack Overflow",
    version="1.0.0",
)


@app.on_event("startup")
async def startup():
    # Create a single Redis pool
    redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    app.state.redis: Redis = await from_url(
        redis_url, encoding="utf8", decode_responses=True
    )
    # Optionally test the connection
    await app.state.redis.ping()


@app.on_event("shutdown")
async def shutdown():
    await app.state.redis.close()
    await app.state.redis.wait_closed()


question_limiter = RateLimiter(times=60, seconds=60)
auth_limiter = RateLimiter(times=10, seconds=60)
search_limiter = RateLimiter(times=30, seconds=60)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update this with your frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Add request ID middleware
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

# Include feature routers
app.include_router(badges.router, prefix="/api/badges", tags=["Badges"])
app.include_router(answers.router, prefix="/api/answers", tags=["Answer"])
app.include_router(category.router, prefix="/api/categories", tags=["Category"])
app.include_router(
    questions.router,
    prefix="/api/questions",
    tags=["Question"],
    dependencies=[Depends(question_limiter)],
)
app.include_router(tag.router, prefix="/api/tags", tags=["Tag"])
app.include_router(users.router, prefix="/api/users", tags=["User"])
app.include_router(
    votes.router, prefix="/api/votes", tags=["QuestionVote", "AnswerVote"]
)
app.include_router(
    notifications.router, prefix="/api/notifications", tags=["Notifications"]
)
app.include_router(health_router, tags=["Health"])


# Add search route with rate limiting
@router.get("/search", tags=["Search"], dependencies=[Depends(search_limiter)])
def get_search(query: str, db: Session = Depends(get_db)):
    questions = crud_question.search_questions_full_text(db, query)
    users = crud_users.get_users_fuzzy(db, query)
    tags = crud_tags.get_tags_fuzzy(db, query)
    return {"questions": questions, "users": users, "tags": tags}


# Include the search router
app.include_router(router)


@app.get("/", tags=["Root"])
def read_root():
    return {
        "message": "Welcome to the Q&A API",
        "version": "1.0.0",
        "docs_url": "/docs",
        "redoc_url": "/redoc",
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
