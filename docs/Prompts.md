# AI Prompts Documentation
## AI-Assisted Life Management Application

**Version:** 1.0 MVP
**Date:** 2025-10-16

---

## Overview

This document defines the AI prompts used to generate inspirational content for each life area. In the MVP, these prompts return **static placeholders** via `ai_stub.py`. In future releases, these will be sent to OpenAI, Anthropic Claude, or a local LLM.

---

## Prompt Structure

Each prompt follows this pattern:

```
System Context + Life Area Context + Output Format Instructions
```

---

## 1. Bible Verse Generation

### Generic Prompt Template

```
You are a spiritual counselor helping someone grow in their faith and life management.

Generate an encouraging Bible verse relevant to {LIFE_AREA}.

Requirements:
- Include book, chapter, and verse reference
- Provide the full verse text
- Choose verses that inspire action and growth
- Avoid doom/judgment verses; focus on hope and strength

Output format (JSON):
{
  "reference": "Book Chapter:Verse",
  "text": "Full verse text here"
}
```

### Area-Specific Prompts

**Physical/Health:**
```
Generate a Bible verse about caring for the body as a temple, strength, health, or discipline related to physical wellbeing.

Examples: 1 Corinthians 6:19-20 (body is a temple), Philippians 4:13 (strength through Christ), 3 John 1:2 (health and prosperity)
```

**Hobby:**
```
Generate a Bible verse about creativity, using your hands, talents, or work as worship.

Examples: Colossians 3:23 (work heartily), Exodus 35:35 (filled with skill), Psalm 90:17 (establish the work of our hands)
```

**Income & Expenses:**
```
Generate a Bible verse about stewardship, provision, managing money wisely, or trusting God financially.

Examples: Proverbs 21:5 (diligent planning), Luke 16:10 (faithful with little), Malachi 3:10 (bring tithes)
```

**Assets & Liabilities:**
```
Generate a Bible verse about wealth, debt, financial freedom, or laying up treasures.

Examples: Proverbs 22:7 (borrower is slave to lender), Matthew 6:19-21 (treasures in heaven), Romans 13:8 (owe no one anything)
```

**One-on-One Relationship:**
```
Generate a Bible verse about marriage, partnership, love, patience, or unity in relationships.

Examples: Ephesians 4:2-3 (bear with one another), 1 Corinthians 13:4-7 (love is patient), Ecclesiastes 4:9-12 (two are better)
```

**Family & Friends:**
```
Generate a Bible verse about family, friendship, community, honoring relationships, or love.

Examples: Proverbs 17:17 (friend loves at all times), Ephesians 6:2 (honor father and mother), 1 John 4:7 (love one another)
```

**Politics/Civics:**
```
Generate a Bible verse about justice, leadership, governing, civic duty, or righteousness in society.

Examples: Micah 6:8 (act justly, love mercy), Romans 13:1 (submit to authorities), Proverbs 29:2 (when righteous increase)
```

**Spiritual:**
```
Generate a Bible verse about prayer, faith, spiritual growth, devotion, or walking with God.

Examples: Philippians 4:6-7 (prayer and peace), Psalm 46:10 (be still and know), Hebrews 11:1 (faith is confidence)
```

---

## 2. Insight Generation

### Generic Prompt Template

```
You are a life coach helping someone improve their {LIFE_AREA}.

Based on typical challenges people face in {LIFE_AREA}, provide a short, actionable insight or tip (1-2 sentences).

Requirements:
- Practical and specific
- Actionable (user can do something today)
- Encouraging tone
- Avoid generic advice
- Maximum 2 sentences

Output format (JSON):
{
  "insight": "Your actionable tip here."
}
```

### Area-Specific Prompts

**Physical/Health:**
```
Provide a health tip related to:
- Sleep hygiene
- Nutrition basics
- Exercise consistency
- Stress management
- Hydration
- Preventive care

Example: "Consider setting a consistent bedtime to improve sleep quality and energy levels."
```

