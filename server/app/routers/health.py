"""Health Catalog endpoints"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlmodel import Session, select
from typing import List, Optional
from datetime import datetime

from ..db import get_session
from ..schemas import HealthCatalogItemCreate, HealthCatalogItemUpdate, HealthCatalogItemResponse
from ..models import HealthCatalogItem, User, HealthCatalogType
from ..auth import get_current_user

router = APIRouter()


@router.post("/", response_model=HealthCatalogItemResponse, status_code=status.HTTP_201_CREATED)
def create_health_item(
    item_data: HealthCatalogItemCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    Create a new health catalog item.

    - **name**: Item name
    - **catalog_type**: doctor, food, supplement, medication, or motion
    - **notes**: Optional notes/details
    - **frequency**: For supplements/medications (e.g., "daily", "as needed")
    - **dosage**: For supplements/medications (e.g., "500mg", "1 tablet")
    """
    # Create health item
    item = HealthCatalogItem(
        user_id=current_user.id,
        name=item_data.name,
        catalog_type=item_data.catalog_type,
        notes=item_data.notes,
        frequency=item_data.frequency,
        dosage=item_data.dosage
    )
    session.add(item)
    session.commit()
    session.refresh(item)

    return item


@router.get("/", response_model=List[HealthCatalogItemResponse])
def list_health_items(
    catalog_type: Optional[HealthCatalogType] = Query(None, description="Filter by catalog type"),
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    List all health catalog items for the current user.

    Optional filters:
    - **catalog_type**: Filter by doctor, food, supplement, medication, or motion
    """
    # Build query
    statement = select(HealthCatalogItem).where(HealthCatalogItem.user_id == current_user.id)

    if catalog_type:
        statement = statement.where(HealthCatalogItem.catalog_type == catalog_type)

    items = session.exec(statement).all()
    return items


@router.get("/{item_id}", response_model=HealthCatalogItemResponse)
def get_health_item(
    item_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    Get a specific health catalog item by ID.
    """
    item = session.get(HealthCatalogItem, item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Health catalog item not found"
        )

    if item.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this health catalog item"
        )

    return item


@router.put("/{item_id}", response_model=HealthCatalogItemResponse)
def update_health_item(
    item_id: int,
    item_data: HealthCatalogItemUpdate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    Update an existing health catalog item.

    All fields are optional. Only provided fields will be updated.
    """
    item = session.get(HealthCatalogItem, item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Health catalog item not found"
        )

    if item.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this health catalog item"
        )

    # Update fields
    update_data = item_data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(item, key, value)

    item.updated_at = datetime.utcnow()
    session.add(item)
    session.commit()
    session.refresh(item)

    return item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_health_item(
    item_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    Delete a health catalog item.
    """
    item = session.get(HealthCatalogItem, item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Health catalog item not found"
        )

    if item.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this health catalog item"
        )

    session.delete(item)
    session.commit()

    return None
