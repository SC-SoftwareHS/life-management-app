# Data Model Documentation
## AI-Assisted Life Management Application

**Version:** 1.0 MVP
**Date:** 2025-10-16

---

## 1. Overview

This document defines the complete database schema using SQLModel (SQLAlchemy 2.x + Pydantic). All models include:
- Primary keys (auto-incrementing integers)
- Timestamps (created_at, updated_at)
- Foreign keys with proper relationships
- Type hints for Python/Pydantic validation

---

## 2. Core Models

### 2.1 User

**Purpose:** Authentication and user profile

```python
class User(SQLModel, table=True):
    __tablename__ = "users"

    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(unique=True, index=True, max_length=50)
    email: str | None = Field(default=None, max_length=100)
    hashed_password: str = Field(max_length=255)
    full_name: str | None = Field(default=None, max_length=100)
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    goals: list["Goal"] = Relationship(back_populates="user")
    habits: list["Habit"] = Relationship(back_populates="user")
    tasks: list["Task"] = Relationship(back_populates="user")
    contacts: list["Contact"] = Relationship(back_populates="user")
    references: list["Reference"] = Relationship(back_populates="user")
    entries: list["Entry"] = Relationship(back_populates="user")
    health_items: list["HealthCatalogItem"] = Relationship(back_populates="user")
    financial_accounts: list["FinancialAccount"] = Relationship(back_populates="user")
    conflict_topics: list["ConflictTopic"] = Relationship(back_populates="user")
```

**Indexes:**
- `username` (unique)
- `email` (optional, for future use)

**Constraints:**
- `username` required, unique
- `hashed_password` required (bcrypt hash)

---

### 2.2 LifeArea (Enum)

**Purpose:** 8 predefined life dimensions

```python
class LifeAreaEnum(str, Enum):
    PHYSICAL_HEALTH = "physical_health"
    HOBBY = "hobby"
    INCOME_EXPENSES = "income_expenses"
    ASSETS_LIABILITIES = "assets_liabilities"
    ONE_ON_ONE = "one_on_one"
    FAMILY_FRIENDS = "family_friends"
    POLITICS = "politics"
    SPIRITUAL = "spiritual"

class LifeArea(SQLModel, table=True):
    __tablename__ = "life_areas"

    id: int | None = Field(default=None, primary_key=True)
    name: LifeAreaEnum = Field(index=True)
    display_name: str = Field(max_length=50)
    description: str | None = None
    icon: str | None = Field(default=None, max_length=50)  # e.g., emoji or icon name
    created_at: datetime = Field(default_factory=datetime.utcnow)
```

**Seed Data:**
1. Physical/Health - "Optimize physical wellbeing"
2. Hobby - "Pursue creative interests"
3. Income & Expenses - "Monitor cash flow"
4. Assets & Liabilities - "Manage wealth and debts"
5. One-on-One Relationship - "Strengthen primary partnership"
6. Family & Friends - "Nurture social connections"
7. Politics/Civics - "Engage with civic duties"
8. Spiritual - "Deepen faith and spiritual practices"

---

## 3. Goal System

### 3.1 Goal

**Purpose:** Short/Medium/Long term objectives

```python
class GoalTimeframe(str, Enum):
    SHORT = "short"      # < 3 months
    MEDIUM = "medium"    # 3-12 months
    LONG = "long"        # 12+ months

class GoalStatus(str, Enum):
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    ABANDONED = "abandoned"

class Goal(SQLModel, table=True):
    __tablename__ = "goals"

    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True)
    title: str = Field(max_length=200)
    description: str | None = None
    timeframe: GoalTimeframe = Field(index=True)
    status: GoalStatus = Field(default=GoalStatus.NOT_STARTED, index=True)
    progress_percentage: int = Field(default=0, ge=0, le=100)
    due_date: date | None = None
    contact_id: int | None = Field(default=None, foreign_key="contacts.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    user: User = Relationship(back_populates="goals")
    contact: "Contact" | None = Relationship()
    areas: list["LifeArea"] = Relationship(link_model="GoalAreaLink")
```