**Hobby:**
```
Provide a creativity tip related to:
- Overcoming creative blocks
- Dedicating time to hobbies
- Trying new techniques
- Sharing your work
- Finding inspiration

Example: "Schedule 15 minutes of 'play time' with your hobby each day, even if it's just sketching or brainstorming."
```

**Income & Expenses:**
```
Provide a financial management tip related to:
- Tracking expenses
- Budgeting methods
- Saving strategies
- Reducing unnecessary spending
- Income diversification

Example: "Track every expense for one week to identify spending patterns and find easy cuts."
```

**Assets & Liabilities:**
```
Provide a wealth-building or debt reduction tip related to:
- Paying down high-interest debt
- Building emergency funds
- Investing basics
- Asset allocation
- Net worth tracking

Example: "Focus on paying off your highest interest rate debt first (avalanche method) to minimize total interest paid."
```

**One-on-One Relationship:**
```
Provide a relationship tip related to:
- Communication skills
- Quality time
- Conflict resolution
- Appreciation/gratitude
- Emotional connection

Example: "Schedule a weekly 'check-in' conversation with your partner to discuss what's going well and what needs attention."
```

**Family & Friends:**
```
Provide a social connection tip related to:
- Staying in touch regularly
- Remembering important dates
- Quality time with loved ones
- Conflict resolution
- Showing appreciation

Example: "Set monthly reminders to reach out to friends you haven't connected with recently, even just a quick text."
```

**Politics/Civics:**
```
Provide a civic engagement tip related to:
- Staying informed
- Local involvement
- Contacting representatives
- Voting
- Community service

Example: "Subscribe to your local city council meeting agendas to stay informed about decisions affecting your community."
```

**Spiritual:**
```
Provide a spiritual growth tip related to:
- Daily devotional practices
- Prayer consistency
- Scripture study
- Meditation/contemplation
- Serving others
- Community involvement

Example: "Start your day with 5 minutes of quiet prayer or meditation before checking your phone."
```

---

## 3. Goal Suggestions (Future)

### Prompt Template

```
Based on the user's current activity in {LIFE_AREA}, suggest 2-3 realistic goals they might want to set.

Context:
- Current goals: {USER_GOALS}
- Current habits: {USER_HABITS}
- Current tasks: {USER_TASKS}

Requirements:
- SMART goals (Specific, Measurable, Achievable, Relevant, Time-bound)
- Mix of short, medium, long-term
- Aligned with common growth areas
- Avoid duplicating existing goals

Output format (JSON):
{
  "suggestions": [
    {
      "title": "Goal title",
      "timeframe": "short|medium|long",
      "rationale": "Why this goal makes sense"
    }
  ]
}
```

---

## 4. Habit Recommendations (Future)

### Prompt Template

```
Suggest 2-3 habits that would support the user's goals in {LIFE_AREA}.

Current goals: {USER_GOALS}
Current habits: {USER_HABITS}

Requirements:
- Small, achievable habits (keystone habits)
- Clear frequency (daily, 3x/week, etc.)
- Both "gain" and "lose" habit types
- Avoid duplicating existing habits

Output format (JSON):
{
  "suggestions": [
    {
      "name": "Habit name",
      "type": "gain|lose",
      "frequency": "daily|3x/week|etc",
      "rationale": "How this supports goals"
    }
  ]
}
```

---

## 5. Conflict Resolution Strategies (One-on-One)

### Prompt Template

```
Provide a research-backed strategy for resolving relationship conflict around: {CONFLICT_TOPIC}

Requirements:
- Based on couples therapy best practices
- Specific, actionable steps
- Involves both partners
- Focuses on communication and understanding
- Avoids blame language

Output format (JSON):
{
  "strategy": "Detailed strategy description",
  "steps": [
    "Step 1",
    "Step 2",
    "Step 3"
  ],
  "resources": ["Book or article recommendation"]
}
```

