# Implementation Plan
## AI-Assisted Life Management Application MVP

**Version:** 1.0
**Date:** 2025-10-16
**Estimated Timeline:** 2-3 weeks

---

## Phase 1: Foundation (Days 1-3)

### Day 1: Project Setup & Database

**Tasks:**
1. Initialize project structure
   - Create directory tree
   - Set up Python virtual environment
   - Create `requirements.txt` with dependencies

2. Database setup
   - Install SQLite (comes with Python)
   - Create `/data/app.sqlite3` location
   - Set up SQLModel models in `models.py`
   - Configure database connection in `db.py`

3. Alembic migrations
   - Initialize Alembic: `alembic init migrations`
   - Configure `alembic.ini` for SQLite
   - Create initial migration
   - Test migration: `alembic upgrade head`

4. Seed life areas
   - Create seed script for 8 life areas
   - Run seed script

**Deliverables:**
- ✅ Working database with all tables
- ✅ 8 life areas populated
- ✅ Alembic migrations functional

**Validation:**
```bash
sqlite3 data/app.sqlite3 ".tables"  # Should show all tables
sqlite3 data/app.sqlite3 "SELECT * FROM life_areas;"  # Should show 8 areas
```

---

### Day 2: Authentication & Core App

**Tasks:**
1. Implement authentication
   - Create `auth.py` with bcrypt password hashing
   - Implement session middleware (Starlette)
   - Create user registration logic
   - Create login/logout logic
   - Add `get_current_user` dependency

2. FastAPI app setup
   - Create `main.py` with FastAPI app
   - Configure CORS (for future frontend)
   - Add session middleware
   - Create `/auth` router
   - Test with Swagger UI

3. Pydantic schemas
   - Create request/response schemas in `schemas.py`
   - User schemas (UserCreate, UserResponse)
   - Auth schemas (LoginRequest, etc.)

**Deliverables:**
- ✅ User registration works
- ✅ Login/logout works
- ✅ Session cookies set correctly
- ✅ Protected endpoints require authentication

**Validation:**
```bash
# Start server
uvicorn app.main:app --reload

# Test registration (use curl or Swagger UI)
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"test","password":"test1234"}'

# Test login
curl -X POST http://localhost:8000/api/auth/login \
  -d '{"username":"test","password":"test1234"}'
```

---

### Day 3: Core Models & Schemas

**Tasks:**
1. Complete SQLModel models
   - Goal, GoalAreaLink
   - Habit, HabitAreaLink, HabitCheckin
   - Task
   - Contact, ContactAreaLink
   - Reference, ReferenceAreaLink
   - Entry
   - HealthCatalogItem
   - FinancialAccount
   - ConflictTopic

2. Create Pydantic schemas for all models
   - Create (input schemas)
   - Update (partial input schemas)
   - Response (output schemas)
   - List responses with nested area info

3. Run migration for new models
   ```bash
   alembic revision --autogenerate -m "Add all core models"
   alembic upgrade head
   ```

**Deliverables:**
- ✅ All models defined
- ✅ All schemas defined
- ✅ Database tables created

**Validation:**
```bash
sqlite3 data/app.sqlite3 ".schema goals"
sqlite3 data/app.sqlite3 ".schema habits"
# Etc. for all tables
```

---

## Phase 2: Core Endpoints (Days 4-8)

### Day 4: Goals & Habits Routers

**Tasks:**
1. Create `/api/goals` router
   - GET /goals (list with filters)
   - POST /goals (create)
   - GET /goals/{id} (retrieve)
   - PUT /goals/{id} (update)
   - DELETE /goals/{id}

2. Create `/api/habits` router
   - GET /habits (list with filters)
   - POST /habits (create)
   - GET /habits/{id}
   - PUT /habits/{id}
   - DELETE /habits/{id}
   - POST /habits/{id}/checkin (special endpoint)

3. Implement many-to-many area links
   - Helper functions to link/unlink areas
   - Include area details in responses

**Deliverables:**
- ✅ Goals CRUD fully functional
- ✅ Habits CRUD fully functional
- ✅ Habit check-in increments streaks correctly

**Validation:**
- Create goal via Swagger UI
- Update progress percentage
- Create habit and check in multiple days
- Verify streak calculation

---

### Day 5: Tasks & Contacts Routers

**Tasks:**
1. Create `/api/tasks` router
   - Standard CRUD operations
   - Status transition logic
   - Set completed_at when status → "done"
   - Filter by area, status, priority

2. Create `/api/contacts` router
   - Standard CRUD operations
   - GET /contacts/birthdays (special endpoint)
   - Implement age calculation helper
   - Filter by area

**Deliverables:**
- ✅ Tasks CRUD functional
- ✅ Contacts CRUD functional
- ✅ Birthday age calculation works (Y, M, D)
- ✅ Upcoming birthdays endpoint works

