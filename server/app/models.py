"""SQLModel database models for Life Management Application"""
from sqlmodel import Field, SQLModel, Relationship
from typing import Optional, List
from datetime import datetime, date
from enum import Enum


# ==================== ENUMS ====================

class LifeAreaEnum(str, Enum):
    """8 Life Areas"""
    PHYSICAL_HEALTH = "physical_health"
    HOBBY = "hobby"
    INCOME_EXPENSES = "income_expenses"
    ASSETS_LIABILITIES = "assets_liabilities"
    ONE_ON_ONE = "one_on_one"
    FAMILY_FRIENDS = "family_friends"
    POLITICS = "politics"
    SPIRITUAL = "spiritual"


class GoalTimeframe(str, Enum):
    """Goal timeframes"""
    SHORT = "short"      # < 3 months
    MEDIUM = "medium"    # 3-12 months
    LONG = "long"        # 12+ months


class GoalStatus(str, Enum):
    """Goal status options"""
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    ABANDONED = "abandoned"


class HabitType(str, Enum):
    """Habit types"""
    GAIN = "gain"  # Build a good habit
    LOSE = "lose"  # Break a bad habit


class TaskStatus(str, Enum):
    """Task status options"""
    TODO = "todo"
    DOING = "doing"
    DONE = "done"


