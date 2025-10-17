"""One-on-One Conflict Resolution endpoints"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import List
from datetime import datetime

from ..db import get_session
from ..schemas import ConflictTopicCreate, ConflictTopicUpdate, ConflictTopicResponse
from ..models import ConflictTopic, User
from ..auth import get_current_user

router = APIRouter()


@router.post("/", response_model=ConflictTopicResponse, status_code=status.HTTP_201_CREATED)
def create_conflict_topic(
    topic_data: ConflictTopicCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    Create a new conflict topic.

    Maximum of 3 topics allowed per user (representing the 3 main relationship topics).

    - **topic**: Topic name/title
    - **description**: Description of the conflict or issue
    - **resolution_notes**: Optional notes on resolution progress
    - **is_resolved**: Whether the topic is resolved (defaults to false)
    """
    # Check if user already has 3 topics
    statement = select(ConflictTopic).where(ConflictTopic.user_id == current_user.id)
    existing_topics = session.exec(statement).all()

    if len(existing_topics) >= 3:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Maximum of 3 conflict topics allowed. Please delete or resolve an existing topic first."
        )

    # Create conflict topic
    topic = ConflictTopic(
        user_id=current_user.id,
        topic=topic_data.topic,
        description=topic_data.description,
        resolution_notes=topic_data.resolution_notes,
        is_resolved=topic_data.is_resolved or False
    )
    session.add(topic)
    session.commit()
    session.refresh(topic)

    return topic


@router.get("/", response_model=List[ConflictTopicResponse])
def list_conflict_topics(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    List all conflict topics for the current user.

    Returns up to 3 topics representing the 3 main relationship areas.
    """
    statement = select(ConflictTopic).where(ConflictTopic.user_id == current_user.id)
    topics = session.exec(statement).all()
    return topics


@router.get("/{topic_id}", response_model=ConflictTopicResponse)
def get_conflict_topic(
    topic_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    Get a specific conflict topic by ID.
    """
    topic = session.get(ConflictTopic, topic_id)
    if not topic:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conflict topic not found"
        )

    if topic.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this conflict topic"
        )

    return topic


@router.put("/{topic_id}", response_model=ConflictTopicResponse)
def update_conflict_topic(
    topic_id: int,
    topic_data: ConflictTopicUpdate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    Update an existing conflict topic.

    All fields are optional. Only provided fields will be updated.

    Use this to add resolution notes or mark a topic as resolved.
    """
    topic = session.get(ConflictTopic, topic_id)
    if not topic:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conflict topic not found"
        )

    if topic.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this conflict topic"
        )

    # Update fields
    update_data = topic_data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(topic, key, value)

    topic.updated_at = datetime.utcnow()
    session.add(topic)
    session.commit()
    session.refresh(topic)

    return topic


@router.delete("/{topic_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_conflict_topic(
    topic_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    Delete a conflict topic.

    This frees up a slot for a new topic (max 3 topics allowed).
    """
    topic = session.get(ConflictTopic, topic_id)
    if not topic:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conflict topic not found"
        )

    if topic.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this conflict topic"
        )

    session.delete(topic)
    session.commit()

    return None
