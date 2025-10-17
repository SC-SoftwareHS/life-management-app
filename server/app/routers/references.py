"""References endpoints"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlmodel import Session, select
from typing import List, Optional
from datetime import datetime

from ..db import get_session
from ..schemas import ReferenceCreate, ReferenceUpdate, ReferenceResponse
from ..models import Reference, User, LifeArea, ReferenceAreaLink, ReferenceType
from ..auth import get_current_user

router = APIRouter()


@router.post("/", response_model=ReferenceResponse, status_code=status.HTTP_201_CREATED)
def create_reference(
    reference_data: ReferenceCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    Create a new reference.

    - **title**: Reference title/name
    - **reference_type**: website, scripture, or law
    - **url**: URL for websites
    - **book_chapter_verse**: For scriptures (e.g., "John 3:16")
    - **law_citation**: For laws (e.g., "USC Title 42")
    - **notes**: Optional notes
    - **area_ids**: List of life area IDs (1-8)
    """
    # Validate area IDs exist
    for area_id in reference_data.area_ids:
        area = session.get(LifeArea, area_id)
        if not area:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Life area with id {area_id} not found"
            )

    # Validate reference type-specific fields
    if reference_data.reference_type == ReferenceType.WEBSITE and not reference_data.url:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="URL is required for website references"
        )
    if reference_data.reference_type == ReferenceType.SCRIPTURE and not reference_data.book_chapter_verse:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Book/chapter/verse is required for scripture references"
        )
    if reference_data.reference_type == ReferenceType.LAW and not reference_data.law_citation:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Law citation is required for law references"
        )

    # Create reference
    reference = Reference(
        user_id=current_user.id,
        title=reference_data.title,
        reference_type=reference_data.reference_type,
        url=reference_data.url,
        book_chapter_verse=reference_data.book_chapter_verse,
        law_citation=reference_data.law_citation,
        notes=reference_data.notes
    )
    session.add(reference)
    session.commit()
    session.refresh(reference)

    # Link to areas
    for area_id in reference_data.area_ids:
        link = ReferenceAreaLink(reference_id=reference.id, area_id=area_id)
        session.add(link)
    session.commit()

    # Reload with relationships
    session.refresh(reference)
    return reference


@router.get("/", response_model=List[ReferenceResponse])
def list_references(
    area_id: Optional[int] = Query(None, description="Filter by life area ID"),
    reference_type: Optional[ReferenceType] = Query(None, description="Filter by reference type"),
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    List all references for the current user.

    Optional filters:
    - **area_id**: Filter by life area (1-8)
    - **reference_type**: Filter by website, scripture, or law
    """
    # Build query
    statement = select(Reference).where(Reference.user_id == current_user.id)

    if reference_type:
        statement = statement.where(Reference.reference_type == reference_type)

    references = session.exec(statement).all()

    # Filter by area if requested
    if area_id is not None:
        filtered_references = []
        for reference in references:
            area_ids = [area.id for area in reference.areas]
            if area_id in area_ids:
                filtered_references.append(reference)
        references = filtered_references

    return references


@router.get("/{reference_id}", response_model=ReferenceResponse)
def get_reference(
    reference_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    Get a specific reference by ID.
    """
    reference = session.get(Reference, reference_id)
    if not reference:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reference not found"
        )

    if reference.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this reference"
        )

    return reference


@router.put("/{reference_id}", response_model=ReferenceResponse)
def update_reference(
    reference_id: int,
    reference_data: ReferenceUpdate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    Update an existing reference.

    All fields are optional. Only provided fields will be updated.
    """
    reference = session.get(Reference, reference_id)
    if not reference:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reference not found"
        )

    if reference.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this reference"
        )

    # Update fields
    update_data = reference_data.model_dump(exclude_unset=True)

    # Handle area_ids separately
    area_ids = update_data.pop("area_ids", None)

    for key, value in update_data.items():
        setattr(reference, key, value)

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
        statement = select(ReferenceAreaLink).where(ReferenceAreaLink.reference_id == reference_id)
        existing_links = session.exec(statement).all()
        for link in existing_links:
            session.delete(link)

        # Create new links
        for area_id in area_ids:
            link = ReferenceAreaLink(reference_id=reference_id, area_id=area_id)
            session.add(link)

    reference.updated_at = datetime.utcnow()
    session.add(reference)
    session.commit()
    session.refresh(reference)

    return reference


@router.delete("/{reference_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_reference(
    reference_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    Delete a reference.
    """
    reference = session.get(Reference, reference_id)
    if not reference:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reference not found"
        )

    if reference.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this reference"
        )

    session.delete(reference)
    session.commit()

    return None
