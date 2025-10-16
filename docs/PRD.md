# Product Requirements Document (PRD)
## AI-Assisted Life Management Application

**Version:** 1.0 MVP
**Date:** 2025-10-16
**Author:** Senior PM + Tech Lead

---

## 1. Executive Summary

The Life Management Application is a comprehensive web-based tool that helps users organize, track, and improve all aspects of their lives across 8 core areas. The MVP focuses on essential tracking, goal-setting, habit formation, and AI-assisted inspirational guidance delivered through a simple, intuitive interface backed by a lightweight SQLite database.

### Vision
Empower individuals to achieve holistic life balance through structured tracking, meaningful insights, and AI-assisted guidance across health, relationships, finances, and personal growth.

### Success Metrics (MVP)
- Users can manage goals, habits, and tasks across all 8 life areas
- AI-generated inspirational content appears reliably (via stubs initially)
- Data persists locally with zero external dependencies
- Complete CRUD operations for all core entities
- Sub-500ms response times for all API calls

---

## 2. Problem Statement

People struggle to manage multiple life dimensions simultaneously. Existing tools are either:
- Too narrow (fitness-only, finance-only)
- Too complex (enterprise project management)
- Lack spiritual/relational depth
- Require cloud services and subscriptions

**User Pain Points:**
- "I can track my workouts but not my spiritual growth"
- "I forget important birthdays and relationship milestones"
- "My goals are scattered across apps, notebooks, and my head"
- "I want privacy - I don't want my personal data in the cloud"

---

## 3. Target Users

### Primary Persona: "Holistic Hannah"
- **Age:** 28-45
- **Profile:** Working professional seeking work-life balance
- **Goals:** Improve health, deepen relationships, grow spiritually, manage finances
- **Tech Comfort:** Moderate (can run local apps, prefers simplicity)
- **Privacy Needs:** High (prefers local-first tools)

### Secondary Persona: "Organized Oliver"
- **Age:** 35-55
- **Profile:** Detail-oriented individual managing family, career, civic duties
- **Goals:** Track everything systematically, reduce mental overhead
- **Tech Comfort:** High (comfortable with Docker, command-line)
- **Privacy Needs:** Very high (self-hosts when possible)

---

## 4. Life Areas & Core Features

### 4.1 Physical/Health
**Description:** Track and optimize physical wellbeing through health catalogs and motion tracking.

**Features:**
- Health Catalogs: Doctors, Foods, Supplements, Medications, Motion Activities
- Link health items to goals and habits
- Track frequency and notes for each catalog item

**User Stories:**
- As a user, I can add my doctors with contact info and specialties
- As a user, I can track my food choices and vitamins
- As a user, I can log motion activities (walk/run/yoga) with frequency

### 4.2 Hobby
**Description:** Pursue creative interests and hands-on projects.

**Features:**
- "Something your hands help to make" goal tracking
- Project-specific todos and contacts
- Reference materials (websites, tutorials)

**User Stories:**
- As a user, I can set hobby goals (e.g., "Build a birdhouse by Q2")
- As a user, I can track progress on creative projects
- As a user, I can save reference links for hobby inspiration

### 4.3 Income & Expenses
**Description:** Monitor cash flow and spending patterns.

**Features:**
- Expense list with categorization
- Income tracking
- Contact references for employers, clients, vendors

**User Stories:**
- As a user, I can list all recurring expenses with amounts and due dates
- As a user, I can track income sources and amounts
- As a user, I can reference financial contacts and websites

### 4.4 Assets & Liabilities
**Description:** Manage wealth, debts, and financial obligations.

**Features:**
- Banking account tracking
- Asset lists (property, investments, valuables)
- Liability tracking (loans, mortgages, credit cards)
- Financial goals (pay off debt, save for X)

**User Stories:**
- As a user, I can add all my bank accounts with current balances
- As a user, I can track assets like my home, car, retirement accounts
- As a user, I can monitor liabilities with balances and interest rates

### 4.5 One-on-One Relationship
**Description:** Strengthen primary romantic/partner relationship.

**Features:**
- Identify 3 main argument topics with resolution strategies
- Relationship-specific goals (short/medium/long)
- Contact info for counselors, resources
- AI-generated relationship insights

**User Stories:**
- As a user, I can document our 3 recurring conflict topics
- As a user, I can track strategies to fix each conflict area
- As a user, I can set relationship goals (e.g., "Weekly date nights")

### 4.6 Family & Friends
**Description:** Nurture social connections and remember important dates.

**Features:**
- Birthday list with auto-calculated age (Years, Months, Days)
- Contact information for each person
- Relationship-specific goals and habits
- Gift ideas and communication tracking

**User Stories:**
- As a user, I can add family/friends with birthdays and contact info
- As a user, I can see upcoming birthdays with exact age calculation
- As a user, I can set goals like "Call Mom weekly"

### 4.7 Politics/Civics
**Description:** Engage with civic duties and stay informed on governance.

**Features:**
- Federal/State/Local law references
- Political goals (e.g., "Attend town hall monthly")
- Contact info for representatives, organizations
- Reference links to legislation and news sources

