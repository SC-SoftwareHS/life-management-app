# Architecture Documentation
## AI-Assisted Life Management Application

**Version:** 1.0 MVP
**Date:** 2025-10-16

---

## 1. System Overview

### 1.1 Architecture Style
**Monolithic API-first application** with clear separation of concerns:
- RESTful API backend (FastAPI)
- SQLite database (file-based, in-repo)
- Modular router-based organization
- Future-ready for frontend integration

### 1.2 High-Level Architecture Diagram

```
┌─────────────────────────────────────────────────────────┐
│                    Future Frontend                       │
│              (React/Vue/Svelte - Phase 2)               │
└─────────────────────┬───────────────────────────────────┘
                      │ HTTP/JSON
                      │
┌─────────────────────▼───────────────────────────────────┐
│                  FastAPI Application                     │
│  ┌───────────────────────────────────────────────────┐  │
│  │              API Router Layer                     │  │
│  │  ┌──────────┬──────────┬──────────┬────────────┐ │  │
│  │  │ Areas    │ Goals    │ Habits   │ Tasks      │ │  │
│  │  ├──────────┼──────────┼──────────┼────────────┤ │  │
│  │  │ Contacts │ Refs     │ Health   │ Finance    │ │  │
│  │  ├──────────┼──────────┴──────────┴────────────┤ │  │
│  │  │ Auth     │ AI Stub (placeholder)            │ │  │
│  │  └──────────┴───────────────────────────────────┘ │  │
│  └────────────────────┬──────────────────────────────┘  │
│                       │                                  │
│  ┌────────────────────▼──────────────────────────────┐  │
│  │           Business Logic Layer                    │  │
│  │  - Pydantic Schemas (validation)                  │  │
│  │  - SQLModel Models (ORM)                          │  │
│  │  - Dependency Injection (sessions, auth)          │  │
│  └────────────────────┬──────────────────────────────┘  │
│                       │                                  │
│  ┌────────────────────▼──────────────────────────────┐  │
│  │            Data Access Layer                      │  │
│  │  - SQLAlchemy 2.x Core                            │  │
│  │  - Session Management                             │  │
│  │  - Connection Pooling                             │  │
│  └────────────────────┬──────────────────────────────┘  │
└─────────────────────┬─┴──────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────┐
│               SQLite Database                            │
│            /data/app.sqlite3                             │
│  ┌───────────────────────────────────────────────────┐  │
│  │  Users  Goals  Habits  Tasks  Contacts  ...      │  │
│  └───────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────┘
```

---

## 2. Technology Stack

### 2.1 Backend Framework
**FastAPI 0.104+**
- Modern async Python web framework
- Automatic OpenAPI/Swagger documentation
- Built-in validation via Pydantic
- High performance (comparable to Node.js/Go)
- Type hints for better IDE support

**Why FastAPI?**
- Minimal boilerplate for rapid MVP development
- Excellent documentation auto-generation
- Strong typing reduces bugs
- Easy to test with `TestClient`
- Future-ready for async operations

### 2.2 Database & ORM
**SQLite 3**
- File-based database (`/data/app.sqlite3`)
- Zero configuration
- ACID compliant
- Sufficient for single-user/small team use
- Easy to backup (copy file)

**SQLModel 0.14+**
- Combines SQLAlchemy + Pydantic
- Single class definition for DB models and API schemas
- Type safety across entire stack
- Familiar to SQLAlchemy users

**SQLAlchemy 2.x**
- Mature ORM with excellent query capabilities
- Relationship management
- Migration support via Alembic
- Connection pooling

**Alembic**
- Database migration management
- Version control for schema changes
- Rollback capabilities

### 2.3 Authentication
**Bcrypt + Starlette Sessions**
- Bcrypt for password hashing (cost factor 12)
- Starlette's `SessionMiddleware` for cookie-based sessions
- Signed cookies prevent tampering
- HTTP-only cookies for XSS protection

**No OAuth/JWT in MVP:**
- Reduces complexity
- Appropriate for single-user local deployment
- Can add in Phase 2 if multi-user needed

