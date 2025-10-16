# Prompts for Continuing Implementation

This file contains ready-to-use prompts for AI assistants (Claude, ChatGPT, etc.) to help you complete the implementation.

---

## 🎯 General Implementation Prompt

```
I have a life management application project with complete documentation. The project has:

- Complete PRD in docs/PRD.md
- Full data model specifications in docs/Data-Model.md
- Complete API schema in docs/API-Schema.md
- Architecture documentation in docs/Architecture.md
- Seed data in seed/fixtures.json

I need to implement the FastAPI backend. The tech stack is:
- FastAPI with SQLModel
- SQLite database
- Bcrypt authentication
- Alembic migrations

Please help me implement [SPECIFIC COMPONENT] following the specifications in the documentation.
```

---

## 📦 Specific Component Prompts

### 1. Database Setup

```
Using the data model specifications in docs/Data-Model.md, please create:

1. server/app/db.py - Database engine and session management with SQLite
2. server/app/models.py - All SQLModel table models including:
   - User, LifeArea, Goal, GoalAreaLink
   - Habit, HabitAreaLink, HabitCheckin
   - Task, Contact, ContactAreaLink
   - Reference, ReferenceAreaLink, Entry
   - HealthCatalogItem, FinancialAccount, ConflictTopic

Include proper type hints, relationships, and the enums defined in the spec.
```

### 2. Pydantic Schemas

```
Using docs/API-Schema.md and docs/Data-Model.md, create server/app/schemas.py with:

1. Request schemas (Create, Update) for all models
2. Response schemas with nested relationships
3. Auth schemas (LoginRequest, RegisterRequest, UserResponse)
4. Special response schemas (BirthdayResponse with age calculation, etc.)

Follow the exact request/response formats specified in API-Schema.md.
```

### 3. Authentication System

```
Create server/app/auth.py implementing:

1. Password hashing with bcrypt (cost factor 12)
2. User registration function
3. Login verification function
4. get_current_user dependency for FastAPI
5. Session management helpers

Follow the security requirements in docs/Security-Privacy.md.
```

### 4. AI Stub Module

```
Create server/app/ai_stub.py with:

1. Static Bible verses for all 8 life areas (use content from docs/Prompts.md)
2. Static insights for all 8 life areas
3. generate_bible_verse(area: str) -> dict function
4. generate_insight(area: str) -> str function

These should return deterministic placeholders ready to be swapped with real AI later.
```

### 5. Main Application

```
Create server/app/main.py with:

1. FastAPI app initialization
2. CORS middleware configuration (allow localhost:3000 for future frontend)
3. Session middleware with secret from environment
4. Include all routers (when created)
5. Startup event to create tables
6. Root endpoint that returns API info

Use the architecture from docs/Architecture.md.
```

### 6. Goals Router

```
Using docs/API-Schema.md, implement server/app/routers/goals.py with:

- GET /goals - List with filters (area_id, timeframe, status)
- POST /goals - Create with area linking
- GET /goals/{id} - Retrieve single goal
- PUT /goals/{id} - Update including progress
- DELETE /goals/{id} - Delete

Include:
- Authentication requirement (get_current_user dependency)
- User data isolation (filter by user_id)
- Proper error handling (404 if not found, 401 if unauthorized)
- Many-to-many area linking via GoalAreaLink

Return responses matching the schemas in API-Schema.md exactly.
```

### 7. Habits Router

```
Implement server/app/routers/habits.py with CRUD plus special check-in endpoint:

- GET /habits - List with filters
- POST /habits - Create
- GET /habits/{id} - Retrieve
- PUT /habits/{id} - Update
- DELETE /habits/{id} - Delete
- POST /habits/{id}/checkin - Special endpoint that:
  * Accepts optional checkin_date (defaults to today)
  * Creates HabitCheckin record
  * Updates current_streak (increment if consecutive, reset if gap)
  * Updates longest_streak if current > longest
  * Prevents duplicate check-ins for same date
  * Returns updated habit with new streak

Use the streak calculation logic described in docs/Data-Model.md.
```

### 8. Contacts Router + Birthday Calculation

```
Implement server/app/routers/contacts.py including the special birthday endpoint:

Standard CRUD plus:
- GET /contacts/birthdays?days_ahead=30
  * Calculate exact age in years, months, days
  * Calculate days until next birthday
  * Filter to only contacts with birthdays in next X days
  * Sort by days_until_birthday

Use the age calculation helper from docs/Data-Model.md:
- Account for year, month, and day differences
- Handle edge cases (leap years, month-end dates)
```