**User Stories:**
- As a user, I can save important laws and regulations by level (federal/state/local)
- As a user, I can track civic engagement goals
- As a user, I can maintain contacts for elected officials

### 4.8 Spiritual
**Description:** Deepen faith and spiritual practices.

**Features:**
- AI-generated Bible verses and inspirational content
- Spiritual goals (prayer, study, service)
- Scripture and resource references
- Habit tracking (daily devotions, meditation)

**User Stories:**
- As a user, I receive AI-generated Bible verses relevant to my spiritual focus
- As a user, I can set spiritual goals like "Read one Psalm daily"
- As a user, I can track spiritual habits and streaks

---

## 5. Cross-Cutting Features

### 5.1 Goals System
**Timeframes:** Short, Medium, Long term
**Attributes:**
- Title and description
- Timeframe (dropdown selection)
- Due date (optional)
- Status (Not Started, In Progress, Completed, Abandoned)
- Progress percentage (0-100%)
- Associated life area(s)
- Optional contact reference

**User Stories:**
- As a user, I can create goals with clear timeframes
- As a user, I can update goal progress and status
- As a user, I can view all goals filtered by area or timeframe

### 5.2 Habits System
**Types:** Gain a good habit, Lose a bad habit
**Attributes:**
- Habit name and description
- Type (gain/lose)
- Frequency description (text field: "daily", "3x/week", etc.)
- Streak counter (increments on check-in)
- Last check-in date
- Associated life area(s)

**User Stories:**
- As a user, I can create habits I want to build or break
- As a user, I can check in on habits and see my streak grow
- As a user, I can reset streaks when I break a habit

### 5.3 Tasks/Todo System
**Statuses:** Todo, Doing, Done
**Attributes:**
- Title and description
- Status (dropdown)
- Due date (optional)
- Priority (Low, Medium, High)
- Associated life area
- Optional contact reference

**User Stories:**
- As a user, I can create tasks with due dates and priorities
- As a user, I can move tasks through todo/doing/done statuses
- As a user, I can filter tasks by area or status

### 5.4 Contacts System
**Attributes:**
- Name
- Role/relationship
- Contact channels (phone, email, address, etc.)
- Birthday (optional)
- Associated life area(s)
- Notes

**User Stories:**
- As a user, I can add contacts with multiple communication channels
- As a user, I can link contacts to relevant life areas
- As a user, I can see all contacts for a specific area (e.g., all doctors)

### 5.5 References System
**Types:** Websites, Scriptures, Laws, Notes
**Attributes:**
- Title
- Type (dropdown)
- URL or text content
- Associated life area(s)
- Tags for filtering

**User Stories:**
- As a user, I can save useful websites organized by life area
- As a user, I can store scripture references and legal citations
- As a user, I can quickly access references when working in an area

### 5.6 AI-Generated Content
**Content Types:**
- Bible verses / inspirational quotes
- Area-specific insights
- Goal suggestions
- Habit recommendations

**MVP Implementation:**
- Stub functions return deterministic placeholders
- Clear function signatures for future API integration
- Cache generated content to minimize future API calls

**User Stories:**
- As a user, I receive inspirational Bible verses for each life area
- As a user, I see AI-generated insights when I open an area
- As a user, I understand that AI features are planned enhancements

---

## 6. User Workflows

