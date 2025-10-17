"""Database connection and session management"""
from sqlmodel import create_engine, Session, SQLModel
from typing import Generator
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Ensure data directory exists
data_dir = Path(__file__).parent.parent / "data"
data_dir.mkdir(exist_ok=True)

# Get database URL from environment (use absolute path for SQLite)
db_path = (data_dir / "app.sqlite3").absolute()
DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{db_path}")

# Create engine
# Set check_same_thread=False for SQLite to work with FastAPI
engine = create_engine(
    DATABASE_URL,
    echo=False,  # Set to True for SQL query debugging
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)


def create_db_and_tables():
    """Create all database tables"""
    # Import all models to register them with SQLModel.metadata
    from . import models  # noqa: F401
    SQLModel.metadata.create_all(engine)


def get_session() -> Generator[Session, None, None]:
    """
    Dependency for getting database sessions.
    Use this with FastAPI's Depends().
    """
    with Session(engine) as session:
        yield session
