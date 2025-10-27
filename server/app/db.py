"""Database connection and session management"""
from sqlmodel import create_engine, Session, SQLModel
from typing import Generator
import os
from pathlib import Path
from urllib.parse import urlparse
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

SERVER_DIR = Path(__file__).resolve().parent.parent


def _normalize_sqlite_url(url: str) -> str:
    """Ensure sqlite URLs use absolute paths with exactly three leading slashes."""
    parsed = urlparse(url)
    if parsed.scheme != "sqlite":
        return url

    path_with_netloc = f"/{parsed.netloc}{parsed.path}" if parsed.netloc else parsed.path

    if path_with_netloc.startswith("//"):
        # Handle sqlite:////absolute/path by collapsing the duplicate slash
        normalized_path = "/" + path_with_netloc.lstrip("/")
    elif path_with_netloc.startswith("/../") or path_with_netloc.startswith("/./"):
        # Treat ../ or ./ prefixes as relative to the server directory
        relative_target = Path(path_with_netloc[1:])
        normalized_path = (SERVER_DIR / relative_target).resolve().as_posix()
    else:
        candidate_path = Path(path_with_netloc)
        if candidate_path.is_absolute():
            normalized_path = candidate_path.resolve().as_posix()
        else:
            normalized_path = (SERVER_DIR / candidate_path).resolve().as_posix()

    if not normalized_path.startswith("/"):
        normalized_path = f"/{normalized_path}"

    # SQLAlchemy needs sqlite:/// + /absolute/path (4 slashes total)
    normalized_url = f"sqlite:///{normalized_path}"
    if parsed.query:
        normalized_url += f"?{parsed.query}"
    if parsed.fragment:
        normalized_url += f"#{parsed.fragment}"
    return normalized_url


def _get_database_url() -> str:
    """Return the DATABASE_URL from env or compute the default sqlite path."""
    env_url = os.getenv("DATABASE_URL")
    if env_url:
        return _normalize_sqlite_url(env_url)

    # For Railway/production, use /tmp for ephemeral storage
    # For local dev, use server/data
    railway_detected = any(
        os.getenv(var_name)
        for var_name in (
            "RAILWAY_ENVIRONMENT",
            "RAILWAY_ENVIRONMENT_ID",
            "RAILWAY_PROJECT_ID",
            "RAILWAY_SERVICE_ID",
        )
    )
    if railway_detected:
        data_dir = Path("/tmp/data")
    else:
        data_dir = SERVER_DIR / "data"

    data_dir.mkdir(parents=True, exist_ok=True)
    db_file = data_dir / "app.sqlite3"
    # SQLAlchemy needs 4 slashes total: sqlite:/// + /absolute/path
    return f"sqlite:///{str(db_file.resolve())}"


# Get DATABASE_URL from environment, with sensible default
# Default: SQLite database in server/data/app.sqlite3 (using absolute path)
DATABASE_URL = _get_database_url()

print(f"[DB] Database URL: {DATABASE_URL}")

# Create engine
# Set check_same_thread=False for SQLite to work with FastAPI async
engine = create_engine(
    DATABASE_URL,
    echo=False,  # Set to True for SQL query debugging
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)


def create_db_and_tables():
    """Create all database tables"""
    print("[DB] Creating database tables...")
    # Import all models to register them with SQLModel.metadata
    from . import models  # noqa: F401
    SQLModel.metadata.create_all(engine)
    print("[DB] Database tables created successfully!")


def get_session() -> Generator[Session, None, None]:
    """
    Dependency for getting database sessions.
    Use this with FastAPI's Depends().
    """
    with Session(engine) as session:
        yield session