**Examples:**
- Financial disagreements → Monthly budget meetings, "fun money" allowances
- Household chores → Weekly rotation chart, Sunday review meetings
- Quality time vs. personal space → Scheduled date nights + solo time blocks

---

## 6. Birthday Gift Ideas (Future)

### Prompt Template

```
Suggest thoughtful gift ideas for {CONTACT_NAME} based on:
- Relationship: {ROLE}
- Age: {AGE}
- Interests: {TAGS_OR_NOTES}
- Budget: ${BUDGET}

Requirements:
- 3-5 specific ideas
- Range of price points
- Thoughtful and personal
- Avoid generic suggestions

Output format (JSON):
{
  "ideas": [
    {
      "gift": "Gift description",
      "estimated_cost": "$XX",
      "why": "Why this fits them"
    }
  ]
}
```

---

## 7. Task Prioritization (Future)

### Prompt Template

```
Given these tasks: {TASK_LIST}

Suggest a priority order based on:
- Due dates
- Importance (health, finance, etc.)
- Dependencies
- Effort required

Output format (JSON):
{
  "prioritized_tasks": [
    {
      "task_id": 1,
      "suggested_priority": "high|medium|low",
      "rationale": "Why this priority"
    }
  ]
}
```

---

## Implementation Notes (MVP)

### Stub Responses

In `ai_stub.py`, hard-code responses for each area:

```python
BIBLE_VERSES = {
    "physical_health": {
        "reference": "Philippians 4:13",
        "text": "I can do all things through Christ who strengthens me."
    },
    "hobby": {
        "reference": "Colossians 3:23",
        "text": "Whatever you do, work heartily, as for the Lord and not for men."
    },
    # ... etc for all 8 areas
}

INSIGHTS = {
    "physical_health": "Consider setting a consistent bedtime to improve sleep quality and energy levels.",
    "hobby": "Schedule 15 minutes of 'play time' with your hobby each day, even if it's just sketching or brainstorming.",
    # ... etc
}

def generate_bible_verse(area: str) -> dict:
    return BIBLE_VERSES.get(area, BIBLE_VERSES["spiritual"])

def generate_insight(area: str) -> str:
    return INSIGHTS.get(area, "Keep striving toward your goals in this area.")
```

### Future AI Integration

When integrating real AI (Phase 2):

1. **Choose Provider:**
   - OpenAI GPT-4 (API key required, costs money)
   - Anthropic Claude (API key required)
   - Local LLM (Ollama, LM Studio - free, runs locally)

2. **Update `ai_stub.py` → `ai_service.py`:**
   ```python
   import openai  # or anthropic

   def generate_bible_verse(area: str) -> dict:
       prompt = VERSE_PROMPTS[area]
       response = openai.ChatCompletion.create(
           model="gpt-4",
           messages=[{"role": "user", "content": prompt}]
       )
       return parse_json_response(response)
   ```

3. **Add Caching:**
   - Store generated content in `AIContentCache` table
   - Check cache before calling API
   - Set TTL (e.g., 7 days) to keep content fresh

4. **Handle Errors:**
   - Fallback to stub content if API fails
   - Log errors for monitoring
   - Retry logic for transient failures

5. **Cost Management:**
   - Cache aggressively
   - Rate limit requests
   - Consider batch processing
   - Monitor API usage/costs

---

## Prompt Engineering Best Practices

1. **Be Specific:** Clearly define the output format and constraints
2. **Provide Examples:** Show the model what good output looks like
3. **Use System Messages:** Set the AI's role/persona
4. **Iterate:** Test and refine prompts based on output quality
5. **Safety:** Filter out inappropriate or harmful content
6. **Consistency:** Use the same format across all prompts

---

## Related Documents
- [PRD.md](PRD.md) - Product requirements
- [Architecture.md](Architecture.md) - System design
- [Implementation-Plan.md](Implementation-Plan.md) - Build steps
