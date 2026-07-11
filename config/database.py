"""
Database configuration.

Responsibilities:
1. Create the SQLite engine.
2. Create database sessions.
3. Initialize all tables.
"""
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker


# DB PATH
BASE_DIR=Path(__file__).resolve().parent.parent
DATABASE_DIR = BASE_DIR/'database'
DATABASE_DIR.mkdir(exist_ok=True)
DATABASE_URL = f"sqlite:///{DATABASE_DIR / 'chat.db'}"


# Enginee

engine = create_engine(DATABASE_URL,echo=False)

#Session Factory
SessionLocal = sessionmaker(bind=engine,autoflush=False,autocommit=False,expire_on_commit=False)

#base model
class BaseModel(DeclarativeBase):
    """Base class for all ORM models."""
    pass

#DB session

def get_session()->Session:
    return SessionLocal()

#table

def init_db():
    BaseModel.metadata.create_all(bind=engine)

