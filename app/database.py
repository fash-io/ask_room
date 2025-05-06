from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.pool import QueuePool, NullPool
from dotenv import load_dotenv
import os

load_dotenv()

DB_USER = os.environ.get("DB_USER", "postgres.attydxjiaoihvxjdqxeu")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "4WDGBD5YHVDsZXLg")
DB_HOST = os.environ.get("DB_HOST", "aws-0-eu-central-1.pooler.supabase.com")
DB_PORT = os.environ.get("DB_PORT", "5432")
DB_NAME = os.environ.get("DB_NAME", "postgres")

DATABASE_URL = (
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    "?sslmode=require"
)

IS_PRODUCTION = os.environ.get("ENVIRONMENT", "development") == "production"

if IS_PRODUCTION:
    engine = create_engine(
        DATABASE_URL,
        poolclass=QueuePool,
        pool_size=10,  
        max_overflow=20,  
        pool_timeout=30, 
        pool_recycle=1800,  
        echo=False
    )
    print("✅ Using connection pooling for production")
else:
    engine = create_engine(DATABASE_URL, echo=True, poolclass=NullPool) 
    print("✅ Using direct connection for development")

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

Base = declarative_base()

try:
    with engine.connect() as connection:
        print("✅ Connection successful!")
        
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