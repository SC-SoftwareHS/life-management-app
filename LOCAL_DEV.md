# Local Development Guide

## Quick Start

Your local server is already running! 🎉

**Local URL:** http://localhost:8000/static/index.html

---

## Server Status

The server is running with:
- **Port:** 8000
- **Auto-reload:** Enabled (watches for file changes)
- **Database:** SQLite at `data/app.sqlite3`

**Server Process ID:** 81595 (if you need to kill it: `kill 81595`)

---

## How to Work Locally

### 1. Make Code Changes

Edit any file in:
- `frontend/js/*.js` - JavaScript modules
- `frontend/css/styles.css` - Styling
- `frontend/index.html` - HTML structure
- `server/app/*.py` - Backend Python code
- `server/app/routers/*.py` - API endpoints

### 2. See Changes Immediately

**Frontend changes (HTML/CSS/JS):**
- Just refresh your browser (F5 or Cmd+R)
- Or hard refresh to clear cache (Ctrl+Shift+R or Cmd+Shift+R)

**Backend changes (Python):**
- Server auto-reloads automatically (--reload flag)
- Watch terminal for "Application startup complete"
- No need to restart manually!

### 3. Test Your Changes

Open: http://localhost:8000/static/index.html

---

## Common Tasks

### View Server Logs

The server is running in the background. To see logs:

```bash
# Find the process
ps aux | grep uvicorn

# Or check if it's responding
curl http://localhost:8000/health
```

### Restart Server

```bash
# Kill existing server
kill 81595  # Use the actual PID

# Start fresh
cd "/Users/harrison/Documents/Project for Joe"
source venv/bin/activate
uvicorn server.app.main:app --reload --port 8000
```

### Check API Endpoints

**Swagger UI:** http://localhost:8000/docs
**ReDoc:** http://localhost:8000/redoc

### View Database

```bash
# Open SQLite database
sqlite3 data/app.sqlite3

# Common queries:
sqlite> SELECT * FROM user;
sqlite> SELECT * FROM goal;
sqlite> .tables  # List all tables
sqlite> .exit    # Exit SQLite
```

### Create Test User via API

```bash
# Register
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"testlocal","email":"test@local.com","full_name":"Test Local","password":"testpass123"}'

# Login
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"testlocal","password":"testpass123"}' \
  -c cookies.txt

# Create a goal
curl -X POST http://localhost:8000/api/goals/ \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{"title":"Test Goal","description":"This is a test","timeframe":"short","target_date":"2025-12-31","area_ids":[1]}'
```

---

## Current Working Changes

### ✅ Just Fixed:

1. **Added `backToDashboard()` function** in `dashboard.js`
   - Now the "← Back to Dashboard" button works!

2. **Goals view loads real data** from API
   - Shows empty state or goal cards

3. **Navigation buttons added** to all views

### 🧪 Test These Now:

1. Go to http://localhost:8000/static/index.html
2. Login/register
3. Click a life area card
4. Click "← Back to Dashboard"
5. Should return to main view! ✅

---

## Rapid Iteration Workflow

### Example: Adding a Feature

```bash
# 1. Edit the file (example: add console.log to dashboard.js)
nano frontend/js/dashboard.js
# or use VS Code: code frontend/js/dashboard.js

# 2. Save the file (Cmd+S or Ctrl+S)

# 3. Refresh browser (F5)

# 4. Check browser console (F12 → Console tab)

# 5. See your changes instantly!
```

### Example: Testing Backend Changes

```bash
# 1. Edit a router
nano server/app/routers/goals.py

# 2. Save the file

# 3. Watch terminal - server auto-reloads:
#    "INFO:     Application startup complete."

# 4. Test the endpoint
curl http://localhost:8000/api/goals/ -b cookies.txt

# 5. Changes are live!
```

---

## Browser Developer Tools

### Open DevTools
- **Mac:** Cmd + Option + I
- **Windows/Linux:** F12 or Ctrl + Shift + I

