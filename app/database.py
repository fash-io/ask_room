import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.pool import QueuePool

# Get Neon connection details from environment variables
# These are automatically set by Vercel when you add the Neon integration
DATABASE_URL = os.environ.get("DATABASE_URL")
POOLED_DATABASE_URL = os.environ.get("POSTGRES_URL")  # This includes the pooler

# Check if we're in production or development
IS_PRODUCTION = os.environ.get("ENVIRONMENT", "development") == "production"

# For production: Use connection pooling
if IS_PRODUCTION:
    # Connection pooling configuration
    engine = create_engine(
        POOLED_DATABASE_URL,
        poolclass=QueuePool,
        pool_size=10,  # Maintain 10 connections in the pool
        max_overflow=20,  # Allow up to 20 additional connections when needed
        pool_timeout=30,  # Wait up to 30 seconds to get a connection
        pool_recycle=1800,  # Recycle connections after 30 minutes
        echo=False
    )
    print("✅ Using connection pooling for production")
# For development: Use direct connection
else:
    # For development, we use a simpler configuration without extensive pooling
    engine = create_engine(DATABASE_URL, echo=True)  # echo=True for SQL logging in development
    print("✅ Using direct connection for development")

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

# Base class for your models
Base = declarative_base()

# Database connection test
try:
    with engine.connect() as connection:
        print("✅ Connection successful!")
        
        # Use SQLAlchemy's execution API
        result = connection.execute(text("SELECT NOW()"))
        now = result.scalar_one()
        print("Current Time:", now)
        
    print("🔒 Connection closed.")
except Exception as e:
    print(f"❌ Failed to connect: {e}")

def get_db():
    """
    Dependency function to get a database session.
    This creates a new database session for each request and closes it when the request is done.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