### 2.4 AI Integration (Stubbed)
**Deterministic Placeholders**
- `ai_stub.py` module with clear function signatures
- Returns hardcoded inspirational content
- Future-ready for OpenAI/Anthropic/local LLM integration

**Placeholder Strategy:**
```python
def generate_bible_verse(area: str) -> str:
    # TODO: Replace with real AI call
    return STATIC_VERSES.get(area, DEFAULT_VERSE)
```

### 2.5 Testing
**Pytest**
- Industry-standard Python testing
- FastAPI's `TestClient` for endpoint testing
- Fixtures for database setup/teardown
- Coverage reporting

### 2.6 Development Tools
- **Uvicorn:** ASGI server for local development
- **Python-dotenv:** Environment variable management
- **Pydantic v2:** Data validation and settings
- **Black:** Code formatting (optional)
- **MyPy:** Static type checking (optional)

---

## 3. Project Structure

```
/
├── data/
│   └── app.sqlite3              # SQLite database (created on first run)
│
├── docs/                         # All documentation
│   ├── PRD.md
│   ├── Architecture.md          # This file
│   ├── API-Schema.md
│   ├── Data-Model.md
│   ├── UX-Wireframes.md
│   ├── Acceptance-Tests.md
│   ├── Prompts.md
│   ├── Implementation-Plan.md
│   └── Security-Privacy.md
│
├── seed/                         # Seed data for testing
│   ├── sample.csv               # Normalized CSV data
│   └── fixtures.json            # Structured JSON fixtures
│
├── server/                       # FastAPI application
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py              # App entry point, router registration
│   │   ├── db.py                # Database engine, session management
│   │   ├── models.py            # SQLModel database models
│   │   ├── schemas.py           # Pydantic request/response schemas
│   │   ├── auth.py              # Authentication logic
│   │   ├── ai_stub.py           # AI placeholder functions
│   │   │
│   │   └── routers/             # Modular API endpoints
│   │       ├── __init__.py
│   │       ├── areas.py         # Life area management
│   │       ├── entries.py       # Journal entries
│   │       ├── goals.py         # Goal CRUD + progress
│   │       ├── habits.py        # Habit tracking + streaks
│   │       ├── tasks.py         # Todo management
│   │       ├── contacts.py      # Contact management
│   │       ├── references.py    # Websites, scriptures, laws
│   │       ├── health.py        # Health catalog endpoints
│   │       ├── finance.py       # Banking, assets, liabilities
│   │       └── ai.py            # AI-generated content
│   │
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── conftest.py          # Pytest fixtures
│   │   └── test_core.py         # Core API tests
│   │
│   ├── migrations/               # Alembic migrations
│   │   ├── versions/
│   │   │   └── 001_initial.py
│   │   └── env.py
│   │
│   ├── alembic.ini              # Alembic configuration
│   ├── .env.example             # Environment template
│   └── requirements.txt         # Python dependencies
│
├── Dockerfile                    # Container build
├── Makefile                      # Common commands
├── README.md                     # Setup and usage guide
└── .gitignore                    # Git exclusions
```

---

## 4. Data Flow

### 4.1 Typical Request Flow

```
1. HTTP Request
   └─> FastAPI Router (e.g., /api/goals POST)
       └─> Dependency Injection (get_db, get_current_user)
           └─> Pydantic Schema Validation (GoalCreate)
               └─> Business Logic (in router or service)
                   └─> SQLModel ORM Call (session.add, session.commit)
                       └─> SQLite Database Write
                           └─> Return Pydantic Response Schema
                               └─> JSON Response
```

### 4.2 Authentication Flow

```
1. User Registration
   POST /api/auth/register
   └─> Validate username/password (Pydantic)
       └─> Hash password (bcrypt)
           └─> Create User record
               └─> Return success

2. User Login
   POST /api/auth/login
   └─> Look up user by username
       └─> Verify password hash
           └─> Create session (set signed cookie)
               └─> Return user info

3. Authenticated Request
   GET /api/goals
   └─> Check session cookie
       └─> Validate signature
           └─> Load user from session
               └─> Proceed with request (inject current_user)
```

