You are a Senior PM + Tech Lead. Produce a build-ready MVP spec for an AI-assisted life-management web app, using a SINGLE lightweight backend with SQLite stored in-repo. Use the CSV-like source below to define features.

======================
SOURCE CSV-LIKE SPEC
(HOBBY, INCOME, ASSETS, EXPENSES, LIABILITIES, FAMILY & FRIENDS, ONE on ONE, POLITICS, SPIRITUAL)

HOBBY | INCOME | ASSETS
- Bible verse - ai (per-area inspirational text, AI-generated)
- Goals - drop down (Short / Medium / Long term)
- To Do List - drop down
- Goals — something your hands help to make (Hobby-specific)
- Contacts / websites dropdown
- Gain a good habit / Lose a bad habit
- Doctor's — drop down (global health)
- Food — drop down (global)
- Vitamins / Supplements — drop down (global)
- Medications — drop down (global)
- Motion (Walk/Run/Yoga) — drop down (global)

ASSETS adds:
- Banking
- Contacts / websites dropdown

EXPENSES | LIABILITIES
- List — Drop down
- Contacts / websites dropdown

FAMILY & FRIENDS | ONE on ONE | POLITICS | SPIRITUAL
- Bible verse — ai
- Goals - drop down (Short / Medium / Long)
- Birthday list with DoB + age (Y,M,D)
- also contact info
- Identify 3 main topics of argument & fix (One-on-One)
- Federal / State / Local Laws (Politics references)
- Contacts / websites dropdown
- Gain a good habit / Lose a bad habit
======================

## MVP CONSTRAINTS (MANDATORY)
- **Database:** SQLite file stored in-repo at `/data/app.sqlite3` (checked in for demo; ignore via .gitignore optional). No external DBs.
- **Backend:** Python **FastAPI** + SQLModel (or SQLAlchemy 2.x) for models. Minimal dependencies only.
- **Auth:** Simple username/password (bcrypt) + signed cookie sessions (Starlette). No OAuth, no emails.
- **AI:** Stub endpoints that return deterministic placeholders; leave a clearly marked function to swap in provider later.
- **Deploy:** Run locally via `uvicorn` and optional Dockerfile; no cloud infra.
- **Migrations:** Alembic included, but MVP may use `create_all()` initially. Provide a “how to migrate later” section.
- **Tests:** A few high-signal API tests (pytest) for core flows only.
- **Privacy/Safety:** Basic PII notes; no real secrets beyond a `.env` app secret.

## NORMALIZED LIFE AREAS (for data model)
1) Physical/Health (global health catalogs: doctors, foods, supplements, meds, motion)
2) Hobby
3) Income & Expenses
4) Assets & Liabilities
5) One-on-One Relationship
6) Family & Friends
7) Politics/Civics
8) Spiritual

## DELIVERABLES (GENERATE THESE FILES)
1) /docs/PRD.md
2) /docs/Architecture.md
3) /docs/API-Schema.md
4) /docs/Data-Model.md
5) /docs/UX-Wireframes.md
6) /docs/Acceptance-Tests.md
7) /docs/Prompts.md
8) /docs/Implementation-Plan.md
9) /docs/Security-Privacy.md
10) /seed/sample.csv (normalized)
11) /seed/fixtures.json
12) /server/app/main.py (FastAPI app)
13) /server/app/models.py (SQLModel models)
14) /server/app/schemas.py (pydantic I/O)
15) /server/app/db.py (SQLite engine + session)
16) /server/app/auth.py (bcrypt + cookie session)
17) /server/app/routers/*.py (areas, entries, goals, habits, tasks, contacts, references, health, finance, ai)
18) /server/app/ai_stub.py (returns static “bible verse” + “insight” placeholders)
19) /server/alembic.ini + /server/migrations/ (init + first migration)
20) /server/tests/test_core.py (pytest)
21) /server/.env.example (APP_SECRET=…)
22) /Dockerfile + /Makefile
23) /README.md (setup, run, seed, tests)

## SCOPE & FEATURES (MVP)
- **Entries**: free-text with area tags.
- **Goals**: short/medium/long; status; due; simple % progress.
- **Habits**: gain/lose; frequency text field; streak counter on check-in.
- **Tasks**: todo/doing/done; due date; optional contact ref.
- **Contacts**: name, role, channels; link to areas.
- **References**: websites, scriptures, laws (federal/state/local), notes.
- **Health Catalogs**: doctors, foods, supplements, meds, motion; linkable from any area.
- **Birthdays**: compute age Y,M,D server-side at re