### Useful Tabs:

**Console:**
- See JavaScript errors
- Test code: `Dashboard.backToDashboard()`
- View logged data

**Network:**
- See all API calls
- Check request/response
- Debug "Failed to fetch" errors

**Elements:**
- Inspect HTML structure
- See applied CSS
- Test CSS changes live

**Application:**
- View cookies
- Check session data
- Clear storage

---

## Debugging Tips

### JavaScript Not Working?

1. **Check Console for errors** (F12 → Console)
2. **Hard refresh** to clear cache (Ctrl+Shift+R)
3. **Verify file saved** (check file timestamp)
4. **Check syntax** (look for red underlines in editor)

### API Calls Failing?

1. **Check Network tab** (F12 → Network → XHR)
2. **Look at response** (click request → Preview tab)
3. **Check server logs** in terminal
4. **Verify you're logged in** (check cookies in Application tab)

### Back Button Still Not Working?

1. **Open Console** (F12)
2. **Click the back button**
3. **Type:** `Dashboard.backToDashboard()`
4. **If error:** Function not defined → file didn't reload
5. **If works:** Button click handler issue

### CSS Not Applying?

1. **Hard refresh** (Ctrl+Shift+R)
2. **Check Elements tab** (F12 → Elements)
3. **Click element** and see applied styles
4. **Verify class names match** between HTML and CSS

---

## Git Workflow (When You're Happy with Changes)

```bash
# 1. See what changed
git status

# 2. Stage changes
git add frontend/js/dashboard.js

# 3. Commit
git commit -m "Fix back button functionality"

# 4. Push to Railway (auto-deploys)
git push origin main

# 5. Wait ~90 seconds for Railway to rebuild
```

---

## Common Issues & Solutions

### Server won't start - "Address already in use"

```bash
# Find and kill the existing server
lsof -ti:8000 | xargs kill
# Or: kill 81595

# Start fresh
uvicorn server.app.main:app --reload --port 8000
```

### Changes not showing up

```bash
# Hard refresh browser
Ctrl+Shift+R (Windows/Linux)
Cmd+Shift+R (Mac)

# Or open in incognito window
```

### Database errors

```bash
# Reset database (WARNING: deletes all data!)
rm data/app.sqlite3

# Restart server (will recreate tables)
# Re-register user
```

### Import errors in Python

```bash
# Make sure venv is activated
source venv/bin/activate

# Check requirements installed
pip list | grep fastapi
```

---

## Quick Reference

### URLs
- **Frontend:** http://localhost:8000/static/index.html
- **API Docs:** http://localhost:8000/docs
- **Health Check:** http://localhost:8000/health

### Files to Edit Often
- **Dashboard:** `frontend/js/dashboard.js`
- **Goals:** `frontend/js/goals.js`
- **Styles:** `frontend/css/styles.css`
- **Goals API:** `server/app/routers/goals.py`

### Useful Commands
```bash
# Restart server
kill $(lsof -ti:8000) && uvicorn server.app.main:app --reload --port 8000

# View logs
tail -f logs/app.log  # if you add logging

# Test endpoint
curl http://localhost:8000/api/goals/ -H "Cookie: session_id=..."
```

---

## Next Steps

### 1. Test the Back Button Fix
- Open http://localhost:8000/static/index.html
- Login
- Click a life area
- Click "← Back to Dashboard"
- Should work now! ✅

### 2. Try Making a Small Change
- Edit `dashboard.js`
- Add `console.log('Back button clicked!')` in `backToDashboard()`
- Refresh browser
- Click back button
- Check console (F12)

### 3. Explore the Code
- Read through `frontend/js/` files
- Check out `server/app/routers/` endpoints
- Look at `docs/` for specifications

---

**You're all set for rapid local development!** 🚀

Make changes → Save → Refresh → Test → Repeat!

Any issues? Check the browser console first (F12 → Console).
