from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.dependencies import get_db

router = APIRouter()

@router.get("/health")
def health_check(db: Session = Depends(get_db)):
    """
    Health check endpoint to verify the API and database are working.
    Returns the current database timestamp and connection status.
    """
    try:
        # Test database connection
        result = db.execute(text("SELECT NOW()"))
        timestamp = result.scalar_one()
        
        return {
            "status": "healthy",
            "database": "connected",
            "timestamp": timestamp,
            "message": "API is operational"
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "database": "disconnected",
            "error": str(e),
            "message": "Database connection failed"
        }
