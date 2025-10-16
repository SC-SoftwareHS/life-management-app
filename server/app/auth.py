"""Authentication and authorization"""
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status, Request
from sqlmodel import Session, select
from typing import Optional
from .models import User
from .db import get_session

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Hash a password using bcrypt"""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash"""
    return pwd_context.verify(plain_password, hashed_password)


def create_user(session: Session, username: str, password: str, email: Optional[str] = None, full_name: Optional[str] = None) -> User:
    """
    Create a new user with hashed password.

    Args:
        session: Database session
        username: Unique username
        password: Plain text password (will be hashed)
        email: Optional email
        full_name: Optional full name

    Returns:
        Created User object

    Raises:
        ValueError: If username already exists
    """
    # Check if username exists
    existing = session.exec(select(User).where(User.username == username)).first()
    if existing:
        raise ValueError(f"Username '{username}' already exists")

    # Create user with hashed password
    user = User(
        username=username,
        hashed_password=hash_password(password),
        email=email,
        full_name=full_name
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


def authenticate_user(session: Session, username: str, password: str) -> Optional[User]:
    """
    Authenticate a user by username and password.

    Args:
        session: Database session
        username: Username
        password: Plain text password

    Returns:
        User object if authentication successful, None otherwise
    """
    user = session.exec(select(User).where(User.username == username)).first()
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    if not user.is_active:
        return None
    return user


def get_current_user(request: Request, session: Session = Depends(get_session)) -> User:
    """
    Dependency to get the current authenticated user from session.

    Args:
        request: FastAPI request object (contains session)
        session: Database session

    Returns:
        Current User object

    Raises:
        HTTPException: 401 if not authenticated or user not found
    """
    # Get user_id from session
    user_id = request.session.get("user_id")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required"
        )

    # Load user from database
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User account is inactive"
        )

    return user


def create_session(request: Request, user: User):
    """
    Create a session for the user.

    Args:
        request: FastAPI request object
        user: User object to create session for
    """
    request.session["user_id"] = user.id
    request.session["username"] = user.username


def destroy_session(request: Request):
    """
    Destroy the current session (logout).

    Args:
        request: FastAPI request object
    """
    request.session.clear()
