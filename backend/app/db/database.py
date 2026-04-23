from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

# For development, use SQLite if POSTGRES_URL is not set
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./mentornet.db")

if SQLALCHEMY_DATABASE_URL.startswith("sqlite"):
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
    )
else:
    engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

from app.db.base_class import Base

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