### 4.3 AI Content Generation (Stubbed)

```
GET /api/ai/verse?area=spiritual
└─> Call ai_stub.generate_bible_verse("spiritual")
    └─> Return static placeholder
        └─> (Future: Call OpenAI API, cache result)
```

---

## 5. Database Design

### 5.1 Core Principles
- **Normalized:** Minimize redundancy, use foreign keys
- **Indexed:** Key fields indexed for query performance
- **Timestamped:** All entities have created_at, updated_at
- **Soft Deletes:** Consider adding `deleted_at` for auditing (optional)

### 5.2 Entity Relationships

```
User
  └─> has many Goals
  └─> has many Habits
  └─> has many Tasks
  └─> has many Contacts
  └─> has many References
  └─> has many Entries
  └─> has many HealthCatalogItems
  └─> has many FinancialAccounts

LifeArea (enum-like, 8 predefined)
  ├─> referenced by Goals (many-to-many via tags)
  ├─> referenced by Habits (many-to-many via tags)
  ├─> referenced by Tasks (foreign key)
  ├─> referenced by Contacts (many-to-many)
  ├─> referenced by References (many-to-many)
  └─> referenced by Entries (foreign key)

Contact
  └─> linked to Tasks (optional FK)
  └─> linked to Goals (optional FK)
  └─> birthday → auto-calculates age

Reference
  └─> type field (website, scripture, law)
  └─> law_level field (federal, state, local) if type=law

HealthCatalogItem
  └─> catalog_type (doctor, food, supplement, medication, motion)

ConflictTopic (One-on-One specific)
  └─> user_id (FK)
  └─> topic, resolution_strategy

FinancialAccount
  └─> account_type (banking, asset, liability)
```

### 5.3 Key Design Decisions

**Many-to-Many for Life Areas:**
- Goals/Habits can span multiple areas (e.g., "Exercise 3x/week" → Physical + Hobby)
- Use association tables for flexibility

**Polymorphic Health Catalog:**
- Single `HealthCatalogItem` table with `catalog_type` discriminator
- Simpler than 5 separate tables
- JSON field for type-specific attributes (optional)

**Contact Linking:**
- Optional FK on Task, Goal allows linking relevant people
- Avoids complex many-to-many for MVP

**Birthday Age Calculation:**
- Computed at query time via SQL or Python helper function
- No stored age field (would require daily updates)

---

## 6. API Design

### 6.1 RESTful Principles
- **Resources:** Nouns (goals, habits, tasks, etc.)
- **HTTP Verbs:** GET (read), POST (create), PUT/PATCH (update), DELETE (delete)
- **Status Codes:** 200 OK, 201 Created, 204 No Content, 400 Bad Request, 401 Unauthorized, 404 Not Found, 500 Server Error

### 6.2 URL Structure

