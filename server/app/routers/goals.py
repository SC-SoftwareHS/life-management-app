"""Goals endpoints"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlmodel import Session, select
from typing import List, Optional
from datetime import datetime

from ..db import get_session
from ..schemas import GoalCreate, GoalUpdate, GoalResponse
from ..models import Goal, User, LifeArea, GoalAreaLink, GoalTimeframe, GoalStatus
from ..auth import get_current_user

router = APIRouter()


@router.post("/", response_model=GoalResponse, status_code=status.HTTP_201_CREATED)
def create_goal(
    goal_data: GoalCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    Create a new goal.

    - **name**: Goal name/description
    - **timeframe**: short, medium, or long
    - **target_date**: Optional target completion date
    - **progress_percentage**: Current progress (0-100)
    - **status**: active, completed, abandoned
    - **area_ids**: List of life area IDs (1-8)
    """
    # Validate area IDs exist
    for area_id in goal_data.area_ids:
        area = session.get(LifeArea, area_id)
        if not area:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Life area with id {area_id} not found"
            )

    # Create goal
    goal = Goal(
        user_id=current_user.id,
        name=goal_data.name,
        timeframe=goal_data.timeframe,
        target_date=goal_data.target_date,
        progress_percentage=goal_data.progress_percentage,
        status=goal_data.status
    )
    session.add(goal)
    session.commit()
    session.refresh(goal)

    # Link to areas
    for area_id in goal_data.area_ids:
        link = GoalAreaLink(goal_id=goal.id, area_id=area_id)
        session.add(link)
    session.commit()

    # Reload with relationships
    session.refresh(goal)
    return goal


@router.get("/", response_model=List[GoalResponse])
def list_goals(
    area_id: Optional[int] = Query(None, description="Filter by life area ID"),
    timeframe: Optional[GoalTimeframe] = Query(None, description="Filter by timeframe"),
    status: Optional[GoalStatus] = Query(None, description="Filter by status"),
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    List all goals for the current user.

    Optional filters:
    - **area_id**: Filter by life area (1-8)
    - **timeframe**: Filter by short, medium, or long
    - **status**: Filter by active, completed, or abandoned
    """
    # Build query
    statement = select(Goal).where(Goal.user_id == current_user.id)

    if timeframe:
        statement = statement.where(Goal.timeframe == timeframe)
    if status:
        statement = statement.where(Goal.status == status)

    goals = session.exec(statement).all()

    # Filter by area if requested
    if area_id is not None:
        filtered_goals = []
        for goal in goals:
            area_ids = [area.id for area in goal.areas]
            if area_id in area_ids:
                filtered_goals.append(goal)
        goals = filtered_goals

    return goals


@router.get("/{goal_id}", response_model=GoalResponse)
def get_goal(
    goal_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    Get a specific goal by ID.
    """
    goal = session.get(Goal, goal_id)
    if not goal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Goal not found"
        )

    if goal.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this goal"
        )

    return goal


@router.put("/{goal_id}", response_model=GoalResponse)
def update_goal(
    goal_id: int,
    goal_data: GoalUpdate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    Update an existing goal.

    All fields are optional. Only provided fields will be updated.
    """
    goal = session.get(Goal, goal_id)
    if not goal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Goal not found"
        )

    if goal.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this goal"
        )

    # Update fields
    update_data = goal_data.model_dump(exclude_unset=True)

    # Handle area_ids separately
    area_ids = update_data.pop("area_ids", None)

    for key, value in update_data.items():
        setattr(goal, key, value)

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
        statement = select(GoalAreaLink).where(GoalAreaLink.goal_id == goal_id)
        existing_links = session.exec(statement).all()
        for link in existing_links:
            session.delete(link)

        # Create new links
        for area_id in area_ids:
            link = GoalAreaLink(goal_id=goal_id, area_id=area_id)
            session.add(link)

    goal.updated_at = datetime.utcnow()
    session.add(goal)
    session.commit()
    session.refresh(goal)

    return goal


@router.delete("/{goal_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_goal(
    goal_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    Delete a goal.
    """
    goal = session.get(Goal, goal_id)
    if not goal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Goal not found"
        )

    if goal.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this goal"
        )

    session.delete(goal)
    session.commit()

    return None
