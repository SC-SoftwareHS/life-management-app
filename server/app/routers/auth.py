"""Authentication endpoints"""
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlmodel import Session
from datetime import datetime

from ..db import get_session
from ..schemas import UserCreate, LoginRequest, UserResponse
from ..auth import create_user, authenticate_user, get_current_user, create_session, destroy_session
from ..models import User

router = APIRouter()


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(
    user_data: UserCreate,
    session: Session = Depends(get_session)
):
    """
    Register a new user account.

    - **username**: Unique username (3-50 chars)
    - **password**: Password (min 8 chars)
    - **email**: Optional email
    - **full_name**: Optional full name
    """
    try:
        user = create_user(
            session=session,
            username=user_data.username,
            password=user_data.password,
            email=user_data.email,
            full_name=user_data.full_name
        )
        return user
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/login")
def login(
    login_data: LoginRequest,
    request: Request,
    session: Session = Depends(get_session)
):
    """
    Login with username and password.

    Creates a session cookie that will be used for authentication.
    """
    user = authenticate_user(
        session=session,
        username=login_data.username,
        password=login_data.password
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    # Create session
    create_session(request, user)

    return {
        "message": "Login successful",
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "full_name": user.full_name
        }
    }


@router.post("/logout")
def logout(request: Request):
    """
    Logout and destroy session.
    """
    destroy_session(request)
    return {"message": "Logged out successfully"}


@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    """
    Get current authenticated user information.

    Requires authentication.
    """
    return current_user