```
/api/auth/register              POST    Register new user
/api/auth/login                 POST    Login and create session
/api/auth/logout                POST    Destroy session
/api/auth/me                    GET     Get current user info

/api/areas                      GET     List all life areas (static 8)

/api/goals                      GET     List user's goals (filter by area, timeframe)
/api/goals                      POST    Create new goal
/api/goals/{id}                 GET     Get goal details
/api/goals/{id}                 PUT     Update goal
/api/goals/{id}                 DELETE  Delete goal

/api/habits                     GET     List habits (filter by area, type)
/api/habits                     POST    Create habit
/api/habits/{id}                GET     Get habit details
/api/habits/{id}                PUT     Update habit
/api/habits/{id}                DELETE  Delete habit
/api/habits/{id}/checkin        POST    Increment streak

/api/tasks                      GET     List tasks (filter by area, status)
/api/tasks                      POST    Create task
/api/tasks/{id}                 GET     Get task details
/api/tasks/{id}                 PUT     Update task (including status change)
/api/tasks/{id}                 DELETE  Delete task

/api/contacts                   GET     List contacts (filter by area)
/api/contacts                   POST    Create contact
/api/contacts/{id}              GET     Get contact details
/api/contacts/{id}              PUT     Update contact
/api/contacts/{id}              DELETE  Delete contact
/api/contacts/birthdays         GET     Upcoming birthdays with age calculation

/api/references                 GET     List references (filter by area, type)
/api/references                 POST    Create reference
/api/references/{id}            GET     Get reference details
/api/references/{id}            PUT     Update reference
/api/references/{id}            DELETE  Delete reference

/api/health                     GET     List health catalog items (filter by type)
/api/health                     POST    Create health item
/api/health/{id}                GET     Get health item details
/api/health/{id}                PUT     Update health item
/api/health/{id}                DELETE  Delete health item

/api/finance                    GET     List financial accounts (filter by type)
/api/finance                    POST    Create financial account
/api/finance/{id}               GET     Get account details
/api/finance/{id}               PUT     Update account
/api/finance/{id}               DELETE  Delete account

/api/one-on-one/conflicts       GET     List 3 conflict topics
/api/one-on-one/conflicts       POST    Create/update conflict topic
/api/one-on-one/conflicts/{id}  PUT     Update conflict topic
/api/one-on-one/conflicts/{id}  DELETE  Delete conflict topic

/api/entries                    GET     List journal entries (filter by area)
/api/entries                    POST    Create entry
/api/entries/{id}               GET     Get entry details
/api/entries/{id}               PUT     Update entry
/api/entries/{id}               DELETE  Delete entry

/api/ai/verse                   GET     Get AI-generated Bible verse (query param: area)
/api/ai/insight                 GET     Get AI-generated insight (query param: area)
```

### 6.3 Request/Response Format
**Content-Type:** `application/json`
**Charset:** UTF-8

**Standard Response Envelope (Success):**
```json
{
  "data": { ... },
  "message": "Goal created successfully"
}
```

**Standard Error Response:**
```json
{
  "detail": "Invalid credentials",
  "error_code": "AUTH_INVALID_CREDENTIALS"
}
```

### 6.4 Pagination (Optional for MVP)
If implementing pagination:
```
GET /api/goals?page=1&limit=20

Response:
{
  "data": [...],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 47,
    "pages": 3
  }
}
```

---

## 7. Security Architecture

### 7.1 Authentication Layers
1. **Password Hashing:** Bcrypt with cost factor 12
2. **Session Management:** Signed cookies (HMAC-SHA256)
3. **Session Storage:** Server-side (in-memory for MVP, can move to Redis later)
4. **Cookie Settings:** HTTP-only, Secure (HTTPS), SameSite=Lax

### 7.2 Authorization
**MVP Approach:**
- Single-user per instance (no multi-tenancy)
- All authenticated endpoints check `current_user`
- Users can only access their own data (enforced by user_id FK filters)

**Dependency Injection Pattern:**
```python
async def get_current_user(session: Session = Depends(get_session)):
    # Validate session cookie, return User or raise 401
    pass

@router.get("/goals")
def list_goals(current_user: User = Depends(get_current_user)):
    # current_user automatically injected
    return query_goals(user_id=current_user.id)
```

### 7.3 Input Validation
**Pydantic Schemas:**
- All input validated via Pydantic models
- Type checking, length limits, regex patterns
- Automatic 422 Unprocessable Entity on validation failure

**SQL Injection Prevention:**
- SQLAlchemy ORM parameterizes all queries
- Never use string concatenation for SQL

**XSS Prevention:**
- API returns JSON (not HTML), minimal XSS risk
- Future frontend must sanitize on render

### 7.4 Secrets Management
**.env File:**
```
APP_SECRET=random-64-character-secret-key-here
DATABASE_URL=sqlite:///./data/app.sqlite3
ENVIRONMENT=development
```

**Deployment:**
- `.env` excluded from git via `.gitignore`
- `.env.example` committed with placeholder values
- Production: Use environment variables (Docker secrets, etc.)

---

## 8. Performance Considerations