### 9. All Other Routers

```
Implement the following routers following the same pattern as goals/habits:

1. server/app/routers/areas.py - Simple GET /areas returning 8 predefined areas
2. server/app/routers/tasks.py - CRUD with status transitions
3. server/app/routers/references.py - CRUD with type filtering
4. server/app/routers/health.py - CRUD with catalog_type filtering
5. server/app/routers/finance.py - CRUD with account_type filtering
6. server/app/routers/entries.py - CRUD with date range filtering
7. server/app/routers/one_on_one.py - CRUD with max 3 topics enforcement
8. server/app/routers/ai.py - GET endpoints returning stub content

Use docs/API-Schema.md for exact endpoint specifications.
```

### 10. Alembic Migrations

```
Set up Alembic migrations:

1. Initialize Alembic in server/ directory
2. Configure alembic.ini to use DATABASE_URL from .env
3. Configure migrations/env.py to:
   - Import all SQLModel models
   - Set target_metadata = SQLModel.metadata
4. Create initial migration: alembic revision --autogenerate -m "Initial schema"
5. Review the generated migration file
6. Test with: alembic upgrade head

Also create server/seed_db.py script that:
- Loads seed/fixtures.json
- Creates the 8 life areas
- Optionally creates test user and sample data
```

### 11. Pytest Test Suite

```
Create test infrastructure:

1. server/tests/conftest.py with fixtures:
   - test_db (in-memory SQLite)
   - test_client (FastAPI TestClient)
   - test_user (authenticated user)

2. server/tests/test_auth.py:
   - Test user registration
   - Test login success/failure
   - Test logout
   - Test authentication required on protected endpoints

3. server/tests/test_habits.py:
   - Test habit check-in increments streak correctly
   - Test duplicate check-in prevention
   - Test streak reset after gap

4. server/tests/test_contacts.py:
   - Test birthday age calculation accuracy
   - Test upcoming birthdays filtering

Use the test scenarios from docs/Acceptance-Tests.md.
```

### 12. Infrastructure Files

```
Create deployment infrastructure:

1. Dockerfile:
   - FROM python:3.11-slim
   - Install dependencies from requirements.txt
   - Copy server code
   - Run migrations on startup
   - CMD uvicorn app.main:app --host 0.0.0.0 --port 8000

2. Makefile with targets:
   - setup: Create venv, install deps, copy .env
   - migrate: Run alembic upgrade head
   - seed: Run seed script
   - run: Start uvicorn with --reload
   - test: Run pytest
   - clean: Remove __pycache__, .pyc files
   - docker-build: Build Docker image
   - docker-run: Run Docker container

Follow the examples in docs/Implementation-Plan.md Day 9.
```

---

## 🔄 Incremental Implementation Workflow

### Option A: Component by Component

```
Let's implement this step by step:

STEP 1: Set up the database foundation
- Create db.py with SQLite engine
- Create all models in models.py
- Test that tables can be created

STEP 2: Add schemas
- Create all Pydantic schemas in schemas.py

STEP 3: Add authentication
- Create auth.py
- Test password hashing and verification

STEP 4: Create main app
- Create main.py with basic setup
- Add one simple router to test

STEP 5: Build routers incrementally
- Start with areas.py (simplest)
- Then goals.py
- Then habits.py (most complex due to streaks)
- Continue with remaining routers

STEP 6: Add migrations and seeding
- Set up Alembic
- Create seed script

STEP 7: Add tests
- Start with auth tests
- Add router tests

STEP 8: Infrastructure
- Dockerfile
- Makefile

Let's start with STEP 1. Ready?
```

### Option B: Vertical Slice Approach

```
Let's implement one complete feature end-to-end, then iterate:

SLICE 1: User Authentication
- Models: User
- Schemas: UserCreate, UserResponse, LoginRequest
- Router: auth.py with register/login/logout
- Tests: test_auth.py
- Goal: Can register and login

SLICE 2: Goals Feature
- Models: Goal, GoalAreaLink, LifeArea
- Schemas: GoalCreate, GoalUpdate, GoalResponse
- Router: goals.py with full CRUD
- Tests: test_goals.py
- Goal: Can manage goals with authentication

SLICE 3: Habits with Streaks
- Models: Habit, HabitAreaLink, HabitCheckin
- Schemas: HabitCreate, HabitCheckin
- Router: habits.py with check-in logic
- Tests: test_habits.py (streak calculation)
- Goal: Can track habits and build streaks

[Continue with remaining features...]

Which slice should we start with?
```

