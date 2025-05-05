import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base

load_dotenv()

USER     = os.getenv("user")
PASSWORD = os.getenv("password")
HOST     = os.getenv("host")
PORT     = os.getenv("port")
DBNAME   = os.getenv("dbname")

DATABASE_URL = (
    f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}"
    "?sslmode=require"
)

engine = create_engine(DATABASE_URL, echo=False)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

# 3) Base class for your models
Base = declarative_base()

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
