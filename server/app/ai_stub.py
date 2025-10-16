"""AI content stub module - Placeholder responses for MVP"""
from typing import Dict

# Static Bible verses for each life area
BIBLE_VERSES: Dict[str, Dict[str, str]] = {
    "physical_health": {
        "reference": "Philippians 4:13",
        "text": "I can do all things through Christ who strengthens me."
    },
    "hobby": {
        "reference": "Colossians 3:23",
        "text": "Whatever you do, work heartily, as for the Lord and not for men."
    },
    "income_expenses": {
        "reference": "Proverbs 21:5",
        "text": "The plans of the diligent lead surely to abundance, but everyone who is hasty comes only to poverty."
    },
    "assets_liabilities": {
        "reference": "Proverbs 22:7",
        "text": "The rich rules over the poor, and the borrower is the slave of the lender."
    },
    "one_on_one": {
        "reference": "Ephesians 4:2-3",
        "text": "Be completely humble and gentle; be patient, bearing with one another in love."
    },
    "family_friends": {
        "reference": "Proverbs 17:17",
        "text": "A friend loves at all times, and a brother is born for adversity."
    },
    "politics": {
        "reference": "Micah 6:8",
        "text": "He has told you, O man, what is good; and what does the Lord require of you but to do justice, and to love kindness, and to walk humbly with your God?"
    },
    "spiritual": {
        "reference": "Psalm 46:10",
        "text": "Be still, and know that I am God. I will be exalted among the nations, I will be exalted in the earth!"
    }
}

# Static insights for each life area
INSIGHTS: Dict[str, str] = {
    "physical_health": "Consider setting a consistent bedtime to improve sleep quality and energy levels.",
    "hobby": "Schedule 15 minutes of 'play time' with your hobby each day, even if it's just sketching or brainstorming.",
    "income_expenses": "Track every expense for one week to identify spending patterns and find easy cuts.",
    "assets_liabilities": "Focus on paying off your highest interest rate debt first (avalanche method) to minimize total interest paid.",
    "one_on_one": "Schedule a weekly 'check-in' conversation with your partner to discuss what's going well and what needs attention.",
    "family_friends": "Set monthly reminders to reach out to friends you haven't connected with recently, even just a quick text.",
    "politics": "Subscribe to your local city council meeting agendas to stay informed about decisions affecting your community.",
    "spiritual": "Start your day with 5 minutes of quiet prayer or meditation before checking your phone."
}

# Default fallbacks
DEFAULT_VERSE = {
    "reference": "Psalm 23:1",
    "text": "The Lord is my shepherd; I shall not want."
}

DEFAULT_INSIGHT = "Keep striving toward your goals in this area. Small consistent steps lead to big changes."


def generate_bible_verse(area: str) -> Dict[str, str]:
    """
    Generate (return static) Bible verse for a life area.

    Args:
        area: Life area name (e.g., "physical_health", "spiritual")

    Returns:
        Dict with 'reference' and 'text' keys

    Note: In MVP, this returns static content. In Phase 2, this will
    call OpenAI/Anthropic/local LLM to generate dynamic verses.
    """
    return BIBLE_VERSES.get(area, DEFAULT_VERSE)


def generate_insight(area: str) -> str:
    """
    Generate (return static) insight for a life area.

    Args:
        area: Life area name (e.g., "physical_health", "spiritual")

    Returns:
        Insight string (1-2 sentences)

    Note: In MVP, this returns static content. In Phase 2, this will
    call an AI API to generate personalized insights based on user data.
    """
    return INSIGHTS.get(area, DEFAULT_INSIGHT)


def generate_goal_suggestions(area: str, user_goals: list = None) -> list:
    """
    Generate goal suggestions for a life area.

    Note: Not implemented in MVP. Returns empty list.
    Future: Will use AI to suggest goals based on area and existing goals.
    """
    return []


def generate_habit_recommendations(area: str, user_habits: list = None) -> list:
    """
    Generate habit recommendations for a life area.

    Note: Not implemented in MVP. Returns empty list.
    Future: Will use AI to suggest habits based on area and existing habits.
    """
    return []
