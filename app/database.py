"""
database.py

Sets up SQLAlchemy engine and session for connecting to Supabase Postgres via DATABASE_URL.
"""
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Read the DATABASE_URL environment variable
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL environment variable not set")

# Create SQLAlchemy engine
# echo=True will log all the SQL queries; turn off in production
engine = create_engine(
    DATABASE_URL,
    echo=True,
    future=True  # use SQLAlchemy 2.0 style
)

# Create a configured "Session" class
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    future=True
)

# Base class for ORM models
Base = declarative_base()

# Dependency to get DB session in FastAPI endpoints

def get_db():
    """
    Yield a SQLAlchemy database session, closing it after use.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
