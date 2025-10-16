# AI-Assisted Life Management Application

A comprehensive, privacy-first life management system that helps users organize and improve all aspects of their lives across 8 core areas: Physical/Health, Hobby, Income/Expenses, Assets/Liabilities, One-on-One Relationship, Family/Friends, Politics/Civics, and Spiritual.

## 🌟 Features

### 8 Life Areas
- **💪 Physical/Health** - Track doctors, medications, supplements, food, and motion activities
- **🎨 Hobby** - Manage creative projects and personal interests
- **💰 Income & Expenses** - Monitor cash flow and spending
- **🏦 Assets & Liabilities** - Track wealth, accounts, and debts
- **💑 One-on-One Relationship** - Strengthen partnerships with conflict resolution tracking
- **👨‍👩‍👧‍👦 Family & Friends** - Nurture connections with birthday reminders and contact management
- **🗳️ Politics/Civics** - Engage with government through law references and civic goals
- **🙏 Spiritual** - Deepen faith with scripture, habits, and reflections

### Core Functionality
- ✅ **Goals System** - Short/Medium/Long term goals with progress tracking (0-100%)
- ✅ **Habits Tracker** - Build good habits, break bad ones with streak counters
- ✅ **Task Management** - Todo/Doing/Done workflow with priorities and due dates
- ✅ **Contacts** - Store people with automatic birthday age calculation (Years/Months/Days)
- ✅ **References** - Save websites, scriptures, laws organized by area
- ✅ **Health Catalog** - Manage doctors, foods, supplements, medications, motion activities
- ✅ **Financial Tracking** - Banking accounts, assets, liabilities with balances
- ✅ **Conflict Resolution** - Track 3 main argument topics with resolution strategies (One-on-One)
- ✅ **Journal Entries** - Free-text reflections per life area
- ✅ **AI Content** - Inspirational Bible verses and insights (stubbed for MVP, ready for real AI)

## 🏗️ Architecture

### Tech Stack
- **Backend:** FastAPI (Python 3.11+)
- **Database:** SQLite with SQLModel ORM
- **Migrations:** Alembic
- **Auth:** Bcrypt password hashing + session cookies
- **Testing:** Pytest
- **API Docs:** Auto-generated Swagger/OpenAPI at `/docs`

### Privacy-First Design
- 🔒 All data stored locally in SQLite file
- 🔒 No external API calls (AI is stubbed in MVP)
- 🔒 Single-user deployment per instance
- 🔒 Bcrypt password hashing (cost factor 12)
- 🔒 HTTP-only session cookies

## 📚 Documentation

Complete documentation available in [/docs](docs/):

1. **[PRD.md](docs/PRD.md)** - Product Requirements Document with user stories
2. **[Architecture.md](docs/Architecture.md)** - System design and technical decisions
3. **[API-Schema.md](docs/API-Schema.md)** - Complete REST API specification
4. **[Data-Model.md](docs/Data-Model.md)** - SQLModel database schema
5. **[UX-Wireframes.md](docs/UX-Wireframes.md)** - UI mockups for future frontend
6. **[Acceptance-Tests.md](docs/Acceptance-Tests.md)** - Test scenarios
7. **[Prompts.md](docs/Prompts.md)** - AI prompt templates
8. **[Implementation-Plan.md](docs/Implementation-Plan.md)** - 14-day build schedule
9. **[Security-Privacy.md](docs/Security-Privacy.md)** - Security best practices

## 🚀 Quick Start

### Prerequisites
- Python 3.11 or higher
- pip (Python package manager)
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd "Project for Joe"
   ```

2. **Set up Python virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r server/requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   cp server/.env.example server/.env
   # Edit server/.env and set a strong APP_SECRET
   ```

5. **Set up database** (Implementation files to be added)
   ```bash
   cd server
   # Run migrations when implementation is complete:
   # alembic upgrade head
   ```

6. **Seed sample data** (Optional)
   ```bash
   # Seed script to be implemented - loads data from seed/fixtures.json
   # python seed_db.py
   ```

7. **Run the application**
   ```bash
   cd server
   uvicorn app.main:app --reload --port 8000
   ```

8. **Access the API**
   - API Base: http://localhost:8000/api
   - Swagger Docs: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

## 📦 Project Structure