### 3.2 GoalAreaLink (Association Table)

**Purpose:** Many-to-many between Goals and Life Areas

```python
class GoalAreaLink(SQLModel, table=True):
    __tablename__ = "goal_area_links"

    goal_id: int = Field(foreign_key="goals.id", primary_key=True)
    area_id: int = Field(foreign_key="life_areas.id", primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
```

---

## 4. Habit System

### 4.1 Habit

**Purpose:** Build good habits, break bad ones

```python
class HabitType(str, Enum):
    GAIN = "gain"  # Build a good habit
    LOSE = "lose"  # Break a bad habit

class Habit(SQLModel, table=True):
    __tablename__ = "habits"

    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True)
    name: str = Field(max_length=200)
    description: str | None = None
    habit_type: HabitType = Field(index=True)
    frequency_description: str = Field(max_length=100)  # "daily", "3x/week", etc.
    current_streak: int = Field(default=0, ge=0)
    longest_streak: int = Field(default=0, ge=0)
    last_checkin_date: date | None = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    user: User = Relationship(back_populates="habits")
    areas: list["LifeArea"] = Relationship(link_model="HabitAreaLink")
    checkins: list["HabitCheckin"] = Relationship(back_populates="habit")
```

### 4.2 HabitAreaLink

```python
class HabitAreaLink(SQLModel, table=True):
    __tablename__ = "habit_area_links"

    habit_id: int = Field(foreign_key="habits.id", primary_key=True)
    area_id: int = Field(foreign_key="life_areas.id", primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
```

### 4.3 HabitCheckin

**Purpose:** Track individual check-ins for streak calculation

```python
class HabitCheckin(SQLModel, table=True):
    __tablename__ = "habit_checkins"

    id: int | None = Field(default=None, primary_key=True)
    habit_id: int = Field(foreign_key="habits.id", index=True)
    checkin_date: date = Field(index=True)
    notes: str | None = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    habit: Habit = Relationship(back_populates="checkins")

    # Unique constraint: one check-in per habit per day
    __table_args__ = (
        UniqueConstraint('habit_id', 'checkin_date', name='unique_habit_checkin'),
    )
```

---

## 5. Task System

### 5.1 Task

**Purpose:** Todo list management

```python
class TaskStatus(str, Enum):
    TODO = "todo"
    DOING = "doing"
    DONE = "done"

class TaskPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class Task(SQLModel, table=True):
    __tablename__ = "tasks"

    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True)
    area_id: int = Field(foreign_key="life_areas.id", index=True)
    title: str = Field(max_length=200)
    description: str | None = None
    status: TaskStatus = Field(default=TaskStatus.TODO, index=True)
    priority: TaskPriority = Field(default=TaskPriority.MEDIUM)
    due_date: date | None = None
    contact_id: int | None = Field(default=None, foreign_key="contacts.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    completed_at: datetime | None = None

    # Relationships
    user: User = Relationship(back_populates="tasks")
    area: LifeArea = Relationship()
    contact: "Contact" | None = Relationship()
```

**Indexes:**
- `user_id, status` (composite for filtering)
- `area_id`
- `due_date`

---

## 6. Contact System

### 6.1 Contact

**Purpose:** People across all life areas

```python
class Contact(SQLModel, table=True):
    __tablename__ = "contacts"

    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True)
    name: str = Field(max_length=100)
    role: str | None = Field(default=None, max_length=100)  # "Doctor", "Friend", "Boss"
    phone: str | None = Field(default=None, max_length=20)
    email: str | None = Field(default=None, max_length=100)
    address: str | None = None
    birthday: date | None = None
    notes: str | None = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    user: User = Relationship(back_populates="contacts")
    areas: list["LifeArea"] = Relationship(link_model="ContactAreaLink")
```

### 6.2 ContactAreaLink

```python
class ContactAreaLink(SQLModel, table=True):
    __tablename__ = "contact_area_links"

    contact_id: int = Field(foreign_key="contacts.id", primary_key=True)
    area_id: int = Field(foreign_key="life_areas.id", primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
```