---

## 🐛 Debugging Prompts

### Database Issues

```
I'm getting a database error: [ERROR MESSAGE]

My setup:
- Using SQLite
- Models defined in server/app/models.py
- Connection string: sqlite:///./data/app.sqlite3

The data model specification is in docs/Data-Model.md.

What could be wrong and how do I fix it?
```

### Authentication Issues

```
Authentication isn't working. The issue is: [DESCRIBE ISSUE]

My implementation:
- Using bcrypt for password hashing
- Session cookies with Starlette SessionMiddleware
- get_current_user dependency

Security requirements are in docs/Security-Privacy.md.

How should I fix this?
```

### Streak Calculation Issues

```
Habit streak calculation isn't working correctly.

Current behavior: [DESCRIBE CURRENT BEHAVIOR]
Expected behavior: [DESCRIBE EXPECTED]

The streak logic is described in docs/Data-Model.md section 4.1 and docs/Acceptance-Tests.md scenario 3.3-3.4.

Help me debug this.
```

---

## 🎓 Learning Prompts

### Understanding the Architecture

```
I want to understand the architecture of this life management application.

Please explain:
1. How does the data flow from API request to database and back?
2. How are the 8 life areas connected to goals, habits, tasks, etc.?
3. How does authentication work with session cookies?
4. What's the relationship between SQLModel models and Pydantic schemas?

Use docs/Architecture.md and docs/Data-Model.md as reference.
```

### Understanding a Specific Feature

```
I want to deeply understand how [FEATURE] works in this application.

Please explain:
1. What models are involved?
2. What endpoints expose this feature?
3. What are the key business logic rules?
4. How does it relate to life areas?
5. Are there any special considerations?

Use the relevant documentation files as reference.
```

---

## ✅ Validation Prompts

### Code Review Request

```
I've implemented [COMPONENT]. Please review it against the specifications.

My implementation: [PASTE CODE OR FILE]

Specification: See docs/[RELEVANT_DOC].md

Check for:
1. Does it match the API specification exactly?
2. Are all required fields handled?
3. Is authentication enforced?
4. Is user data isolation correct?
5. Are errors handled appropriately?
6. Any security issues?
```

### Test Coverage Check

```
I've written tests for [FEATURE]. Are there any test cases I'm missing?

My tests: [PASTE TEST CODE]

Test scenarios are documented in docs/Acceptance-Tests.md.

What additional tests should I add to ensure full coverage?
```

---

## 🚀 Next Steps After MVP

```
The MVP is complete! All acceptance tests pass. What should I work on next?

Current status:
- All 8 life areas implemented
- Goals, habits, tasks, contacts all working
- Authentication functional
- Tests passing

I want to add [FEATURE]. Based on the architecture in docs/Architecture.md and the roadmap in README.md, how should I approach this?

Options:
A) Build the frontend (React/Vue/Svelte)
B) Integrate real AI (OpenAI/Anthropic)
C) Add email notifications
D) Add data export functionality
E) Migrate to PostgreSQL for multi-user

Which would you recommend and why? How would I start?
```

---

## 📝 Documentation Update Prompts

```
I've implemented [FEATURE] with some changes from the original spec. Please help me update the documentation.

Changes made:
1. [DESCRIBE CHANGE]
2. [DESCRIBE CHANGE]

Which documentation files need updating and what should be changed?

Current docs:
- docs/PRD.md
- docs/Architecture.md
- docs/API-Schema.md
- docs/Data-Model.md
- README.md
```

---

## 💡 Tips for Using These Prompts

1. **Be Specific:** Always mention which documentation file contains the relevant specifications
2. **Provide Context:** Include the tech stack (FastAPI, SQLModel, SQLite, bcrypt)
3. **Share Error Messages:** If debugging, include the full error message
4. **Paste Relevant Code:** When asking for code review, paste the actual code
5. **Reference Docs:** Point the AI to the specific doc files for context
6. **Iterate:** Start with simple components, test, then move to complex ones

---

## 🔗 Quick Reference Links

- Full specs: `docs/` directory
- Sample data: `seed/fixtures.json`
- Implementation schedule: `docs/Implementation-Plan.md`
- Test scenarios: `docs/Acceptance-Tests.md`
- API endpoints: `docs/API-Schema.md`
- Database schema: `docs/Data-Model.md`

---

**Last Updated:** 2025-10-16
**Status:** Ready for implementation - All specifications complete