### 8.1 Database Optimization
**Indexes:**
- Primary keys (auto-indexed)
- Foreign keys (user_id, area_id, etc.)
- Frequently queried fields (status, created_at)

**Query Optimization:**
- Use `select` with `joinedload`/`selectinload` for relationships
- Avoid N+1 queries
- Limit result sets with pagination

**Connection Pooling:**
- SQLAlchemy's default pool (5 connections)
- Sufficient for single-user local deployment

### 8.2 Caching (Future)
**MVP:** No caching layer
**Post-MVP:** Consider:
- Redis for session storage
- Cache AI-generated content (verse, insights)
- Cache static life area definitions

### 8.3 Async vs Sync
**MVP:** Synchronous SQLAlchemy
**Rationale:** Simpler code, adequate performance for local use
**Future:** Migrate to `asyncpg` + async SQLAlchemy for high concurrency

---

## 9. Scalability & Future Architecture

### 9.1 Current Limitations
- Single SQLite file (no horizontal scaling)
- Single-user per instance
- No background job processing

### 9.2 Migration Path to Multi-User SaaS
**Phase 2 Changes:**
1. **Database:** Migrate to PostgreSQL
   - Alembic makes this straightforward
   - Update `DATABASE_URL` in .env
2. **Authentication:** Add OAuth, JWT tokens for API
3. **Multi-Tenancy:** Enforce user_id filtering rigorously
4. **Session Storage:** Move to Redis
5. **Background Jobs:** Add Celery for email, AI processing
6. **Caching:** Redis for frequently accessed data
7. **API Rate Limiting:** Prevent abuse
8. **Monitoring:** Add Sentry, Datadog, etc.

### 9.3 Frontend Integration
**API-First Design Benefits:**
- Frontend can be any framework (React, Vue, Svelte, Flutter, etc.)
- Mobile apps can consume same API
- Third-party integrations possible

**CORS Configuration:**
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## 10. Deployment Architecture

### 10.1 Local Development
```bash
# Install dependencies
pip install -r server/requirements.txt

# Run migrations
cd server
alembic upgrade head

# Start server
uvicorn app.main:app --reload --port 8000
```

**Access:**
- API: http://localhost:8000
- Swagger Docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### 10.2 Docker Deployment
**Dockerfile:**
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY server/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY server/ .
COPY data/ /app/data/
RUN alembic upgrade head
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Run:**
```bash
docker build -t life-mgmt-app .
docker run -p 8000:8000 -v $(pwd)/data:/app/data life-mgmt-app
```

### 10.3 Production Considerations (Post-MVP)
- **Reverse Proxy:** Nginx or Traefik
- **HTTPS:** Let's Encrypt certificates
- **Process Manager:** Systemd or Docker Compose
- **Monitoring:** Prometheus + Grafana
- **Backups:** Automated SQLite backups (cron job)
- **Logging:** Centralized logging (ELK stack, Loki)

---

## 11. Testing Strategy

### 11.1 Unit Tests
**Coverage:**
- Model validations (Pydantic schemas)
- Business logic functions (age calculation, streak increments)
- AI stub functions

**Tools:** Pytest with coverage plugin

### 11.2 Integration Tests
**Coverage:**
- API endpoint responses (status codes, JSON structure)
- Database CRUD operations
- Authentication flows
- Error handling

**Pattern:**
```python
def test_create_goal(client: TestClient, auth_headers):
    response = client.post("/api/goals", json={...}, headers=auth_headers)
    assert response.status_code == 201
    assert response.json()["data"]["title"] == "Test Goal"
```

### 11.3 Test Database
**Approach:**
- In-memory SQLite (`:memory:`) for fast tests
- Or separate `test.sqlite3` file cleaned between tests
- Fixtures create/tear down test data

### 11.4 Manual Testing
**Postman/Insomnia:**
- Collection of API requests
- Environment variables for localhost

**Swagger UI:**
- Built-in interactive API documentation
- Test endpoints directly in browser

---

## 12. Monitoring & Observability (Future)

