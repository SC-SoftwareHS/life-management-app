"""Main FastAPI application entry point"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from contextlib import asynccontextmanager
import os
import secrets
from pathlib import Path
from dotenv import load_dotenv

from .db import create_db_and_tables

# Load environment variables
load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan events - runs on startup and shutdown"""
    # Startup
    print("Creating database tables...")
    create_db_and_tables()
    print("Database ready!")
    yield
    # Shutdown
    print("Shutting down...")


# Create FastAPI app
app = FastAPI(
    title="Life Management API",
    description="AI-assisted life management application covering 8 life areas",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware (for future frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],  # Frontend dev servers
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def _get_app_secret() -> str:
    """Return configured APP_SECRET or generate a temporary one."""
    configured = os.getenv("APP_SECRET")
    if configured:
        return configured

    generated = secrets.token_urlsafe(32)
    print(
        "[SECURITY] APP_SECRET not provided. Generated a temporary secret for this runtime. "
        "Sessions will reset on restart."
    )
    return generated


# Add session middleware for authentication
APP_SECRET = _get_app_secret()

app.add_middleware(
    SessionMiddleware,
    secret_key=APP_SECRET,
    session_cookie="session_id",
    max_age=86400,  # 24 hours
    same_site="lax",
    https_only=False,  # Set to True in production with HTTPS
    # httponly is set by default in SessionMiddleware
)


# Root endpoint
@app.get("/")
def read_root():
    """Root endpoint - API info"""
    return {
        "name": "Life Management API",
        "version": "1.0.0",
        "description": "AI-assisted life management application",
        "docs": "/docs",
        "redoc": "/redoc",
        "features": {
            "life_areas": 8,
            "goals": "short/medium/long term with progress tracking",
            "habits": "with streak counters",
            "tasks": "todo/doing/done workflow",
            "contacts": "with birthday age calculation",
            "references": "websites, scriptures, laws",
            "health_catalog": "doctors, foods, supplements, medications, motion",
            "financial": "banking, assets, liabilities",
            "conflict_resolution": "3 main topics for relationships",
            "journal": "entries per life area",
            "ai_content": "Bible verses and insights (stubbed in MVP)"
        }
    }


# Health check
@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


# Include routers
from .routers import auth, areas, ai, goals, habits, tasks, contacts, references, health, finance, entries, one_on_one

app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(areas.router, prefix="/api/areas", tags=["Life Areas"])
app.include_router(ai.router, prefix="/api/ai", tags=["AI Content"])
app.include_router(goals.router, prefix="/api/goals", tags=["Goals"])
app.include_router(habits.router, prefix="/api/habits", tags=["Habits"])
app.include_router(tasks.router, prefix="/api/tasks", tags=["Tasks"])
app.include_router(contacts.router, prefix="/api/contacts", tags=["Contacts"])
app.include_router(references.router, prefix="/api/references", tags=["References"])
app.include_router(health.router, prefix="/api/health", tags=["Health Catalog"])
app.include_router(finance.router, prefix="/api/finance", tags=["Finance"])
app.include_router(entries.router, prefix="/api/entries", tags=["Entries"])
app.include_router(one_on_one.router, prefix="/api/one-on-one", tags=["One-on-One"])

# Serve frontend static files
# Find the frontend directory (it's next to server/)
server_dir = Path(__file__).resolve().parent.parent
frontend_dir = server_dir.parent / "frontend"

if frontend_dir.exists():
    # Mount static files for CSS and JS
    app.mount("/static", StaticFiles(directory=str(frontend_dir)), name="static")
    print(f"[FRONTEND] Serving frontend from: {frontend_dir}")
else:
    print(f"[FRONTEND] Frontend directory not found at: {frontend_dir}")
