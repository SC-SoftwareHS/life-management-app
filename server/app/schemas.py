"""Pydantic schemas for request/response validation"""
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import datetime, date
from .models import (
    LifeAreaEnum, GoalTimeframe, GoalStatus, HabitType, TaskStatus, TaskPriority,
    ReferenceType, LawLevel, HealthCatalogType, FinancialAccountType
)


# ==================== AUTH SCHEMAS ====================

class UserCreate(BaseModel):
    """Schema for user registration"""
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=8)
    email: Optional[str] = None
    full_name: Optional[str] = None


class LoginRequest(BaseModel):
    """Schema for login"""
    username: str
    password: str


class UserResponse(BaseModel):
    """Schema for user data response"""
    id: int
    username: str
    email: Optional[str]
    full_name: Optional[str]
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# ==================== LIFE AREA SCHEMAS ====================

class LifeAreaResponse(BaseModel):
    """Schema for life area response"""
    id: int
    name: LifeAreaEnum
    display_name: str
    description: Optional[str]
    icon: Optional[str]

    model_config = ConfigDict(from_attributes=True)


# ==================== GOAL SCHEMAS ====================

class GoalCreate(BaseModel):
    """Schema for creating a goal"""
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    timeframe: GoalTimeframe
    due_date: Optional[date] = None
    area_ids: List[int] = Field(..., min_items=1)
    contact_id: Optional[int] = None


class GoalUpdate(BaseModel):
    """Schema for updating a goal"""
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    status: Optional[GoalStatus] = None
    progress_percentage: Optional[int] = Field(None, ge=0, le=100)
    due_date: Optional[date] = None
    area_ids: Optional[List[int]] = None
    contact_id: Optional[int] = None


class GoalResponse(BaseModel):
    """Schema for goal response"""
    id: int
    title: str
    description: Optional[str]
    timeframe: GoalTimeframe
    status: GoalStatus
    progress_percentage: int
    due_date: Optional[date]
    areas: List[LifeAreaResponse]
    contact_id: Optional[int]
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


# ==================== HABIT SCHEMAS ====================

class HabitCreate(BaseModel):
    """Schema for creating a habit"""
    name: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    habit_type: HabitType
    frequency_description: str = Field(..., min_length=1, max_length=100)
    area_ids: List[int] = Field(..., min_items=1)


class HabitUpdate(BaseModel):
    """Schema for updating a habit"""
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    frequency_description: Optional[str] = Field(None, min_length=1, max_length=100)
    area_ids: Optional[List[int]] = None


class HabitCheckinRequest(BaseModel):
    """Schema for habit check-in"""
    checkin_date: Optional[date] = None
    notes: Optional[str] = None


class HabitResponse(BaseModel):
    """Schema for habit response"""
    id: int
    name: str
    description: Optional[str]
    habit_type: HabitType
    frequency_description: str
    current_streak: int
    longest_streak: int
    last_checkin_date: Optional[date]
    areas: List[LifeAreaResponse]
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


# ==================== TASK SCHEMAS ====================

class TaskCreate(BaseModel):
    """Schema for creating a task"""
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    area_id: int
    status: TaskStatus = TaskStatus.TODO
    priority: TaskPriority = TaskPriority.MEDIUM
    due_date: Optional[date] = None
    contact_id: Optional[int] = None


class TaskUpdate(BaseModel):
    """Schema for updating a task"""
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None
    due_date: Optional[date] = None
    contact_id: Optional[int] = None


class TaskResponse(BaseModel):
    """Schema for task response"""
    id: int
    title: str
    description: Optional[str]
    status: TaskStatus
    priority: TaskPriority
    due_date: Optional[date]
    area: LifeAreaResponse
    contact_id: Optional[int]
    created_at: datetime
    updated_at: datetime
    completed_at: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)


# ==================== CONTACT SCHEMAS ====================

class ContactCreate(BaseModel):
    """Schema for creating a contact"""
    name: str = Field(..., min_length=1, max_length=100)
    role: Optional[str] = Field(None, max_length=100)
    phone: Optional[str] = Field(None, max_length=20)
    email: Optional[str] = Field(None, max_length=100)
    address: Optional[str] = None
    birthday: Optional[date] = None
    notes: Optional[str] = None
    area_ids: List[int] = Field(..., min_items=1)


class ContactUpdate(BaseModel):
    """Schema for updating a contact"""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    role: Optional[str] = Field(None, max_length=100)
    phone: Optional[str] = Field(None, max_length=20)
    email: Optional[str] = Field(None, max_length=100)
    address: Optional[str] = None
    birthday: Optional[date] = None
    notes: Optional[str] = None
    area_ids: Optional[List[int]] = None


class ContactResponse(BaseModel):
    """Schema for contact response"""
    id: int
    name: str
    role: Optional[str]
    phone: Optional[str]
    email: Optional[str]
    address: Optional[str]
    birthday: Optional[date]
    notes: Optional[str]
    areas: List[LifeAreaResponse]
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class BirthdayResponse(BaseModel):
    """Schema for birthday with age calculation"""
    contact_id: int
    name: str
    birthday: date
    age: dict  # {years, months, days}
    days_until_birthday: int


# ==================== REFERENCE SCHEMAS ====================

