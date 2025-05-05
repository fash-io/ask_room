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
# Fetch variables
USER = os.getenv("user")
PASSWORD = os.getenv("password")
HOST = os.getenv("host")
PORT = os.getenv("port")
DBNAME = os.getenv("dbname")
# Create SQLAlchemy engine

DATABASE_URL = f"postgresql+psycopg2://{USER}:{PASSWORD}@db-attydxjiaoihvxjdqxeu:{PORT}/{DBNAME}?sslmode=require"

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

try:
    with engine.connect() as connection:
        print("Connection successful!")
except Exception as e:
    print(f"Failed to connect: {e}")