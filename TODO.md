# Implementation TODO List

## Project Status: Documentation Complete ✅ | Implementation In Progress 🚧

---

## Phase 1: Foundation ✅ COMPLETE

- [x] Create project structure
- [x] Write comprehensive documentation (9 files)
- [x] Prepare seed data (CSV + JSON)
- [x] Set up .gitignore
- [x] Create .env.example
- [x] Write README.md
- [x] Define requirements.txt

---

## Phase 2: Backend Core 🚧 IN PROGRESS

### Database & Models
- [ ] Create `server/app/__init__.py`
- [ ] Create `server/app/db.py` - Database connection and session management
  - SQLite engine setup
  - Session dependency injection
  - Create tables helper
- [ ] Create `server/app/models.py` - SQLModel database models
  - User model
  - LifeArea model + enum
  - Goal model + GoalAreaLink
  - Habit model + HabitAreaLink + HabitCheckin
  - Task model
  - Contact model + ContactAreaLink
  - Reference model + ReferenceAreaLink
  - Entry model
  - HealthCatalogItem model
  - FinancialAccount model
  - ConflictTopic model
  - AIContentCache model (optional)
- [ ] Create `server/app/schemas.py` - Pydantic request/response schemas
  - User schemas (Create, Response)
  - Auth schemas (Login, Register)
  - Goal schemas (Create, Update, Response, List)
  - Habit schemas (Create, Update, Response, Checkin)
  - Task schemas (Create, Update, Response)
  - Contact schemas (Create, Update, Response, Birthday)
  - Reference schemas (Create, Update, Response)
  - Health schemas (Create, Update, Response)
  - Finance schemas (Create, Update, Response)
  - Entry schemas (Create, Update, Response)
  - Conflict schemas (Create, Update, Response)

**Reference:** See [docs/Data-Model.md](docs/Data-Model.md) for complete model definitions

### Authentication
- [ ] Create `server/app/auth.py` - Authentication logic
  - Password hashing functions (bcrypt)
  - User creation
  - Login verification
  - get_current_user dependency
  - Session management

**Reference:** See [docs/Security-Privacy.md](docs/Security-Privacy.md) for security requirements

### AI Stubs
- [ ] Create `server/app/ai_stub.py` - AI placeholder functions
  - Static Bible verses for each life area
  - Static insights for each life area
  - generate_bible_verse(area) function
  - generate_insight(area) function

**Reference:** See [docs/Prompts.md](docs/Prompts.md) for content templates

### Main Application
- [ ] Create `server/app/main.py` - FastAPI app entry point
  - Initialize FastAPI app
  - Add CORS middleware
  - Add session middleware
  - Include all routers
  - Startup/shutdown events
  - Root endpoint

---

## Phase 3: API Routers 🚧 NEXT

### Router Files (Create in `server/app/routers/`)
- [ ] `__init__.py` - Empty init file
- [ ] `auth.py` - Authentication endpoints
  - POST /auth/register
  - POST /auth/login
  - POST /auth/logout
  - GET /auth/me
- [ ] `areas.py` - Life areas endpoints
  - GET /areas - List all 8 areas
- [ ] `goals.py` - Goals CRUD
  - GET /goals (with filters)
  - POST /goals
  - GET /goals/{id}
  - PUT /goals/{id}
  - DELETE /goals/{id}
- [ ] `habits.py` - Habits CRUD + check-in
  - GET /habits (with filters)
  - POST /habits
  - GET /habits/{id}
  - PUT /habits/{id}
  - DELETE /habits/{id}
  - POST /habits/{id}/checkin - Special endpoint for streak tracking
- [ ] `tasks.py` - Tasks CRUD
  - GET /tasks (with filters)
  - POST /tasks
  - GET /tasks/{id}
  - PUT /tasks/{id}
  - DELETE /tasks/{id}
- [ ] `contacts.py` - Contacts CRUD + birthdays
  - GET /contacts (with filters)
  - POST /contacts
  - GET /contacts/{id}
  - PUT /contacts/{id}
  - DELETE /contacts/{id}
  - GET /contacts/birthdays - Special endpoint with age calculation
- [ ] `references.py` - References CRUD
  - GET /references (with filters)
  - POST /references
  - GET /references/{id}
  - PUT /references/{id}
  - DELETE /references/{id}
- [ ] `health.py` - Health catalog CRUD
  - GET /health (filter by catalog_type)
  - POST /health
  - GET /health/{id}
  - PUT /health/{id}
  - DELETE /health/{id}
