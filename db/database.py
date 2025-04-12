from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# Read DB config from environment or fallback
DB_URL = os.getenv("DATABASE_URL", "postgresql://gmailuser:gmailpass@localhost:5432/gmail_db")

# SQLAlchemy Engine and Session
engine = create_engine(DB_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base for all models
Base = declarative_base()


def init_db():
    """Create tables and initialize the database."""
    from .models import Email  # Avoid circular import
    Base.metadata.create_all(bind=engine)