"""Tasks endpoints"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlmodel import Session, select
from typing import List, Optional
from datetime import datetime

from ..db import get_session
from ..schemas import TaskCreate, TaskUpdate, TaskResponse
from ..models import Task, User, LifeArea, TaskStatus
from ..auth import get_current_user

router = APIRouter()


@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(
    task_data: TaskCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    Create a new task.

    - **description**: Task description
    - **area_id**: Life area ID (1-8)
    - **status**: todo, doing, or done (defaults to todo)
    - **due_date**: Optional due date
    - **priority**: Optional priority level (1-5, 1=highest)
    """
    # Validate area ID exists
    area = session.get(LifeArea, task_data.area_id)
    if not area:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Life area with id {task_data.area_id} not found"
        )

    # Create task
    task = Task(
        user_id=current_user.id,
        area_id=task_data.area_id,
        description=task_data.description,
        status=task_data.status or TaskStatus.TODO,
        due_date=task_data.due_date,
        priority=task_data.priority
    )
    session.add(task)
    session.commit()
    session.refresh(task)

    return task


@router.get("/", response_model=List[TaskResponse])
def list_tasks(
    area_id: Optional[int] = Query(None, description="Filter by life area ID"),
    status: Optional[TaskStatus] = Query(None, description="Filter by status"),
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    List all tasks for the current user.

    Optional filters:
    - **area_id**: Filter by life area (1-8)
    - **status**: Filter by todo, doing, or done
    """
    # Build query
    statement = select(Task).where(Task.user_id == current_user.id)

    if area_id is not None:
        statement = statement.where(Task.area_id == area_id)
    if status:
        statement = statement.where(Task.status == status)

    # Order by priority (nulls last), then by created_at
    statement = statement.order_by(Task.priority.asc(), Task.created_at.desc())

    tasks = session.exec(statement).all()
    return tasks


@router.get("/{task_id}", response_model=TaskResponse)
def get_task(
    task_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    Get a specific task by ID.
    """
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    if task.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this task"
        )

    return task


@router.put("/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: int,
    task_data: TaskUpdate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    Update an existing task.

    All fields are optional. Only provided fields will be updated.

    Status transitions:
    - todo -> doing -> done (typical workflow)
    - Can transition directly from todo -> done
    - Can move back from done -> doing or doing -> todo
    """
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    if task.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this task"
        )

    # Update fields
    update_data = task_data.model_dump(exclude_unset=True)

    # Validate area_id if provided
    if "area_id" in update_data:
        area = session.get(LifeArea, update_data["area_id"])
        if not area:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Life area with id {update_data['area_id']} not found"
            )

    for key, value in update_data.items():
        setattr(task, key, value)

    task.updated_at = datetime.utcnow()
    session.add(task)
    session.commit()
    session.refresh(task)

    return task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    Delete a task.
    """
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    if task.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this task"
        )

    session.delete(task)
    session.commit()

    return None