- [ ] `finance.py` - Financial accounts CRUD
  - GET /finance (filter by account_type)
  - POST /finance
  - GET /finance/{id}
  - PUT /finance/{id}
  - DELETE /finance/{id}
- [ ] `entries.py` - Journal entries CRUD
  - GET /entries (with filters)
  - POST /entries
  - GET /entries/{id}
  - PUT /entries/{id}
  - DELETE /entries/{id}
- [ ] `one_on_one.py` - Conflict topics CRUD
  - GET /one-on-one/conflicts
  - POST /one-on-one/conflicts (enforce max 3)
  - GET /one-on-one/conflicts/{id}
  - PUT /one-on-one/conflicts/{id}
  - DELETE /one-on-one/conflicts/{id}
- [ ] `ai.py` - AI content endpoints
  - GET /ai/verse?area=X
  - GET /ai/insight?area=X

**Reference:** See [docs/API-Schema.md](docs/API-Schema.md) for complete endpoint specifications

---

## Phase 4: Database Migrations 🚧 PENDING

- [ ] Initialize Alembic
  ```bash
  cd server
  alembic init migrations
  ```
- [ ] Configure `alembic.ini`
  - Set sqlalchemy.url to match .env
- [ ] Configure `migrations/env.py`
  - Import SQLModel models
  - Set target_metadata
- [ ] Create initial migration
  ```bash
  alembic revision --autogenerate -m "Initial schema"
  ```
- [ ] Review migration file in `migrations/versions/`
- [ ] Test migration
  ```bash
  alembic upgrade head
  ```
- [ ] Create seed script `server/seed_db.py`
  - Load life areas from fixtures.json
  - Optionally load sample user and data

**Reference:** See [docs/Implementation-Plan.md](docs/Implementation-Plan.md) Day 1 tasks

---

## Phase 5: Testing 🚧 PENDING

### Test Setup
- [ ] Create `server/tests/__init__.py`
- [ ] Create `server/tests/conftest.py` - Pytest fixtures
  - test_db fixture (in-memory SQLite)
  - test_client fixture (FastAPI TestClient)
  - test_user fixture
  - test_session fixture

### Test Files
- [ ] Create `server/tests/test_auth.py`
  - Test registration
  - Test login/logout
  - Test authentication required
- [ ] Create `server/tests/test_goals.py`
  - Test CRUD operations
  - Test progress updates
  - Test filtering
- [ ] Create `server/tests/test_habits.py`
  - Test CRUD operations
  - Test check-in streak logic
  - Test duplicate check-in prevention
- [ ] Create `server/tests/test_tasks.py`
  - Test CRUD operations
  - Test status transitions
- [ ] Create `server/tests/test_contacts.py`
  - Test CRUD operations
  - Test birthday age calculation
  - Test upcoming birthdays
- [ ] Create `server/tests/test_core.py` - Core functionality tests
  - User data isolation
  - Authorization checks
  - Error handling

**Reference:** See [docs/Acceptance-Tests.md](docs/Acceptance-Tests.md) for test scenarios

---

## Phase 6: Infrastructure 🚧 PENDING

- [ ] Create `Dockerfile`
  ```dockerfile
  FROM python:3.11-slim
  WORKDIR /app
  COPY server/requirements.txt .
  RUN pip install --no-cache-dir -r requirements.txt
  COPY server/ .
  COPY data/ /app/data/
  CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
  ```
- [ ] Create `Makefile` with common commands:
  - `make setup` - Install deps, create .env
  - `make migrate` - Run Alembic migrations
  - `make seed` - Seed database
  - `make run` - Start uvicorn
  - `make test` - Run pytest
  - `make clean` - Clean __pycache__, etc.
- [ ] Create `docker-compose.yml` (optional)
- [ ] Test Docker build and run

**Reference:** See [docs/Implementation-Plan.md](docs/Implementation-Plan.md) Day 9 tasks

---

## Phase 7: Final Polish 🚧 PENDING

- [ ] Run full test suite and fix bugs
- [ ] Manual testing via Swagger UI
- [ ] Performance testing (response times <500ms)
- [ ] Security review checklist
- [ ] Code cleanup and formatting
- [ ] Update README with actual setup instructions
- [ ] Create demo video or screenshots (optional)
- [ ] Tag v1.0-mvp release

---

## Quick Start Guide for Implementation

### Step 1: Set up environment (5 minutes)
```bash
cd "Project for Joe"
python3 -m venv venv
source venv/bin/activate
pip install -r server/requirements.txt
cp server/.env.example server/.env
# Edit .env and add a strong APP_SECRET
```

