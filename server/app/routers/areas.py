"""Life Areas endpoints"""
from fastapi import APIRouter
from ..schemas import LifeAreaResponse
from ..models import LifeAreaEnum

router = APIRouter()


@router.get("/", response_model=list[LifeAreaResponse])
def list_areas():
    """
    Get all 8 predefined life areas.

    Returns static list of life areas that organize all content in the app.
    """
    # Static list of 8 life areas
    areas = [
        {
            "id": 1,
            "name": LifeAreaEnum.PHYSICAL_HEALTH,
            "display_name": "Physical/Health",
            "description": "Optimize physical wellbeing",
            "icon": "💪"
        },
        {
            "id": 2,
            "name": LifeAreaEnum.HOBBY,
            "display_name": "Hobby",
            "description": "Pursue creative interests",
            "icon": "🎨"
        },
        {
            "id": 3,
            "name": LifeAreaEnum.INCOME_EXPENSES,
            "display_name": "Income & Expenses",
            "description": "Monitor cash flow",
            "icon": "💰"
        },
        {
            "id": 4,
            "name": LifeAreaEnum.ASSETS_LIABILITIES,
            "display_name": "Assets & Liabilities",
            "description": "Manage wealth and debts",
            "icon": "🏦"
        },
        {
            "id": 5,
            "name": LifeAreaEnum.ONE_ON_ONE,
            "display_name": "One-on-One Relationship",
            "description": "Strengthen primary partnership",
            "icon": "💑"
        },
        {
            "id": 6,
            "name": LifeAreaEnum.FAMILY_FRIENDS,
            "display_name": "Family & Friends",
            "description": "Nurture social connections",
            "icon": "👨‍👩‍👧‍👦"
        },
        {
            "id": 7,
            "name": LifeAreaEnum.POLITICS,
            "display_name": "Politics/Civics",
            "description": "Engage with civic duties",
            "icon": "🗳️"
        },
        {
            "id": 8,
            "name": LifeAreaEnum.SPIRITUAL,
            "display_name": "Spiritual",
            "description": "Deepen faith and spiritual practices",
            "icon": "🙏"
        }
    ]
    return areas