### 12.1 Logging
**Current:** Python `logging` module
**Levels:** DEBUG, INFO, WARNING, ERROR, CRITICAL
**Output:** Console (stdout) for MVP

**Future:**
- Structured logging (JSON format)
- Log aggregation (Elasticsearch, Loki)
- Request/response logging middleware

### 12.2 Metrics
**Future Metrics:**
- Request latency (p50, p95, p99)
- Error rate by endpoint
- Database query performance
- Active sessions count
- AI API call costs (when integrated)

**Tools:** Prometheus, Grafana

### 12.3 Error Tracking
**Future:** Sentry integration for exception tracking

---

## 13. Development Workflow

### 13.1 Local Setup
1. Clone repository
2. Create virtual environment: `python -m venv venv`
3. Activate: `source venv/bin/activate`
4. Install deps: `pip install -r server/requirements.txt`
5. Copy `.env.example` to `.env`, set `APP_SECRET`
6. Run migrations: `cd server && alembic upgrade head`
7. Seed database: `python seed_db.py`
8. Start server: `uvicorn app.main:app --reload`

### 13.2 Making Changes
1. Create feature branch
2. Modify code (models, routers, schemas)
3. Run tests: `pytest`
4. Create migration (if schema changed): `alembic revision --autogenerate -m "description"`
5. Test migration: `alembic upgrade head`
6. Commit changes
7. (Optional) Create pull request

### 13.3 Code Quality
**Recommended Tools:**
- **Black:** Code formatting (`black .`)
- **Flake8:** Linting (`flake8 .`)
- **MyPy:** Type checking (`mypy .`)
- **Pytest-cov:** Coverage (`pytest --cov=app`)

**Pre-commit Hooks (Optional):**
```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/psf/black
    hooks:
      - id: black
  - repo: https://github.com/pycqa/flake8
    hooks:
      - id: flake8
```

---

## 14. Migration from MVP to Production

### 14.1 Database Migration
**SQLite → PostgreSQL:**
1. Export data: `sqlite3 data/app.sqlite3 .dump > export.sql`
2. Clean SQL for PostgreSQL compatibility
3. Update `DATABASE_URL` in `.env`
4. Import: `psql -U user -d dbname < export.sql`
5. Verify data integrity
6. Run Alembic migrations if schema differs

### 14.2 AI Integration
**Stub → Real API:**
1. Choose provider (OpenAI, Anthropic, local Ollama)
2. Update `ai_stub.py` → `ai_service.py`
3. Add API key to `.env`
4. Implement caching (Redis) to minimize API costs
5. Add rate limiting
6. Test thoroughly (costs money!)

### 14.3 Frontend Integration
1. Build frontend (React/Vue/Svelte)
2. Configure CORS for frontend origin
3. Deploy frontend separately (Vercel, Netlify, etc.)
4. Or serve static files from FastAPI (`StaticFiles`)

---

## 15. Appendix

### 15.1 Key Design Patterns
- **Dependency Injection:** FastAPI's `Depends()` for session, user
- **Repository Pattern:** (Optional) Abstract DB access into repository classes
- **DTO Pattern:** Pydantic schemas separate from DB models
- **Factory Pattern:** Test fixtures for object creation

### 15.2 Coding Conventions
- **Naming:** snake_case for variables/functions, PascalCase for classes
- **Type Hints:** Required on all function signatures
- **Docstrings:** For complex functions and all routers
- **Error Handling:** Raise `HTTPException` with appropriate status codes

### 15.3 Related Documentation
- [PRD.md](PRD.md) - Product requirements
- [Data-Model.md](Data-Model.md) - Detailed schema definitions
- [API-Schema.md](API-Schema.md) - Full endpoint specifications
- [Security-Privacy.md](Security-Privacy.md) - Security best practices

### 15.4 External Resources
- FastAPI Docs: https://fastapi.tiangolo.com/
- SQLModel Docs: https://sqlmodel.tiangolo.com/
- Alembic Docs: https://alembic.sqlalchemy.org/
- Pydantic Docs: https://docs.pydantic.dev/
