"""Journal Entries endpoints"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlmodel import Session, select
from typing import List, Optional
from datetime import datetime, date

from ..db import get_session
from ..schemas import EntryCreate, EntryUpdate, EntryResponse
from ..models import Entry, User, LifeArea
from ..auth import get_current_user

router = APIRouter()


@router.post("/", response_model=EntryResponse, status_code=status.HTTP_201_CREATED)
def create_entry(
    entry_data: EntryCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    Create a new journal entry.

    - **area_id**: Life area ID (1-8)
    - **entry_date**: Date of the entry (defaults to today)
    - **content**: Journal entry content
    - **title**: Optional title for the entry
    """
    # Validate area ID exists
    area = session.get(LifeArea, entry_data.area_id)
    if not area:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Life area with id {entry_data.area_id} not found"
        )

    # Create entry
    entry = Entry(
        user_id=current_user.id,
        area_id=entry_data.area_id,
        entry_date=entry_data.entry_date or date.today(),
        content=entry_data.content,
        title=entry_data.title
    )
    session.add(entry)
    session.commit()
    session.refresh(entry)

    return entry


@router.get("/", response_model=List[EntryResponse])
def list_entries(
    area_id: Optional[int] = Query(None, description="Filter by life area ID"),
    start_date: Optional[date] = Query(None, description="Filter entries from this date (YYYY-MM-DD)"),
    end_date: Optional[date] = Query(None, description="Filter entries until this date (YYYY-MM-DD)"),
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    List all journal entries for the current user.

    Optional filters:
    - **area_id**: Filter by life area (1-8)
    - **start_date**: Get entries from this date onwards
    - **end_date**: Get entries up to this date
    """
    # Build query
    statement = select(Entry).where(Entry.user_id == current_user.id)

    if area_id is not None:
        statement = statement.where(Entry.area_id == area_id)
    if start_date:
        statement = statement.where(Entry.entry_date >= start_date)
    if end_date:
        statement = statement.where(Entry.entry_date <= end_date)

    # Order by date descending (most recent first)
    statement = statement.order_by(Entry.entry_date.desc())

    entries = session.exec(statement).all()
    return entries


@router.get("/{entry_id}", response_model=EntryResponse)
def get_entry(
    entry_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    Get a specific journal entry by ID.
    """
    entry = session.get(Entry, entry_id)
    if not entry:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Entry not found"
        )

    if entry.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this entry"
        )

    return entry


@router.put("/{entry_id}", response_model=EntryResponse)
def update_entry(
    entry_id: int,
    entry_data: EntryUpdate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    Update an existing journal entry.

    All fields are optional. Only provided fields will be updated.
    """
    entry = session.get(Entry, entry_id)
    if not entry:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Entry not found"
        )

    if entry.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this entry"
        )

    # Update fields
    update_data = entry_data.model_dump(exclude_unset=True)

    # Validate area_id if provided
    if "area_id" in update_data:
        area = session.get(LifeArea, update_data["area_id"])
        if not area:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Life area with id {update_data['area_id']} not found"
            )

    for key, value in update_data.items():
        setattr(entry, key, value)

    entry.updated_at = datetime.utcnow()
    session.add(entry)
    session.commit()
    session.refresh(entry)

    return entry


@router.delete("/{entry_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_entry(
    entry_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    Delete a journal entry.
    """
    entry = session.get(Entry, entry_id)
    if not entry:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Entry not found"
        )

    if entry.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this entry"
        )

    session.delete(entry)
    session.commit()

    return None