```
/
├── docs/                    # Complete documentation (9 files)
├── seed/                    # Sample data for testing
│   ├── sample.csv          # Normalized CSV data
│   └── fixtures.json       # Structured JSON fixtures
├── server/                  # FastAPI application (to be implemented)
│   ├── app/
│   │   ├── main.py         # App entry point
│   │   ├── db.py           # Database connection
│   │   ├── models.py       # SQLModel models
│   │   ├── schemas.py      # Pydantic schemas
│   │   ├── auth.py         # Authentication
│   │   ├── ai_stub.py      # AI placeholders
│   │   └── routers/        # API endpoints
│   ├── tests/              # Pytest test suite
│   ├── migrations/         # Alembic migrations
│   ├── requirements.txt    # Python dependencies
│   └── .env.example        # Environment template
├── data/                    # SQLite database storage
├── Dockerfile              # Container build (to be added)
├── Makefile                # Common commands (to be added)
└── README.md               # This file
```

## 🧪 Testing

```bash
cd server
pytest -v
```

## 🐳 Docker (Future)

```bash
docker build -t life-mgmt-app .
docker run -p 8000:8000 -v $(pwd)/data:/app/data life-mgmt-app
```

## 📊 Sample Data

The `/seed` directory contains comprehensive sample data:
- **sample.csv** - Normalized data covering all 8 life areas
- **fixtures.json** - Complete structured dataset including:
  - 1 test user (username: `test_user`, password: `testpass123`)
  - All 8 life areas
  - 9 goals across different areas
  - 7 habits with streaks
  - 7 contacts including doctors, family, friends
  - 6 tasks in various states
  - 5 references (websites, laws, scriptures)
  - 5 health catalog items
  - 6 financial accounts
  - 3 conflict resolution topics
  - 4 journal entries

## 🔐 Security

- **Passwords:** Bcrypt hashing (cost factor 12)
- **Sessions:** Signed HTTP-only cookies
- **SQL Injection:** Protected via SQLAlchemy ORM
- **Input Validation:** Pydantic schemas validate all inputs
- **Privacy:** All data stays local, no telemetry

See [docs/Security-Privacy.md](docs/Security-Privacy.md) for complete security documentation.

## 🗺️ Roadmap

### MVP (Current) - API-First Backend
- ✅ Complete documentation (9 files)
- ✅ Data model specifications
- ✅ API schema definitions
- ✅ Seed data
- 🚧 FastAPI implementation (in progress)
- 🚧 Alembic migrations
- 🚧 Pytest test suite

### Phase 2 - Frontend
- React/Vue/Svelte UI
- All wireframes implemented
- Mobile-responsive design

### Phase 3 - Real AI Integration
- OpenAI/Anthropic/Local LLM
- Dynamic Bible verses and insights
- Goal and habit suggestions

### Phase 4 - Advanced Features
- Email notifications
- Calendar integration
- Data export/import
- Search functionality
- Analytics dashboards

### Phase 5 - Multi-User
- PostgreSQL migration
- Family/team sharing
- Permission system

## 🤝 Contributing

This is currently a personal project. If you'd like to contribute:
1. Fork the repository
2. Create a feature branch
3. Follow the implementation plan in [docs/Implementation-Plan.md](docs/Implementation-Plan.md)
4. Submit a pull request

## 📝 License

[Specify your license - MIT, Apache 2.0, etc.]

## 🙏 Acknowledgments

Built following best practices from:
- FastAPI documentation
- SQLModel documentation
- OWASP security guidelines

## 📧 Contact

For questions or feedback, please open an issue on GitHub.

---

## Implementation Status

**Phase 1: Documentation & Specifications** ✅ **COMPLETE**
- All 9 documentation files created
- Complete data model defined
- API schema fully specified
- Sample data prepared

**Phase 2: Backend Implementation** 🚧 **IN PROGRESS**
- Core files to be implemented using documentation as reference
- Follow [docs/Implementation-Plan.md](docs/Implementation-Plan.md) for build schedule

**Estimated Time to MVP:** 2-3 weeks following the implementation plan

---

**Note:** This project currently contains complete specifications and documentation. The actual FastAPI implementation files (models, routers, tests) should be created following the detailed specifications in the `/docs` folder.