### 6.1 First-Time User Setup
1. User runs app locally via `uvicorn` or Docker
2. User navigates to app (http://localhost:8000)
3. User creates account (username + password)
4. User sees dashboard with 8 life areas
5. User clicks an area to begin adding content

### 6.2 Daily Check-In Workflow
1. User logs in
2. User sees dashboard with area summaries
3. User checks off daily habits (streaks increment)
4. User reviews today's tasks across all areas
5. User updates task statuses (todo → doing → done)
6. User reads AI-generated inspirational content

### 6.3 Goal Setting Workflow
1. User navigates to specific life area (e.g., Physical/Health)
2. User clicks "Add Goal"
3. User fills in goal details (title, timeframe, due date)
4. User sets initial progress (0%)
5. System displays goal in area view
6. User periodically updates progress percentage

### 6.4 Birthday Reminder Workflow
1. User adds family/friends with birthdays
2. System auto-calculates age (Years, Months, Days)
3. User views upcoming birthdays dashboard
4. User sets reminder tasks for gift planning
5. User tracks communication in contact notes

### 6.5 Relationship Conflict Resolution Workflow (One-on-One)
1. User navigates to One-on-One area
2. User documents 3 main argument topics
3. User adds resolution strategies for each topic
4. User sets goals related to improving communication
5. User tracks progress and notes improvements over time

---

## 7. Non-Functional Requirements

### 7.1 Performance
- API response times < 500ms (95th percentile)
- Database queries optimized with indexes
- Minimal frontend JavaScript for fast load times

### 7.2 Security & Privacy
- Passwords hashed with bcrypt (cost factor 12)
- Session cookies signed and HTTP-only
- No data leaves local machine (privacy-first)
- SQL injection prevention via parameterized queries
- Basic input validation on all endpoints

### 7.3 Reliability
- Graceful error handling with user-friendly messages
- Database transactions for data integrity
- Automated tests for critical paths
- Data backup recommendations in README

### 7.4 Usability
- Consistent UI patterns across all areas
- Clear navigation with breadcrumbs
- Responsive design (desktop-first, mobile-friendly)
- Helpful error messages and validation feedback

### 7.5 Maintainability
- Modular code structure (routers, models, schemas separated)
- Type hints throughout Python codebase
- Clear comments for complex logic
- Alembic migrations for schema changes
- Comprehensive README for onboarding

---

## 8. Out of Scope (Post-MVP)

### Explicitly NOT in MVP:
- Frontend UI implementation (API-only MVP)
- Real AI integration (stubs only)
- Email notifications
- OAuth/social login
- Multi-user/family sharing
- Mobile native apps
- Cloud deployment
- Data export/import (beyond seed data)
- Reminders/notifications system
- Calendar integration
- File/photo uploads
- Rich text editing
- Search functionality (basic filtering only)
- Analytics/reporting dashboards

### Planned for Future Releases:
- Phase 2: Frontend (React/Vue/Svelte)
- Phase 3: Real AI integration (OpenAI, Anthropic, or local LLM)
- Phase 4: Email reminders and notifications
- Phase 5: Mobile apps (React Native or PWA)
- Phase 6: Family sharing and multi-user support

---

## 9. Acceptance Criteria

### Must-Have (MVP Blockers):
✅ All 8 life areas have dedicated endpoints
✅ Users can CRUD goals, habits, tasks, contacts, references
✅ Health catalogs (doctors, foods, supplements, meds, motion) are manageable
✅ Birthday age calculation works correctly (Y, M, D)
✅ AI stub endpoints return consistent placeholder content
✅ Authentication works (register, login, logout)
✅ SQLite database persists data across restarts
✅ Alembic migrations can be run
✅ Core pytest tests pass
✅ Seed data loads successfully
✅ README provides clear setup instructions

### Should-Have (High Priority):
✅ Task status transitions (todo → doing → done)
✅ Habit streak counters increment correctly
✅ Goal progress updates (0-100%)
✅ Contact linking to other entities
✅ Reference tagging and filtering
✅ One-on-One: 3 conflict topics tracked
✅ Politics: Federal/State/Local law categorization

### Nice-to-Have (Optional Enhancements):
- API rate limiting
- Request logging
- Performance monitoring
- Automated database backups
- Data export endpoints

---

## 10. Dependencies & Constraints

### Technical Dependencies:
- Python 3.11+
- FastAPI 0.104+
- SQLModel 0.14+
- SQLAlchemy 2.x
- Alembic
- Pydantic v2
- Uvicorn
- Pytest
- Bcrypt
- Python-dotenv

### Constraints:
- Must use SQLite (no PostgreSQL, MySQL, etc.)
- Must store database in `/data/app.sqlite3`
- No external APIs for AI (stubs only)
- No email service integration
- Local deployment only (no cloud infrastructure)
- Minimal dependencies (avoid bloat)

### Assumptions:
- Users are technical enough to run `uvicorn` or Docker
- Users have Python 3.11+ installed
- Users are comfortable with command-line tools
- Single-user deployment per instance

---

## 11. Release Plan

### MVP Release (v1.0)
**Timeline:** 2-3 weeks
**Deliverables:** All 23 files per spec
**Testing:** Core pytest suite passing
**Documentation:** Complete setup and usage guide

### Post-MVP Roadmap:
- **v1.1** - Frontend UI (choose framework)
- **v1.2** - Real AI integration
- **v2.0** - Multi-user support and family sharing
- **v2.1** - Mobile PWA
- **v3.0** - Advanced analytics and insights

---

## 12. Risks & Mitigations

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| SQLite performance at scale | Medium | Low | Indexes, query optimization, consider PostgreSQL for v2 |
| AI stub confusion | Low | Medium | Clear documentation that AI is placeholder |
| Users expect frontend | Medium | High | Clarify API-first approach in README |
| Data loss (no backups) | High | Medium | Document backup procedures, add export endpoint post-MVP |
| Security vulnerabilities | High | Low | Follow OWASP best practices, regular dependency updates |

---

## 13. Appendix

### Glossary:
- **Life Area:** One of 8 core life dimensions (Health, Hobby, Income/Expenses, etc.)
- **Streak:** Consecutive days a habit has been checked in
- **Timeframe:** Goal duration (Short: <3mo, Medium: 3-12mo, Long: 12mo+)
- **Reference:** Saved resource (website, scripture, law, note)
- **Health Catalog:** Structured list of health-related items (doctors, foods, etc.)

### Related Documents:
- [Architecture.md](Architecture.md) - System design
- [API-Schema.md](API-Schema.md) - Endpoint specifications
- [Data-Model.md](Data-Model.md) - Database schema
- [UX-Wireframes.md](UX-Wireframes.md) - UI mockups
- [Acceptance-Tests.md](Acceptance-Tests.md) - Test scenarios