**Age Calculation Helper:**
```python
def calculate_age_ymd(birthday: date, reference_date: date = None) -> dict:
    """Returns {years, months, days}"""
    if not reference_date:
        reference_date = date.today()

    years = reference_date.year - birthday.year
    months = reference_date.month - birthday.month
    days = reference_date.day - birthday.day

    if days < 0:
        months -= 1
        days += (reference_date.replace(day=1) - timedelta(days=1)).day

    if months < 0:
        years -= 1
        months += 12

    return {"years": years, "months": months, "days": days}
```

---

## 7. Reference System

### 7.1 Reference

**Purpose:** Websites, scriptures, laws, notes

```python
class ReferenceType(str, Enum):
    WEBSITE = "website"
    SCRIPTURE = "scripture"
    LAW = "law"
    NOTE = "note"

class LawLevel(str, Enum):
    FEDERAL = "federal"
    STATE = "state"
    LOCAL = "local"

class Reference(SQLModel, table=True):
    __tablename__ = "references"

    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True)
    title: str = Field(max_length=200)
    type: ReferenceType = Field(index=True)
    url: str | None = Field(default=None, max_length=500)
    content: str | None = None  # For scriptures, laws, notes
    law_level: LawLevel | None = None  # Only if type=LAW
    tags: str | None = None  # Comma-separated for filtering
    notes: str | None = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    user: User = Relationship(back_populates="references")
    areas: list["LifeArea"] = Relationship(link_model="ReferenceAreaLink")
```

### 7.2 ReferenceAreaLink

```python
class ReferenceAreaLink(SQLModel, table=True):
    __tablename__ = "reference_area_links"

    reference_id: int = Field(foreign_key="references.id", primary_key=True)
    area_id: int = Field(foreign_key="life_areas.id", primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
```

---

## 8. Health System

### 8.1 HealthCatalogItem

**Purpose:** Polymorphic catalog for doctors, food, supplements, meds, motion

```python
class HealthCatalogType(str, Enum):
    DOCTOR = "doctor"
    FOOD = "food"
    SUPPLEMENT = "supplement"
    MEDICATION = "medication"
    MOTION = "motion"  # Walk, Run, Yoga, etc.

class HealthCatalogItem(SQLModel, table=True):
    __tablename__ = "health_catalog_items"

    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True)
    catalog_type: HealthCatalogType = Field(index=True)
    name: str = Field(max_length=200)
    description: str | None = None

    # Type-specific fields (optional, use JSON for flexibility)
    doctor_specialty: str | None = Field(default=None, max_length=100)  # DOCTOR
    doctor_phone: str | None = Field(default=None, max_length=20)       # DOCTOR

    food_category: str | None = Field(default=None, max_length=50)      # FOOD

    supplement_dosage: str | None = Field(default=None, max_length=50)  # SUPPLEMENT

    medication_dosage: str | None = Field(default=None, max_length=50)  # MEDICATION
    medication_frequency: str | None = Field(default=None, max_length=100)

    motion_duration: str | None = Field(default=None, max_length=50)    # MOTION (e.g., "30 min")

    frequency_description: str | None = Field(default=None, max_length=100)  # General frequency
    notes: str | None = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    user: User = Relationship(back_populates="health_items")
```

**Indexes:**
- `user_id, catalog_type` (composite)

**Alternative Design (More Normalized):**
Could split into 5 separate tables (DoctorCatalog, FoodCatalog, etc.) but polymorphic approach is simpler for MVP.

---

## 9. Finance System

### 9.1 FinancialAccount

**Purpose:** Banking, assets, liabilities