**Validation:**
- Create contact with birthday
- Query /contacts/birthdays
- Verify age calculation is accurate

---

### Day 6: References, Health, Finance Routers

**Tasks:**
1. Create `/api/references` router
   - CRUD operations
   - Filter by type, law_level, area

2. Create `/api/health` router
   - CRUD for health catalog items
   - Filter by catalog_type

3. Create `/api/finance` router
   - CRUD for financial accounts
   - Filter by account_type

**Deliverables:**
- ✅ All three routers functional
- ✅ Filtering works correctly
- ✅ Type-specific fields handled properly

**Validation:**
- Create doctor, supplement, medication
- Create banking account, asset, liability
- Create website reference, law reference

---

### Day 7: Entries, One-on-One, AI Stubs

**Tasks:**
1. Create `/api/entries` router
   - CRUD operations
   - Filter by area, date range

2. Create `/api/one-on-one/conflicts` router
   - CRUD operations
   - Enforce max 3 topics limit

3. Create AI stub module
   - `ai_stub.py` with static responses
   - Implement `generate_bible_verse(area)`
   - Implement `generate_insight(area)`

4. Create `/api/ai` router
   - GET /ai/verse?area=X
   - GET /ai/insight?area=X

**Deliverables:**
- ✅ Entries CRUD works
- ✅ Conflict topics work with max 3 limit
- ✅ AI endpoints return placeholder content

**Validation:**
- Create journal entries
- Create 3 conflict topics
- Try to create 4th (should fail)
- Query AI endpoints for all 8 areas

---

### Day 8: Testing & Bug Fixes

**Tasks:**
1. Write pytest tests
   - Test authentication flow
   - Test goal creation and updates
   - Test habit check-in and streaks
   - Test birthday age calculation
   - Test max 3 conflicts enforcement
   - Test user data isolation

2. Run tests and fix bugs
   ```bash
   pytest -v
   ```

3. Manual testing via Swagger UI
   - Test all endpoints
   - Verify error handling
   - Check response formats

**Deliverables:**
- ✅ Pytest suite passes
- ✅ All critical bugs fixed
- ✅ Error handling works

---

## Phase 3: Infrastructure & Documentation (Days 9-10)

### Day 9: DevOps Setup

**Tasks:**
1. Create Dockerfile
   - Use python:3.11-slim
   - Install dependencies
   - Run migrations on startup
   - Expose port 8000

2. Create Makefile
   - `make setup` - Install dependencies, run migrations
   - `make run` - Start uvicorn
   - `make test` - Run pytest
   - `make seed` - Seed database
   - `make clean` - Clean up __pycache__, etc.

3. Create .env.example
   - APP_SECRET placeholder
   - DATABASE_URL
   - ENVIRONMENT

4. Test Docker build
   ```bash
   docker build -t life-mgmt-app .
   docker run -p 8000:8000 life-mgmt-app
   ```

**Deliverables:**
- ✅ Dockerfile builds successfully
- ✅ Makefile commands work
- ✅ .env.example provided

---

### Day 10: Seed Data & README

**Tasks:**
1. Create comprehensive seed data
   - `/seed/sample.csv` with normalized data
   - `/seed/fixtures.json` with structured test data
   - Python seed script that populates database

2. Write README.md
   - Project overview
   - Prerequisites (Python 3.11+, etc.)
   - Installation instructions
   - Running locally
   - Running with Docker
   - Seed database instructions
   - Running tests
   - API documentation (link to /docs)
   - Troubleshooting
   - License

3. Final documentation review
   - Ensure all 9 docs are complete
   - Cross-reference links work
   - Spelling/grammar check

**Deliverables:**
- ✅ Seed data loads successfully
- ✅ README is comprehensive and clear
- ✅ All documentation complete

---

## Phase 4: Final Polish (Days 11-14)

### Day 11-12: Integration Testing

**Tasks:**
1. End-to-end testing
   - Register new user
   - Create data in all 8 life areas
   - Test filtering and querying
   - Test streak calculations
   - Test birthday age calculation

2. Performance testing
   - Measure API response times
   - Check database query performance
   - Add indexes if needed
   - Optimize N+1 queries

3. Security review
   - Verify bcrypt hashing
   - Check session cookie settings
   - Test authentication bypass attempts
   - Validate input sanitization

**Deliverables:**
- ✅ All acceptance tests pass
- ✅ Performance meets requirements (<500ms)
- ✅ No security vulnerabilities

---

### Day 13: Documentation Finalization

**Tasks:**
1. Update all docs with any changes
2. Create API examples/tutorials
3. Record demo video (optional)
4. Create Postman/Insomnia collection (optional)

**Deliverables:**
- ✅ Documentation 100% accurate
- ✅ Examples/tutorials available

---

### Day 14: Release Preparation

