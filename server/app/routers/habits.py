"""Habits endpoints"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlmodel import Session, select
from typing import List, Optional
from datetime import datetime, date

from ..db import get_session
from ..schemas import HabitCreate, HabitUpdate, HabitResponse, HabitCheckinRequest, HabitCheckInResponse
from ..models import Habit, User, LifeArea, HabitAreaLink, HabitType
from ..auth import get_current_user

router = APIRouter()


@router.post("/", response_model=HabitResponse, status_code=status.HTTP_201_CREATED)
def create_habit(
    habit_data: HabitCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    Create a new habit.

    - **name**: Habit name/description
    - **habit_type**: positive (build) or negative (break)
    - **frequency_description**: e.g., "daily", "3x per week"
    - **area_ids**: List of life area IDs (1-8)
    """
    # Validate area IDs exist
    for area_id in habit_data.area_ids:
        area = session.get(LifeArea, area_id)
        if not area:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Life area with id {area_id} not found"
            )

    # Create habit
    habit = Habit(
        user_id=current_user.id,
        name=habit_data.name,
        habit_type=habit_data.habit_type,
        frequency_description=habit_data.frequency_description,
        current_streak=0,
        longest_streak=0
    )
    session.add(habit)
    session.commit()
    session.refresh(habit)

    # Link to areas
    for area_id in habit_data.area_ids:
        link = HabitAreaLink(habit_id=habit.id, area_id=area_id)
        session.add(link)
    session.commit()

    # Reload with relationships
    session.refresh(habit)
    return habit


@router.get("/", response_model=List[HabitResponse])
def list_habits(
    area_id: Optional[int] = Query(None, description="Filter by life area ID"),
    habit_type: Optional[HabitType] = Query(None, description="Filter by habit type"),
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    List all habits for the current user.

    Optional filters:
    - **area_id**: Filter by life area (1-8)
    - **habit_type**: Filter by positive or negative
    """
    # Build query
    statement = select(Habit).where(Habit.user_id == current_user.id)

    if habit_type:
        statement = statement.where(Habit.habit_type == habit_type)

    habits = session.exec(statement).all()

    # Filter by area if requested
    if area_id is not None:
        filtered_habits = []
        for habit in habits:
            area_ids = [area.id for area in habit.areas]
            if area_id in area_ids:
                filtered_habits.append(habit)
        habits = filtered_habits

    return habits


@router.get("/{habit_id}", response_model=HabitResponse)
def get_habit(
    habit_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    Get a specific habit by ID.
    """
    habit = session.get(Habit, habit_id)
    if not habit:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Habit not found"
        )

    if habit.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this habit"
        )

    return habit


@router.put("/{habit_id}", response_model=HabitResponse)
def update_habit(
    habit_id: int,
    habit_data: HabitUpdate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    Update an existing habit.

    All fields are optional. Only provided fields will be updated.
    """
    habit = session.get(Habit, habit_id)
    if not habit:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Habit not found"
        )

    if habit.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this habit"
        )

    # Update fields
    update_data = habit_data.model_dump(exclude_unset=True)

    # Handle area_ids separately
    area_ids = update_data.pop("area_ids", None)

    for key, value in update_data.items():
        setattr(habit, key, value)

    # Update area links if provided
    if area_ids is not None:
        # Validate area IDs
        for area_id in area_ids:
            area = session.get(LifeArea, area_id)
            if not area:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Life area with id {area_id} not found"
                )

        # Delete existing links
        statement = select(HabitAreaLink).where(HabitAreaLink.habit_id == habit_id)
        existing_links = session.exec(statement).all()
        for link in existing_links:
            session.delete(link)

        # Create new links
        for area_id in area_ids:
            link = HabitAreaLink(habit_id=habit_id, area_id=area_id)
            session.add(link)

    habit.updated_at = datetime.utcnow()
    session.add(habit)
    session.commit()
    session.refresh(habit)

    return habit


@router.delete("/{habit_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_habit(
    habit_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    Delete a habit.
    """
    habit = session.get(Habit, habit_id)
    if not habit:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Habit not found"
        )

    if habit.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this habit"
        )

    session.delete(habit)
    session.commit()

    return None


@router.post("/{habit_id}/checkin", response_model=HabitCheckInResponse)
def checkin_habit(
    habit_id: int,
    checkin_data: HabitCheckinRequest,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    Check in to a habit and update streak.

    For positive habits: checking in extends the streak
    For negative habits: checking in breaks the streak (reset to 0)

    Streak logic:
    - If checking in on consecutive days, increment current_streak
    - If there's a gap, reset current_streak to 1
    - Update longest_streak if current_streak exceeds it
    """
    habit = session.get(Habit, habit_id)
    if not habit:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Habit not found"
        )

    if habit.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to check in to this habit"
        )

    today = date.today()
    checkin_date = checkin_data.checkin_date or today

    # Don't allow future check-ins
    if checkin_date > today:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot check in to a future date"
        )

    # Calculate streak
    if habit.habit_type == HabitType.POSITIVE:
        # Positive habit: checking in is good
        if habit.last_checkin_date is None:
            # First check-in
            habit.current_streak = 1
        elif checkin_date == habit.last_checkin_date:
            # Already checked in today
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Already checked in for this date"
            )
        elif (checkin_date - habit.last_checkin_date).days == 1:
            # Consecutive day
            habit.current_streak += 1
        else:
            # Gap in streak
            habit.current_streak = 1
    else:
        # Negative habit: checking in means you did the bad habit (breaks streak)
        habit.current_streak = 0

    # Update longest streak
    if habit.current_streak > habit.longest_streak:
        habit.longest_streak = habit.current_streak

    habit.last_checkin_date = checkin_date
    habit.updated_at = datetime.utcnow()

    session.add(habit)
    session.commit()
    session.refresh(habit)

    return HabitCheckInResponse(
        habit_id=habit.id,
        checkin_date=checkin_date,
        current_streak=habit.current_streak,
        longest_streak=habit.longest_streak,
        message=f"Checked in! Current streak: {habit.current_streak} days"
    )
