# Acceptance Tests
## AI-Assisted Life Management Application MVP

**Version:** 1.0
**Date:** 2025-10-16

---

## Test Scenarios

### 1. User Registration & Authentication

**Scenario 1.1: Successful Registration**
- Given I am a new user
- When I POST to `/api/auth/register` with valid credentials
- Then I receive 201 status
- And user account is created in database
- And password is hashed with bcrypt

**Scenario 1.2: Duplicate Username**
- Given username "hannah" already exists
- When I register with username "hannah"
- Then I receive 400 status
- And error message "Username already exists"

**Scenario 1.3: Successful Login**
- Given I have a registered account
- When I POST to `/api/auth/login` with correct credentials
- Then I receive 200 status
- And session cookie is set
- And I can access protected endpoints

**Scenario 1.4: Failed Login**
- When I login with incorrect password
- Then I receive 401 status
- And no session cookie is set

---

### 2. Goals Management

**Scenario 2.1: Create Goal**
- Given I am authenticated
- When I POST to `/api/goals` with title, timeframe, area_ids
- Then goal is created with ID
- And goal appears in GET `/api/goals`
- And goal is linked to specified life areas

**Scenario 2.2: Update Goal Progress**
- Given I have a goal with 0% progress
- When I PUT `/api/goals/{id}` with progress_percentage=50
- Then goal shows 50% progress
- And updated_at timestamp changes

**Scenario 2.3: Complete Goal**
- When I PUT `/api/goals/{id}` with status="completed"
- Then goal status is "completed"
- And progress_percentage can be set to 100

**Scenario 2.4: Filter Goals by Area**
- Given I have 3 goals in Physical/Health, 2 in Spiritual
- When I GET `/api/goals?area_id=1` (Physical/Health)
- Then I receive only 3 goals

---

### 3. Habits & Streaks

**Scenario 3.1: Create Habit**
- Given I am authenticated
- When I POST to `/api/habits` with name, type, frequency, area_ids
- Then habit is created
- And current_streak is 0
- And longest_streak is 0

**Scenario 3.2: First Check-In**
- Given I have a habit with 0 streak
- When I POST `/api/habits/{id}/checkin`
- Then current_streak becomes 1
- And longest_streak becomes 1
- And last_checkin_date is today

**Scenario 3.3: Consecutive Check-In**
- Given I checked in yesterday (streak=5)
- When I check in today
- Then current_streak becomes 6
- And longest_streak updates if 6 > previous longest

**Scenario 3.4: Streak Reset (Skipped Day)**
- Given I last checked in 3 days ago (daily habit)
- When I check in today
- Then current_streak resets to 1
- And longest_streak remains unchanged

**Scenario 3.5: Duplicate Check-In**
- Given I already checked in today
- When I try to check in again
- Then I receive 400 status
- And error "Already checked in today"

---

### 4. Tasks Management

**Scenario 4.1: Create Task**
- When I POST to `/api/tasks` with title, area_id
- Then task is created with status="todo"
- And priority="medium" (default)

**Scenario 4.2: Task Status Transition**
- Given task with status="todo"
- When I PUT status to "doing"
- Then status updates to "doing"
- When I PUT status to "done"
- Then status is "done"
- And completed_at timestamp is set

**Scenario 4.3: Task with Contact**
- When I create task with contact_id=5
- Then task is linked to that contact
- And task JSON includes contact details

**Scenario 4.4: Filter Tasks by Status**
- Given I have 10 tasks: 5 todo, 3 doing, 2 done
- When I GET `/api/tasks?status=doing`
- Then I receive only 3 tasks

---

### 5. Contacts & Birthdays

**Scenario 5.1: Create Contact**
- When I POST to `/api/contacts` with name, birthday, area_ids
- Then contact is created
- And birthday is stored as date