class ReferenceCreate(BaseModel):
    """Schema for creating a reference"""
    title: str = Field(..., min_length=1, max_length=200)
    type: ReferenceType
    url: Optional[str] = Field(None, max_length=500)
    content: Optional[str] = None
    law_level: Optional[LawLevel] = None
    tags: Optional[str] = None
    notes: Optional[str] = None
    area_ids: List[int] = Field(..., min_items=1)


class ReferenceUpdate(BaseModel):
    """Schema for updating a reference"""
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    url: Optional[str] = Field(None, max_length=500)
    content: Optional[str] = None
    law_level: Optional[LawLevel] = None
    tags: Optional[str] = None
    notes: Optional[str] = None
    area_ids: Optional[List[int]] = None


class ReferenceResponse(BaseModel):
    """Schema for reference response"""
    id: int
    title: str
    type: ReferenceType
    url: Optional[str]
    content: Optional[str]
    law_level: Optional[LawLevel]
    tags: Optional[str]
    notes: Optional[str]
    areas: List[LifeAreaResponse]
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


# ==================== HEALTH CATALOG SCHEMAS ====================

class HealthCatalogCreate(BaseModel):
    """Schema for creating a health catalog item"""
    catalog_type: HealthCatalogType
    name: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    doctor_specialty: Optional[str] = None
    doctor_phone: Optional[str] = None
    food_category: Optional[str] = None
    supplement_dosage: Optional[str] = None
    medication_dosage: Optional[str] = None
    medication_frequency: Optional[str] = None
    motion_duration: Optional[str] = None
    frequency_description: Optional[str] = None
    notes: Optional[str] = None


class HealthCatalogUpdate(BaseModel):
    """Schema for updating a health catalog item"""
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    doctor_specialty: Optional[str] = None
    doctor_phone: Optional[str] = None
    food_category: Optional[str] = None
    supplement_dosage: Optional[str] = None
    medication_dosage: Optional[str] = None
    medication_frequency: Optional[str] = None
    motion_duration: Optional[str] = None
    frequency_description: Optional[str] = None
    notes: Optional[str] = None


class HealthCatalogResponse(BaseModel):
    """Schema for health catalog response"""
    id: int
    catalog_type: HealthCatalogType
    name: str
    description: Optional[str]
    doctor_specialty: Optional[str]
    doctor_phone: Optional[str]
    food_category: Optional[str]
    supplement_dosage: Optional[str]
    medication_dosage: Optional[str]
    medication_frequency: Optional[str]
    motion_duration: Optional[str]
    frequency_description: Optional[str]
    notes: Optional[str]
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


# ==================== FINANCE SCHEMAS ====================

class FinancialAccountCreate(BaseModel):
    """Schema for creating a financial account"""
    account_type: FinancialAccountType
    name: str = Field(..., min_length=1, max_length=200)
    institution: Optional[str] = Field(None, max_length=100)
    account_number_last4: Optional[str] = Field(None, max_length=4)
    current_balance: Optional[float] = None
    interest_rate: Optional[float] = None
    due_date: Optional[date] = None
    notes: Optional[str] = None


class FinancialAccountUpdate(BaseModel):
    """Schema for updating a financial account"""
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    institution: Optional[str] = Field(None, max_length=100)
    account_number_last4: Optional[str] = Field(None, max_length=4)
    current_balance: Optional[float] = None
    interest_rate: Optional[float] = None
    due_date: Optional[date] = None
    notes: Optional[str] = None


class FinancialAccountResponse(BaseModel):
    """Schema for financial account response"""
    id: int
    account_type: FinancialAccountType
    name: str
    institution: Optional[str]
    account_number_last4: Optional[str]
    current_balance: Optional[float]
    interest_rate: Optional[float]
    due_date: Optional[date]
    notes: Optional[str]
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


# ==================== ENTRY SCHEMAS ====================

class EntryCreate(BaseModel):
    """Schema for creating a journal entry"""
    area_id: int
    title: Optional[str] = Field(None, max_length=200)
    content: str = Field(..., min_length=1)
    entry_date: Optional[date] = None


class EntryUpdate(BaseModel):
    """Schema for updating a journal entry"""
    title: Optional[str] = Field(None, max_length=200)
    content: Optional[str] = Field(None, min_length=1)
    entry_date: Optional[date] = None


class EntryResponse(BaseModel):
    """Schema for entry response"""
    id: int
    title: Optional[str]
    content: str
    area: LifeAreaResponse
    entry_date: date
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


# ==================== CONFLICT TOPIC SCHEMAS ====================

class ConflictTopicCreate(BaseModel):
    """Schema for creating a conflict topic"""
    topic: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    resolution_strategy: Optional[str] = None
    progress_notes: Optional[str] = None


class ConflictTopicUpdate(BaseModel):
    """Schema for updating a conflict topic"""
    topic: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    resolution_strategy: Optional[str] = None
    progress_notes: Optional[str] = None


class ConflictTopicResponse(BaseModel):
    """Schema for conflict topic response"""
    id: int
    topic: str
    description: Optional[str]
    resolution_strategy: Optional[str]
    progress_notes: Optional[str]
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


# ==================== AI CONTENT SCHEMAS ====================

class AIVerseResponse(BaseModel):
    """Schema for AI-generated Bible verse"""
    reference: str
    text: str
    area: str
    generated_at: datetime


class AIInsightResponse(BaseModel):
    """Schema for AI-generated insight"""
    insight: str
    area: str
    generated_at: datetime