**Tasks:**
1. Final code cleanup
   - Remove debug print statements
   - Format code with Black (optional)
   - Run linter (flake8, mypy)

2. Create git repository (if not already)
   - .gitignore (exclude .env, __pycache__, *.pyc, data/*.sqlite3)
   - Initial commit

3. Tag MVP release
   ```bash
   git tag v1.0-mvp
   ```

4. Prepare handoff
   - Zip entire project
   - Include README with setup steps
   - Document known limitations
   - Outline Phase 2 roadmap

**Deliverables:**
- ✅ Clean, production-ready codebase
- ✅ Git repository with tags
- ✅ Handoff documentation

---

## Development Workflow

### Daily Routine
1. **Morning:**
   - Review previous day's work
   - Plan today's tasks
   - Check TODOs in code

2. **Development:**
   - Write code in small increments
   - Test frequently (manual + automated)
   - Commit working code regularly

3. **End of Day:**
   - Run full test suite
   - Commit final changes
   - Update implementation tracker
   - Note blockers/questions

### Git Workflow
```bash
# Feature branches (optional for solo dev)
git checkout -b feature/goals-router
# ... make changes ...
git add .
git commit -m "Implement goals CRUD endpoints"
git checkout main
git merge feature/goals-router

# Or simple commits on main for MVP
git add .
git commit -m "Add habit check-in streak logic"
```

---

## Dependency Installation

### requirements.txt
```
fastapi==0.104.1
uvicorn[standard]==0.24.0
sqlmodel==0.0.14
alembic==1.12.1
python-dotenv==1.0.0
bcrypt==4.1.1
itsdangerous==2.1.2
pydantic==2.5.0
pytest==7.4.3
httpx==0.25.2
```

### Install
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r server/requirements.txt
```

---

## Testing Strategy

### Unit Tests
- Models (validation, constraints)
- Utility functions (age calculation, streak logic)
- AI stub functions

### Integration Tests
- API endpoints (status codes, response format)
- Database operations (CRUD, relationships)
- Authentication (register, login, logout)

### Manual Tests
- Swagger UI (/docs)
- Create realistic user scenarios
- Test edge cases

---

## Deployment Checklist

Before deploying (even locally for demo):

- [ ] All migrations run successfully
- [ ] Seed data loads without errors
- [ ] All pytest tests pass
- [ ] Environment variables set (APP_SECRET)
- [ ] Swagger docs accessible at /docs
- [ ] No debug/print statements in code
- [ ] Error handling works (try invalid inputs)
- [ ] README instructions are accurate
- [ ] .gitignore excludes sensitive files

---

## Known Limitations & Future Work

### MVP Limitations:
- No frontend UI (API only)
- AI content is static placeholders
- No email notifications
- No file uploads
- No search functionality
- No data export
- Single-user per instance
- SQLite (not suitable for high concurrency)

### Phase 2 Roadmap:
1. **Frontend Development** (2-3 weeks)
   - Choose framework (React, Vue, or Svelte)
   - Implement all wireframes
   - Connect to API

2. **Real AI Integration** (1 week)
   - Choose provider (OpenAI, Anthropic, local LLM)
   - Implement caching
   - Add cost controls

3. **Advanced Features** (ongoing)
   - Email reminders
   - Calendar integration
   - Data export/import
   - Search functionality
   - Analytics/insights dashboard

4. **Multi-User Support** (2-3 weeks)
   - Migrate to PostgreSQL
   - Implement proper multi-tenancy
   - Add team/family sharing features

---

## Troubleshooting

### Common Issues:

**Issue:** Alembic can't find database
**Solution:** Check `DATABASE_URL` in .env and alembic.ini match

**Issue:** Session cookies not persisting
**Solution:** Verify `APP_SECRET` is set in .env, check cookie settings

**Issue:** Foreign key constraint errors
**Solution:** Ensure life_areas are seeded before creating goals/habits

**Issue:** Streak calculation wrong
**Solution:** Check date comparison logic, timezone handling

**Issue:** Tests failing
**Solution:** Ensure test database is clean, check fixtures

---

## Success Metrics

### MVP Complete When:
1. ✅ All 23 deliverable files created
2. ✅ Database fully functional with migrations
3. ✅ All API endpoints work as specified
4. ✅ Pytest suite has >80% coverage and passes
5. ✅ Seed data loads successfully
6. ✅ README allows new developer to set up in <30 min
7. ✅ Docker build succeeds
8. ✅ All acceptance tests pass
9. ✅ Swagger docs are complete and accurate
10. ✅ No critical bugs

---

## Related Documents
- [PRD.md](PRD.md) - Product requirements
- [Architecture.md](Architecture.md) - System design
- [Data-Model.md](Data-Model.md) - Database schema
- [API-Schema.md](API-Schema.md) - Endpoint specifications
- [Acceptance-Tests.md](Acceptance-Tests.md) - Test scenarios