**Scenario 5.2: Birthday Age Calculation**
- Given contact with birthday "1965-11-02"
- When I GET `/api/contacts/birthdays` on "2025-10-16"
- Then response includes:
  - years: 59
  - months: 11
  - days: 14
  - days_until_birthday: 17

**Scenario 5.3: Upcoming Birthdays**
- Given 5 contacts with various birthdays
- When I GET `/api/contacts/birthdays?days_ahead=30`
- Then I receive only contacts with birthdays in next 30 days
- And results are sorted by days_until_birthday

---

### 6. References

**Scenario 6.1: Create Website Reference**
- When I POST to `/api/references` with:
  - type="website"
  - title="Medicare.gov"
  - url="https://medicare.gov"
  - area_ids=[1]
- Then reference is created
- And can be retrieved by area filter

**Scenario 6.2: Create Law Reference**
- When I create reference with:
  - type="law"
  - law_level="federal"
  - content="Summary of ACA..."
- Then law_level is stored
- When I GET `/api/references?type=law&law_level=federal`
- Then this reference is included

---

### 7. Health Catalog

**Scenario 7.1: Create Doctor**
- When I POST to `/api/health` with:
  - catalog_type="doctor"
  - name="Dr. Sarah Johnson"
  - doctor_specialty="Primary Care"
  - doctor_phone="555-0123"
- Then doctor is stored in health_catalog_items

**Scenario 7.2: Create Supplement**
- When I create health item with:
  - catalog_type="supplement"
  - name="Vitamin D3"
  - supplement_dosage="2000 IU"
  - frequency_description="daily"
- Then supplement is created

**Scenario 7.3: Filter by Catalog Type**
- Given I have 2 doctors, 3 supplements, 1 medication
- When I GET `/api/health?catalog_type=supplement`
- Then I receive only 3 supplements

---

### 8. Financial Accounts

**Scenario 8.1: Create Banking Account**
- When I POST to `/api/finance` with:
  - account_type="banking"
  - name="Chase Checking"
  - current_balance=5420.50
- Then account is created

**Scenario 8.2: Create Liability**
- When I create account with:
  - account_type="liability"
  - name="Home Mortgage"
  - current_balance=285000.00
  - interest_rate=3.75
  - due_date="2025-01-15"
- Then liability is created with all fields

**Scenario 8.3: Filter by Account Type**
- Given 2 banking, 3 assets, 2 liabilities
- When I GET `/api/finance?account_type=liability`
- Then I receive only 2 liabilities

---

### 9. One-on-One Conflict Topics

**Scenario 9.1: Create Conflict Topic**
- When I POST to `/api/one-on-one/conflicts` with:
  - topic="Household chores"
  - resolution_strategy="Weekly rotation chart"
- Then conflict topic is created

**Scenario 9.2: Max 3 Topics Enforced**
- Given I already have 3 conflict topics
- When I try to create a 4th
- Then I receive 400 status
- And error "Maximum 3 conflict topics allowed"

**Scenario 9.3: Update Conflict Progress**
- Given a conflict topic exists
- When I PUT with progress_notes="Chart working well"
- Then notes are updated
- And updated_at changes

---

### 10. Journal Entries

**Scenario 10.1: Create Entry**
- When I POST to `/api/entries` with:
  - area_id=8 (Spiritual)
  - title="Morning reflection"
  - content="Today I felt..."
- Then entry is created
- And entry_date defaults to today

**Scenario 10.2: Filter Entries by Area**
- Given 5 entries in Spiritual, 3 in Physical/Health
- When I GET `/api/entries?area_id=8`
- Then I receive only 5 Spiritual entries

**Scenario 10.3: Filter by Date Range**
- When I GET `/api/entries?date_from=2025-10-01&date_to=2025-10-31`
- Then I receive only entries from October 2025

---

### 11. AI Content (Stubbed)

**Scenario 11.1: Get Bible Verse**
- When I GET `/api/ai/verse?area=spiritual`
- Then I receive a deterministic Bible verse
- And response includes verse text and reference

