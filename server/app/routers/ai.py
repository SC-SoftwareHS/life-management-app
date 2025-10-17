"""AI-generated content endpoints (stubbed for MVP)"""
from fastapi import APIRouter, Query
from datetime import datetime

from ..schemas import AIVerseResponse, AIInsightResponse
from ..ai_stub import generate_bible_verse, generate_insight

router = APIRouter()


@router.get("/verse", response_model=AIVerseResponse)
def get_bible_verse(
    area: str = Query(..., description="Life area name (e.g., 'physical_health', 'spiritual')")
):
    """
    Get AI-generated Bible verse for a life area.

    **Note:** In MVP, this returns static placeholder content.
    In Phase 2, this will call an AI API to generate dynamic verses.

    - **area**: One of the 8 life area names
    """
    verse_data = generate_bible_verse(area)

    return AIVerseResponse(
        reference=verse_data["reference"],
        text=verse_data["text"],
        area=area,
        generated_at=datetime.utcnow()
    )


@router.get("/insight", response_model=AIInsightResponse)
def get_insight(
    area: str = Query(..., description="Life area name (e.g., 'physical_health', 'spiritual')")
):
    """
    Get AI-generated insight/tip for a life area.

    **Note:** In MVP, this returns static placeholder content.
    In Phase 2, this will call an AI API to generate personalized insights
    based on user data and goals.

    - **area**: One of the 8 life area names
    """
    insight_text = generate_insight(area)

    return AIInsightResponse(
        insight=insight_text,
        area=area,
        generated_at=datetime.utcnow()
    )
