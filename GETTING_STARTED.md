# Getting Started with Life Management App

## Quick Start

Your Life Management application is now **fully functional**! 🎉

### 1. Start the Server

```bash
cd "/Users/harrison/Documents/Project for Joe"
source venv/bin/activate
uvicorn server.app.main:app --port 8000
```

### 2. Open the Application

**Open in your browser:**
- Frontend: http://localhost:8000/static/index.html
- API Docs: http://localhost:8000/docs (Swagger UI)
- API Redoc: http://localhost:8000/redoc

### 3. Create an Account

1. Go to http://localhost:8000/static/index.html
2. Click "Register"
3. Fill in:
   - Username (min 3 characters)
   - Email
   - Full Name
   - Password (min 8 characters)
4. Click "Register" button
5. You'll be automatically logged in!

### 4. Explore Your Dashboard

After logging in, you'll see 8 life area cards:
- 💪 Physical/Health
- 🎨 Hobby
- 💰 Income & Expenses
- 🏦 Assets & Liabilities
- 💑 One-on-One Relationship
- 👨‍👩‍👧‍👦 Family & Friends
- 🗳️ Politics
- 🙏 Spiritual

Click any card to explore that life area!

## What's Working

### ✅ Backend API (100% Complete)
- **12 Routers** with 50+ endpoints
- **Authentication**: Register, login, logout, session management
- **Life Areas**: All 8 areas defined
- **Goals**: Full CRUD + progress tracking + area linking
- **Habits**: Full CRUD + check-in with streak calculation
- **Tasks**: Full CRUD with todo/doing/done workflow
- **Contacts**: Full CRUD + birthday age calculation
- **References**: Full CRUD (websites, scriptures, laws)
- **Health Catalog**: Full CRUD (doctors, foods, supplements, medications, motion)
- **Finance**: Full CRUD + net worth calculation
- **Entries**: Full CRUD (journal entries)
- **One-on-One**: Full CRUD (max 3 conflict topics)
- **AI Content**: Bible verses and insights (stubbed)

### ✅ Frontend Web App (MVP Complete)
- **Authentication UI**: Beautiful login/register forms
- **Dashboard**: 8 life area cards with icons
- **Modern Design**: Clean, responsive, professional
- **Toast Notifications**: User feedback
- **Modal System**: For forms and dialogs
- **Loading States**: Spinner during API calls

### 🚧 Feature UIs (Coming Soon)
The backend is ready, but the frontend feature UIs are placeholders:
- Goals management UI
- Habits check-in UI
- Tasks kanban board
- Contacts with birthdays
- And more...

## Development

### Run in Development Mode (Auto-reload)
```bash
cd "/Users/harrison/Documents/Project for Joe"
source venv/bin/activate
uvicorn server.app.main:app --reload --port 8000
```

### Access API Documentation
- **Swagger UI**: http://localhost:8000/docs
  - Interactive API testing
  - Try out all endpoints
  - See request/response schemas

- **ReDoc**: http://localhost:8000/redoc
  - Beautiful API documentation
  - Search functionality

### Project Structure
```
Project for Joe/
├── frontend/              # Web frontend
│   ├── index.html        # Main HTML file
│   ├── css/
│   │   └── styles.css    # Modern CSS
│   └── js/
│       ├── api.js        # API client
│       ├── auth.js       # Authentication
│       ├── dashboard.js  # Dashboard
│       └── app.js        # Main app
├── server/               # FastAPI backend
│   ├── app/
│   │   ├── main.py      # App entry point
│   │   ├── models.py    # Database models (12+ tables)
│   │   ├── schemas.py   # Request/response schemas
│   │   ├── auth.py      # Authentication logic
│   │   ├── db.py        # Database connection
│   │   └── routers/     # API endpoints (12 routers)
│   └── data/
│       └── app.sqlite3  # SQLite database
├── docs/                 # Documentation (9 files)
└── seed/                 # Sample data

```

## Database

**Location**: `/Users/harrison/Documents/Project for Joe/data/app.sqlite3`

**Tables** (12+):
- users
- lifeareas
- goals, goal_area_links
- habits, habit_area_links
- tasks
- contacts, contact_area_links
- references, reference_area_links
- healthcatalogitems
- financialaccounts
- entries
- conflicttopics

**View Data**: Use any SQLite browser or:
```bash
sqlite3 data/app.sqlite3
.tables
SELECT * FROM users;
```

## API Examples

### Register a User
```bash
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john",
    "email": "john@example.com",
    "password": "password123",
    "full_name": "John Doe"
  }'
```

### Login
```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -c cookies.txt \
  -d '{
    "username": "john",
    "password": "password123"
  }'
```

### Get Life Areas
```bash
curl http://localhost:8000/api/areas/ \
  -b cookies.txt
```

### Create a Goal
```bash
curl -X POST http://localhost:8000/api/goals/ \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{
    "name": "Run a marathon",
    "timeframe": "long",
    "area_ids": [1],
    "status": "active",
    "progress_percentage": 0
  }'
```

## Technology Stack

### Backend
- **FastAPI**: Modern Python web framework
- **SQLModel**: Type-safe ORM (SQLAlchemy + Pydantic)
- **SQLite**: File-based database
- **Bcrypt**: Password hashing
- **Starlette Sessions**: Session-based auth

### Frontend
- **Vanilla JavaScript** (ES6+)
- **Modern CSS** (Grid, Flexbox, Custom Properties)
- **Fetch API**: HTTP requests
- **No build tools**: Works immediately!

## Next Steps

### To Complete Feature UIs:
1. Implement Goals CRUD interface
2. Implement Habits with check-in button
3. Implement Tasks kanban board (drag & drop)
4. Implement Contacts list with birthday countdown
5. Implement References, Health, Finance, Entries UIs

### To Deploy:
1. Set up production database (PostgreSQL recommended)
2. Configure HTTPS
3. Set `https_only=True` in session middleware
4. Deploy to VPS, Heroku, or AWS

### To Enhance:
1. Add real AI integration (OpenAI API)
2. Implement Alembic migrations
3. Write pytest test suite
4. Add data export/import
5. Build mobile app (React Native)

## Troubleshooting

### Port 8000 Already in Use
```bash
lsof -ti:8000 | xargs kill -9
```

### Database Locked
```bash
# Close any SQLite browsers
# Restart the server
```

### CORS Errors
The backend allows localhost:3000 and localhost:5173 by default.
Frontend served from same origin (localhost:8000) doesn't need CORS.

## Support

- **GitHub**: https://github.com/SC-SoftwareHS/life-management-app
- **Documentation**: See `/docs` folder for detailed specs
- **API Docs**: http://localhost:8000/docs (while server running)

---

🤖 Built with Claude Code
Last Updated: 2025-10-17