class TaskPriority(str, Enum):
    """Task priority levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class ReferenceType(str, Enum):
    """Reference types"""
    WEBSITE = "website"
    SCRIPTURE = "scripture"
    LAW = "law"
    NOTE = "note"


class LawLevel(str, Enum):
    """Law levels (for reference type=law)"""
    FEDERAL = "federal"
    STATE = "state"
    LOCAL = "local"


class HealthCatalogType(str, Enum):
    """Health catalog item types"""
    DOCTOR = "doctor"
    FOOD = "food"
    SUPPLEMENT = "supplement"
    MEDICATION = "medication"
    MOTION = "motion"


class FinancialAccountType(str, Enum):
    """Financial account types"""
    BANKING = "banking"
    ASSET = "asset"
    LIABILITY = "liability"


# ==================== CORE MODELS ====================

class User(SQLModel, table=True):
    """User account"""
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(unique=True, index=True, max_length=50)
    email: Optional[str] = Field(default=None, max_length=100)
    hashed_password: str = Field(max_length=255)
    full_name: Optional[str] = Field(default=None, max_length=100)
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    goals: List["Goal"] = Relationship(back_populates="user")
    habits: List["Habit"] = Relationship(back_populates="user")
    tasks: List["Task"] = Relationship(back_populates="user")
    contacts: List["Contact"] = Relationship(back_populates="user")
    references: List["Reference"] = Relationship(back_populates="user")
    entries: List["Entry"] = Relationship(back_populates="user")
    health_items: List["HealthCatalogItem"] = Relationship(back_populates="user")
    financial_accounts: List["FinancialAccount"] = Relationship(back_populates="user")
    conflict_topics: List["ConflictTopic"] = Relationship(back_populates="user")


class LifeArea(SQLModel, table=True):
    """8 predefined life areas"""
    __tablename__ = "life_areas"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: LifeAreaEnum = Field(index=True)
    display_name: str = Field(max_length=50)
    description: Optional[str] = None
    icon: Optional[str] = Field(default=None, max_length=50)
    created_at: datetime = Field(default_factory=datetime.utcnow)


# ==================== GOAL SYSTEM ====================

class GoalAreaLink(SQLModel, table=True):
    """Many-to-many link between Goals and Life Areas"""
    __tablename__ = "goal_area_links"

    goal_id: int = Field(foreign_key="goals.id", primary_key=True)
    area_id: int = Field(foreign_key="life_areas.id", primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)


class Goal(SQLModel, table=True):
    """User goals with progress tracking"""
    __tablename__ = "goals"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True)
    title: str = Field(max_length=200)
    description: Optional[str] = None
    timeframe: GoalTimeframe = Field(index=True)
    status: GoalStatus = Field(default=GoalStatus.NOT_STARTED, index=True)
    progress_percentage: int = Field(default=0, ge=0, le=100)
    due_date: Optional[date] = None
    contact_id: Optional[int] = Field(default=None, foreign_key="contacts.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    user: User = Relationship(back_populates="goals")
    areas: List[LifeArea] = Relationship(link_model=GoalAreaLink)


# ==================== HABIT SYSTEM ====================

class HabitAreaLink(SQLModel, table=True):
    """Many-to-many link between Habits and Life Areas"""
    __tablename__ = "habit_area_links"

    habit_id: int = Field(foreign_key="habits.id", primary_key=True)
    area_id: int = Field(foreign_key="life_areas.id", primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)


class Habit(SQLModel, table=True):
    """User habits with streak tracking"""
    __tablename__ = "habits"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True)
    name: str = Field(max_length=200)
    description: Optional[str] = None
    habit_type: HabitType = Field(index=True)
    frequency_description: str = Field(max_length=100)
    current_streak: int = Field(default=0, ge=0)
    longest_streak: int = Field(default=0, ge=0)
    last_checkin_date: Optional[date] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    user: User = Relationship(back_populates="habits")
    areas: List[LifeArea] = Relationship(link_model=HabitAreaLink)
    checkins: List["HabitCheckin"] = Relationship(back_populates="habit")


class HabitCheckin(SQLModel, table=True):
    """Individual habit check-ins for streak calculation"""
    __tablename__ = "habit_checkins"

    id: Optional[int] = Field(default=None, primary_key=True)
    habit_id: int = Field(foreign_key="habits.id", index=True)
    checkin_date: date = Field(index=True)
    notes: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    habit: Habit = Relationship(back_populates="checkins")


# ==================== TASK SYSTEM ====================

class Task(SQLModel, table=True):
    """User tasks/todos"""
    __tablename__ = "tasks"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True)
    area_id: int = Field(foreign_key="life_areas.id", index=True)
    title: str = Field(max_length=200)
    description: Optional[str] = None
    status: TaskStatus = Field(default=TaskStatus.TODO, index=True)
    priority: TaskPriority = Field(default=TaskPriority.MEDIUM)
    due_date: Optional[date] = None
    contact_id: Optional[int] = Field(default=None, foreign_key="contacts.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = None

    # Relationships
    user: User = Relationship(back_populates="tasks")
    area: LifeArea = Relationship()


# ==================== CONTACT SYSTEM ====================

class ContactAreaLink(SQLModel, table=True):
    """Many-to-many link between Contacts and Life Areas"""
    __tablename__ = "contact_area_links"

    contact_id: int = Field(foreign_key="contacts.id", primary_key=True)
    area_id: int = Field(foreign_key="life_areas.id", primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)


class Contact(SQLModel, table=True):
    """Contacts across all life areas"""
    __tablename__ = "contacts"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True)
    name: str = Field(max_length=100)
    role: Optional[str] = Field(default=None, max_length=100)
    phone: Optional[str] = Field(default=None, max_length=20)
    email: Optional[str] = Field(default=None, max_length=100)
    address: Optional[str] = None
    birthday: Optional[date] = None
    notes: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    user: User = Relationship(back_populates="contacts")
    areas: List[LifeArea] = Relationship(link_model=ContactAreaLink)


# ==================== REFERENCE SYSTEM ====================

class ReferenceAreaLink(SQLModel, table=True):
    """Many-to-many link between References and Life Areas"""
    __tablename__ = "reference_area_links"

    reference_id: int = Field(foreign_key="references.id", primary_key=True)
    area_id: int = Field(foreign_key="life_areas.id", primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)


class Reference(SQLModel, table=True):
    """References (websites, scriptures, laws, notes)"""
    __tablename__ = "references"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True)
    title: str = Field(max_length=200)
    type: ReferenceType = Field(index=True)
    url: Optional[str] = Field(default=None, max_length=500)
    content: Optional[str] = None
    law_level: Optional[LawLevel] = None
    tags: Optional[str] = None
    notes: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    user: User = Relationship(back_populates="references")
    areas: List[LifeArea] = Relationship(link_model=ReferenceAreaLink)


# ==================== HEALTH SYSTEM ====================

class HealthCatalogItem(SQLModel, table=True):
    """Polymorphic health catalog (doctors, food, supplements, meds, motion)"""
    __tablename__ = "health_catalog_items"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True)
    catalog_type: HealthCatalogType = Field(index=True)
    name: str = Field(max_length=200)
    description: Optional[str] = None

    # Type-specific fields (optional)
    doctor_specialty: Optional[str] = Field(default=None, max_length=100)
    doctor_phone: Optional[str] = Field(default=None, max_length=20)

    food_category: Optional[str] = Field(default=None, max_length=50)

    supplement_dosage: Optional[str] = Field(default=None, max_length=50)

    medication_dosage: Optional[str] = Field(default=None, max_length=50)
    medication_frequency: Optional[str] = Field(default=None, max_length=100)

    motion_duration: Optional[str] = Field(default=None, max_length=50)

    frequency_description: Optional[str] = Field(default=None, max_length=100)
    notes: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    user: User = Relationship(back_populates="health_items")


# ==================== FINANCE SYSTEM ====================

class FinancialAccount(SQLModel, table=True):
    """Financial accounts (banking, assets, liabilities)"""
    __tablename__ = "financial_accounts"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True)
    account_type: FinancialAccountType = Field(index=True)
    name: str = Field(max_length=200)
    institution: Optional[str] = Field(default=None, max_length=100)
    account_number_last4: Optional[str] = Field(default=None, max_length=4)
    current_balance: Optional[float] = None
    interest_rate: Optional[float] = None
    due_date: Optional[date] = None
    notes: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    user: User = Relationship(back_populates="financial_accounts")


# ==================== ENTRY SYSTEM ====================

class Entry(SQLModel, table=True):
    """Journal entries per life area"""
    __tablename__ = "entries"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True)
    area_id: int = Field(foreign_key="life_areas.id", index=True)
    title: Optional[str] = Field(default=None, max_length=200)
    content: str
    entry_date: date = Field(default_factory=date.today, index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    user: User = Relationship(back_populates="entries")
    area: LifeArea = Relationship()


# ==================== ONE-ON-ONE SPECIFIC ====================

class ConflictTopic(SQLModel, table=True):
    """Conflict topics for One-on-One relationship (max 3)"""
    __tablename__ = "conflict_topics"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True)
    topic: str = Field(max_length=200)
    description: Optional[str] = None
    resolution_strategy: Optional[str] = None
    progress_notes: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    user: User = Relationship(back_populates="conflict_topics")
