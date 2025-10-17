"""Contacts endpoints"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlmodel import Session, select
from typing import List, Optional
from datetime import datetime, date

from ..db import get_session
from ..schemas import ContactCreate, ContactUpdate, ContactResponse, ContactBirthdayResponse
from ..models import Contact, User, LifeArea, ContactAreaLink
from ..auth import get_current_user

router = APIRouter()


def calculate_age(birth_date: date, reference_date: date = None) -> int:
    """Calculate age based on birth date"""
    if reference_date is None:
        reference_date = date.today()

    age = reference_date.year - birth_date.year
    # Adjust if birthday hasn't occurred yet this year
    if (reference_date.month, reference_date.day) < (birth_date.month, birth_date.day):
        age -= 1
    return age


@router.post("/", response_model=ContactResponse, status_code=status.HTTP_201_CREATED)
def create_contact(
    contact_data: ContactCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    Create a new contact.

    - **name**: Contact's full name
    - **birthday**: Date of birth (YYYY-MM-DD)
    - **relationship**: e.g., "friend", "family", "colleague"
    - **phone**: Optional phone number
    - **email**: Optional email
    - **notes**: Optional notes
    - **area_ids**: List of life area IDs (1-8)
    """
    # Validate area IDs exist
    for area_id in contact_data.area_ids:
        area = session.get(LifeArea, area_id)
        if not area:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Life area with id {area_id} not found"
            )

    # Create contact
    contact = Contact(
        user_id=current_user.id,
        name=contact_data.name,
        birthday=contact_data.birthday,
        relationship=contact_data.relationship,
        phone=contact_data.phone,
        email=contact_data.email,
        notes=contact_data.notes
    )
    session.add(contact)
    session.commit()
    session.refresh(contact)

    # Link to areas
    for area_id in contact_data.area_ids:
        link = ContactAreaLink(contact_id=contact.id, area_id=area_id)
        session.add(link)
    session.commit()

    # Reload with relationships
    session.refresh(contact)
    return contact


@router.get("/", response_model=List[ContactResponse])
def list_contacts(
    area_id: Optional[int] = Query(None, description="Filter by life area ID"),
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    List all contacts for the current user.

    Optional filters:
    - **area_id**: Filter by life area (1-8)
    """
    # Build query
    statement = select(Contact).where(Contact.user_id == current_user.id)
    contacts = session.exec(statement).all()

    # Filter by area if requested
    if area_id is not None:
        filtered_contacts = []
        for contact in contacts:
            area_ids = [area.id for area in contact.areas]
            if area_id in area_ids:
                filtered_contacts.append(contact)
        contacts = filtered_contacts

    return contacts


@router.get("/{contact_id}", response_model=ContactResponse)
def get_contact(
    contact_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    Get a specific contact by ID.
    """
    contact = session.get(Contact, contact_id)
    if not contact:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contact not found"
        )

    if contact.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this contact"
        )

    return contact


@router.get("/{contact_id}/birthday", response_model=ContactBirthdayResponse)
def get_contact_birthday_info(
    contact_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    Get birthday information for a contact, including calculated age.

    Returns:
    - Current age
    - Days until next birthday
    - Next birthday date
    """
    contact = session.get(Contact, contact_id)
    if not contact:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contact not found"
        )

    if contact.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this contact"
        )

    today = date.today()
    current_age = calculate_age(contact.birthday, today)

    # Calculate next birthday
    next_birthday = date(today.year, contact.birthday.month, contact.birthday.day)
    if next_birthday < today:
        next_birthday = date(today.year + 1, contact.birthday.month, contact.birthday.day)

    days_until_birthday = (next_birthday - today).days

    return ContactBirthdayResponse(
        contact_id=contact.id,
        name=contact.name,
        birthday=contact.birthday,
        current_age=current_age,
        next_birthday=next_birthday,
        days_until_birthday=days_until_birthday
    )


@router.put("/{contact_id}", response_model=ContactResponse)
def update_contact(
    contact_id: int,
    contact_data: ContactUpdate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    Update an existing contact.

    All fields are optional. Only provided fields will be updated.
    """
    contact = session.get(Contact, contact_id)
    if not contact:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contact not found"
        )

    if contact.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this contact"
        )

    # Update fields
    update_data = contact_data.model_dump(exclude_unset=True)

    # Handle area_ids separately
    area_ids = update_data.pop("area_ids", None)

    for key, value in update_data.items():
        setattr(contact, key, value)

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
        statement = select(ContactAreaLink).where(ContactAreaLink.contact_id == contact_id)
        existing_links = session.exec(statement).all()
        for link in existing_links:
            session.delete(link)

        # Create new links
        for area_id in area_ids:
            link = ContactAreaLink(contact_id=contact_id, area_id=area_id)
            session.add(link)

    contact.updated_at = datetime.utcnow()
    session.add(contact)
    session.commit()
    session.refresh(contact)

    return contact


@router.delete("/{contact_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_contact(
    contact_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    Delete a contact.
    """
    contact = session.get(Contact, contact_id)
    if not contact:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contact not found"
        )

    if contact.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this contact"
        )

    session.delete(contact)
    session.commit()

    return None