```python
class FinancialAccountType(str, Enum):
    BANKING = "banking"      # Checking, savings
    ASSET = "asset"          # Property, investments, valuables
    LIABILITY = "liability"  # Loans, mortgages, credit cards

class FinancialAccount(SQLModel, table=True):
    __tablename__ = "financial_accounts"

    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True)
    account_type: FinancialAccountType = Field(index=True)
    name: str = Field(max_length=200)  # "Chase Checking", "Home Mortgage", "Tesla Stock"
    institution: str | None = Field(default=None, max_length=100)
    account_number_last4: str | None = Field(default=None, max_length=4)  # For reference
    current_balance: float | None = None
    interest_rate: float | None = None  # For liabilities/investments
    due_date: date | None = None  # For liabilities
    notes: str | None = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    user: User = Relationship(back_populates="financial_accounts")
```

**Indexes:**
- `user_id, account_type`

**Future Enhancement:**
- Transaction tracking (separate `Transaction` table)
- Net worth calculation

---

## 10. Entry System

### 10.1 Entry

**Purpose:** Free-text journal entries per area

```python
class Entry(SQLModel, table=True):
    __tablename__ = "entries"

    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True)
    area_id: int = Field(foreign_key="life_areas.id", index=True)
    title: str | None = Field(default=None, max_length=200)
    content: str
    entry_date: date = Field(default_factory=date.today, index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    user: User = Relationship(back_populates="entries")
    area: LifeArea = Relationship()
```

**Indexes:**
- `user_id, area_id`
- `entry_date` (for chronological queries)

---

## 11. One-on-One Specific

### 11.1 ConflictTopic

**Purpose:** Track 3 main argument topics in primary relationship

```python
class ConflictTopic(SQLModel, table=True):
    __tablename__ = "conflict_topics"

    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True)
    topic: str = Field(max_length=200)
    description: str | None = None
    resolution_strategy: str | None = None
    progress_notes: str | None = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    user: User = Relationship(back_populates="conflict_topics")
```

**Constraint:** User can have max 3 conflict topics (enforced in application logic)

---

## 12. AI Content Cache (Optional)

### 12.1 AIContentCache

**Purpose:** Cache AI-generated verses/insights to reduce API calls

```python
class AIContentType(str, Enum):
    BIBLE_VERSE = "bible_verse"
    INSIGHT = "insight"
    SUGGESTION = "suggestion"

class AIContentCache(SQLModel, table=True):
    __tablename__ = "ai_content_cache"

    id: int | None = Field(default=None, primary_key=True)
    area_id: int | None = Field(default=None, foreign_key="life_areas.id")
    content_type: AIContentType = Field(index=True)
    prompt_hash: str = Field(max_length=64, index=True)  # SHA-256 of prompt for deduplication
    content: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    expires_at: datetime | None = None  # Optional TTL

    # Unique constraint on prompt_hash for dedup
    __table_args__ = (
        UniqueConstraint('prompt_hash', name='unique_prompt_hash'),
    )
```

---

## 13. Database Relationships Summary

```
User (1) ──── (M) Goal
User (1) ──── (M) Habit
User (1) ──── (M) Task
User (1) ──── (M) Contact
User (1) ──── (M) Reference
User (1) ──── (M) Entry
User (1) ──── (M) HealthCatalogItem
User (1) ──── (M) FinancialAccount
User (1) ──── (M) ConflictTopic

LifeArea (M) ──── (M) Goal      via GoalAreaLink
LifeArea (M) ──── (M) Habit     via HabitAreaLink
LifeArea (1) ──── (M) Task      direct FK
LifeArea (M) ──── (M) Contact   via ContactAreaLink
LifeArea (M) ──── (M) Reference via ReferenceAreaLink
LifeArea (1) ──── (M) Entry     direct FK

Habit (1) ──── (M) HabitCheckin

Contact (1) ──── (M) Goal  (optional)
Contact (1) ──── (M) Task  (optional)
```

---

## 14. Indexes Summary

**Critical Indexes:**
```sql
CREATE INDEX idx_goals_user_status ON goals(user_id, status);
CREATE INDEX idx_habits_user_type ON habits(user_id, habit_type);
CREATE INDEX idx_tasks_user_status ON tasks(user_id, status);
CREATE INDEX idx_tasks_area ON tasks(area_id);
CREATE INDEX idx_contacts_user ON contacts(user_id);
CREATE INDEX idx_health_user_type ON health_catalog_items(user_id, catalog_type);
CREATE INDEX idx_entries_user_area ON entries(user_id, area_id);
CREATE INDEX idx_entries_date ON entries(entry_date);
```