**Scenario 11.2: Get Insight**
- When I GET `/api/ai/insight?area=physical_health`
- Then I receive a health-related insight
- And content is static/placeholder (MVP)

---

### 12. Authorization

**Scenario 12.1: Unauthenticated Access**
- Given I have no session cookie
- When I try to GET `/api/goals`
- Then I receive 401 status
- And error "Authentication required"

**Scenario 12.2: User Isolation**
- Given User A has 5 goals
- And User B has 3 goals
- When User B requests GET `/api/goals`
- Then User B receives only their 3 goals (not User A's)

---

### 13. Data Persistence

**Scenario 13.1: Server Restart**
- Given I create a goal
- When I restart the uvicorn server
- And I query for my goals
- Then the goal still exists (SQLite persisted)

---

### 14. Database Migrations

**Scenario 14.1: Run Migrations**
- Given a fresh environment
- When I run `alembic upgrade head`
- Then all tables are created
- And I can start the app without errors

**Scenario 14.2: Seed Data**
- When I run seed script
- Then 8 life areas are populated
- And I can reference them in API calls

---

## Non-Functional Acceptance Criteria

### Performance
✅ API responses < 500ms (95th percentile)
✅ Database queries use indexes
✅ No N+1 query issues

### Security
✅ Passwords hashed with bcrypt (cost 12)
✅ Session cookies are HTTP-only and signed
✅ SQL injection prevented (parameterized queries)
✅ Input validation on all endpoints

### Reliability
✅ Graceful error handling (no 500 errors for user mistakes)
✅ Transactions for multi-step operations
✅ Foreign key constraints enforced

### Usability (API)
✅ Consistent JSON response format
✅ Clear error messages
✅ OpenAPI docs auto-generated
✅ Sensible defaults (status, priority, etc.)

### Maintainability
✅ Code follows PEP 8 (or formatted with Black)
✅ Type hints on all functions
✅ Docstrings for complex logic
✅ Modular router structure

---

## MVP Blockers (Must Pass)

1. ✅ User can register and login
2. ✅ All 8 life areas are defined
3. ✅ Goals CRUD works with progress tracking
4. ✅ Habits CRUD works with streak calculation
5. ✅ Tasks CRUD works with status transitions
6. ✅ Contacts CRUD works with birthday age calculation
7. ✅ References CRUD works with type filtering
8. ✅ Health catalog CRUD works
9. ✅ Financial accounts CRUD works
10. ✅ One-on-One conflict topics work (max 3)
11. ✅ Journal entries CRUD works
12. ✅ AI stub endpoints return placeholder content
13. ✅ Data persists across server restarts
14. ✅ Alembic migrations can be run
15. ✅ Pytest suite passes
16. ✅ README provides clear setup instructions

---

## Testing Tools

- **Manual Testing:** Swagger UI at `/docs`
- **Automated Testing:** Pytest with FastAPI TestClient
- **Database Inspection:** sqlite3 CLI or DB Browser for SQLite
- **API Client:** Postman/Insomnia collections (optional)

---

## Test Data Requirements

Seed database should include:
- 1 test user (username: "test_user", password: "testpass123")
- All 8 life areas
- Sample goals (1-2 per area)
- Sample habits (1 per area)
- Sample tasks (2-3 across areas)
- Sample contacts (5+, including some with birthdays)
- Sample health items (1 doctor, 1 supplement, 1 medication, 1 motion)
- Sample financial accounts (1 banking, 1 asset, 1 liability)
- Sample conflict topics (2-3)
- Sample references (mix of websites, laws, scriptures)
- Sample journal entries (3-5 across areas)

---

## Related Documents
- [PRD.md](PRD.md) - Product requirements
- [API-Schema.md](API-Schema.md) - Endpoint specifications
- [Data-Model.md](Data-Model.md) - Database schema
- [Implementation-Plan.md](Implementation-Plan.md) - Build steps