### Step 2: Create database models (1-2 hours)
- Open [docs/Data-Model.md](docs/Data-Model.md)
- Create `server/app/db.py` with SQLite engine setup
- Create `server/app/models.py` by copying model definitions from docs
- Create `server/app/schemas.py` with Pydantic schemas

### Step 3: Set up authentication (1 hour)
- Create `server/app/auth.py` using bcrypt
- Reference [docs/Security-Privacy.md](docs/Security-Privacy.md)

### Step 4: Create main app (30 minutes)
- Create `server/app/main.py`
- Set up FastAPI app
- Add middleware (CORS, sessions)

### Step 5: Build routers one at a time (4-6 hours)
- Start with simplest: `areas.py` (just returns 8 static areas)
- Then `goals.py`, `habits.py`, etc.
- Reference [docs/API-Schema.md](docs/API-Schema.md) for exact request/response formats
- Test each router in Swagger UI as you build

### Step 6: Add migrations (1 hour)
- Initialize Alembic
- Create initial migration
- Test database creation

### Step 7: Write tests (2-3 hours)
- Set up test fixtures
- Write critical path tests
- Reference [docs/Acceptance-Tests.md](docs/Acceptance-Tests.md)

### Step 8: Polish and deploy (1-2 hours)
- Fix bugs
- Add Dockerfile and Makefile
- Final testing

**Total Estimated Time:** 12-18 hours of focused development

---

## Development Tips

### Use the Documentation
Every technical decision is documented. When stuck:
1. Check [docs/API-Schema.md](docs/API-Schema.md) for endpoint specs
2. Check [docs/Data-Model.md](docs/Data-Model.md) for database structure
3. Check [docs/Implementation-Plan.md](docs/Implementation-Plan.md) for step-by-step guide

### Test as You Go
- Start uvicorn with `--reload` for auto-restart
- Use Swagger UI at http://localhost:8000/docs to test endpoints
- Run pytest frequently to catch regressions

### Copy-Paste Friendly
The documentation includes code examples you can copy:
- Model definitions in Data-Model.md
- Request/response schemas in API-Schema.md
- Security patterns in Security-Privacy.md

### AI Assistance
If using Claude/ChatGPT to help implement:
- Give it specific doc files as context
- Ask it to implement one router at a time
- Example prompt: "Using the specifications in docs/API-Schema.md and docs/Data-Model.md, implement the goals router in server/app/routers/goals.py"

---

## Files Remaining to Create (23 Target - 12 Created = 11 Remaining)

### Created ✅ (12 files)
1. docs/PRD.md
2. docs/Architecture.md
3. docs/API-Schema.md
4. docs/Data-Model.md
5. docs/UX-Wireframes.md
6. docs/Acceptance-Tests.md
7. docs/Prompts.md
8. docs/Implementation-Plan.md
9. docs/Security-Privacy.md
10. seed/sample.csv
11. seed/fixtures.json
12. server/requirements.txt
13. README.md
14. .gitignore
15. server/.env.example
16. TODO.md (this file)

### To Create 🚧 (Core implementation files)
1. server/app/__init__.py
2. server/app/main.py
3. server/app/db.py
4. server/app/models.py
5. server/app/schemas.py
6. server/app/auth.py
7. server/app/ai_stub.py
8. server/app/routers/*.py (multiple router files)
9. server/tests/conftest.py
10. server/tests/test_core.py
11. Dockerfile
12. Makefile

**Note:** Implementation files should be created by following the detailed specifications in the documentation. The specs are complete and ready to use.

---

## Questions or Issues?

1. **Check Documentation First:** All decisions are documented in `/docs`
2. **Review Implementation Plan:** [docs/Implementation-Plan.md](docs/Implementation-Plan.md) has day-by-day schedule
3. **Check TODO Sections Above:** Each phase has detailed checklist
4. **Test with Seed Data:** Use [seed/fixtures.json](seed/fixtures.json) for realistic testing

---

## Success Criteria

MVP is complete when:
- ✅ All models defined and migrations run
- ✅ All API endpoints functional (test with Swagger UI)
- ✅ Authentication works (register, login, logout)
- ✅ User data isolation enforced
- ✅ Habit streak calculation works correctly
- ✅ Birthday age calculation accurate
- ✅ Core pytest tests pass
- ✅ Can seed database with fixtures.json
- ✅ README instructions work for fresh setup
- ✅ Docker builds and runs

---

Last Updated: 2025-10-16
Project Phase: Documentation Complete, Implementation Ready to Start