---

## 15. Sample Data

### 15.1 User
```python
{
    "username": "holistic_hannah",
    "email": "hannah@example.com",
    "full_name": "Hannah Smith",
    "hashed_password": "$2b$12$..."
}
```

### 15.2 Goal
```python
{
    "user_id": 1,
    "title": "Run 5K in under 30 minutes",
    "timeframe": "short",
    "status": "in_progress",
    "progress_percentage": 45,
    "due_date": "2025-12-31",
    "areas": ["physical_health", "hobby"]
}
```

### 15.3 Habit
```python
{
    "user_id": 1,
    "name": "Morning meditation",
    "habit_type": "gain",
    "frequency_description": "daily",
    "current_streak": 12,
    "longest_streak": 30,
    "areas": ["spiritual"]
}
```

### 15.4 Contact
```python
{
    "user_id": 1,
    "name": "Dr. Sarah Johnson",
    "role": "Primary Care Physician",
    "phone": "555-0123",
    "email": "sjohnson@clinic.com",
    "birthday": "1975-06-15",
    "areas": ["physical_health"]
}
```

### 15.5 HealthCatalogItem
```python
{
    "user_id": 1,
    "catalog_type": "supplement",
    "name": "Vitamin D3",
    "supplement_dosage": "2000 IU",
    "frequency_description": "daily with breakfast"
}
```

### 15.6 FinancialAccount
```python
{
    "user_id": 1,
    "account_type": "liability",
    "name": "Home Mortgage",
    "institution": "Wells Fargo",
    "current_balance": 285000.00,
    "interest_rate": 3.75,
    "due_date": "2025-01-15"
}
```

---

## 16. Migration Strategy

### 16.1 Alembic Initial Migration
```bash
alembic revision --autogenerate -m "Initial schema"
alembic upgrade head
```

### 16.2 Seed Life Areas
```python
# In seed script or migration
areas = [
    {"name": "physical_health", "display_name": "Physical/Health"},
    {"name": "hobby", "display_name": "Hobby"},
    {"name": "income_expenses", "display_name": "Income & Expenses"},
    {"name": "assets_liabilities", "display_name": "Assets & Liabilities"},
    {"name": "one_on_one", "display_name": "One-on-One Relationship"},
    {"name": "family_friends", "display_name": "Family & Friends"},
    {"name": "politics", "display_name": "Politics/Civics"},
    {"name": "spiritual", "display_name": "Spiritual"},
]
```

---

## 17. Constraints & Validation

### 17.1 Database-Level
- Foreign keys enforced
- Unique constraints (username, habit check-in per day, etc.)
- NOT NULL on required fields

### 17.2 Application-Level (Pydantic)
- String length limits
- Email validation (if email field used)
- Date range validation
- Percentage (0-100)
- Enum validation

### 17.3 Business Logic
- Max 3 conflict topics per user (One-on-One)
- Habit streak resets if gap > 1 day (for "daily" habits)
- Goal progress percentage cannot decrease (optional rule)

---

## 18. Future Enhancements

### Post-MVP Schema Changes:
1. **Soft Deletes:** Add `deleted_at` timestamp to all tables
2. **Audit Trail:** Track who changed what and when
3. **Reminders:** `Reminder` table linked to tasks/goals
4. **Notifications:** `Notification` table for user alerts
5. **Tags:** Dedicated `Tag` table instead of comma-separated strings
6. **Transactions:** Financial transaction tracking
7. **Attachments:** Support for file uploads (S3/local)
8. **Sharing:** Multi-user support, permission system

---

## 19. Related Documentation
- [PRD.md](PRD.md) - Product requirements
- [Architecture.md](Architecture.md) - System design
- [API-Schema.md](API-Schema.md) - Endpoint specifications
