# API Schema Documentation
## AI-Assisted Life Management Application

**Version:** 1.0 MVP
**Base URL:** `http://localhost:8000/api`
**Content-Type:** `application/json`

---

## Authentication Endpoints

### POST /auth/register
Register a new user account.

**Request:**
```json
{
  "username": "string (required, 3-50 chars)",
  "password": "string (required, min 8 chars)",
  "email": "string (optional)",
  "full_name": "string (optional)"
}
```

**Response 201:**
```json
{
  "data": {
    "id": 1,
    "username": "holistic_hannah",
    "email": "hannah@example.com",
    "full_name": "Hannah Smith",
    "created_at": "2025-10-16T10:30:00Z"
  },
  "message": "User registered successfully"
}
```

---

### POST /auth/login
Login and create session.

**Request:**
```json
{
  "username": "string (required)",
  "password": "string (required)"
}
```

**Response 200:**
```json
{
  "data": {
    "user_id": 1,
    "username": "holistic_hannah"
  },
  "message": "Login successful"
}
```
Sets HTTP-only session cookie.

---

### POST /auth/logout
Destroy session.

**Response 200:**
```json
{
  "message": "Logged out successfully"
}
```

---

### GET /auth/me
Get current user info.

**Response 200:**
```json
{
  "data": {
    "id": 1,
    "username": "holistic_hannah",
    "email": "hannah@example.com",
    "full_name": "Hannah Smith"
  }
}
```

---

## Life Areas Endpoints

### GET /areas
List all 8 predefined life areas.

**Response 200:**
```json
{
  "data": [
    {
      "id": 1,
      "name": "physical_health",
      "display_name": "Physical/Health",
      "description": "Optimize physical wellbeing",
      "icon": "💪"
    },
    ...
  ]
}
```

---

## Goals Endpoints

### GET /goals
List user's goals with optional filters.

**Query Parameters:**
- `area_id` (int, optional)
- `timeframe` (short|medium|long, optional)
- `status` (not_started|in_progress|completed|abandoned, optional)

**Response 200:**
```json
{
  "data": [
    {
      "id": 1,
      "title": "Run 5K in under 30 minutes",
      "description": "Build up to 5K running capability",
      "timeframe": "short",
      "status": "in_progress",
      "progress_percentage": 45,
      "due_date": "2025-12-31",
      "areas": [
        {"id": 1, "name": "physical_health", "display_name": "Physical/Health"}
      ],
      "contact": null,
      "created_at": "2025-09-01T08:00:00Z",
      "updated_at": "2025-10-15T14:22:00Z"
    }
  ]
}
```

---

### POST /goals
Create a new goal.

**Request:**
```json
{
  "title": "string (required, max 200 chars)",
  "description": "string (optional)",
  "timeframe": "short|medium|long (required)",
  "due_date": "YYYY-MM-DD (optional)",
  "area_ids": [1, 2] (required, array of ints),
  "contact_id": 5 (optional, int)
}
```

**Response 201:**
```json
{
  "data": {
    "id": 2,
    "title": "Learn Spanish",
    "timeframe": "medium",
    "status": "not_started",
    "progress_percentage": 0,
    ...
  },
  "message": "Goal created successfully"
}
```

---

### GET /goals/{id}
Get goal details.

**Response 200:** Same structure as individual goal in list.

---

### PUT /goals/{id}
Update goal.

**Request:**
```json
{
  "title": "string (optional)",
  "description": "string (optional)",
  "status": "not_started|in_progress|completed|abandoned (optional)",
  "progress_percentage": 0-100 (optional, int),
  "due_date": "YYYY-MM-DD (optional)",
  "area_ids": [1, 3] (optional),
  "contact_id": 7 (optional)
}
```

**Response 200:**
```json
{
  "data": { updated goal },
  "message": "Goal updated successfully"
}
```

---

### DELETE /goals/{id}
Delete goal.

**Response 204:** No content.

---

## Habits Endpoints

### GET /habits
List habits with optional filters.

**Query Parameters:**
- `area_id` (int, optional)
- `type` (gain|lose, optional)

**Response 200:**
```json
{
  "data": [
    {
      "id": 1,
      "name": "Morning meditation",
      "description": "10 minutes of mindfulness",
      "habit_type": "gain",
      "frequency_description": "daily",
      "current_streak": 12,
      "longest_streak": 30,
      "last_checkin_date": "2025-10-16",
      "areas": [
        {"id": 8, "name": "spiritual", "display_name": "Spiritual"}
      ],
      "created_at": "2025-08-01T06:00:00Z"
    }
  ]
}
```

---

### POST /habits
Create habit.

**Request:**
```json
{
  "name": "string (required, max 200 chars)",
  "description": "string (optional)",
  "habit_type": "gain|lose (required)",
  "frequency_description": "string (required, max 100 chars)",
  "area_ids": [8] (required, array)
}
```

**Response 201:** Created habit.

---

### POST /habits/{id}/checkin
Check in on habit (increments streak).

**Request:**
```json
{
  "checkin_date": "YYYY-MM-DD (optional, defaults to today)",
  "notes": "string (optional)"
}
```

**Response 200:**
```json
{
  "data": {
    "habit_id": 1,
    "current_streak": 13,
    "longest_streak": 30,
    "last_checkin_date": "2025-10-16"
  },
  "message": "Check-in recorded"
}
```

---

### PUT /habits/{id}
Update habit.

### DELETE /habits/{id}
Delete habit.

---

## Tasks Endpoints

### GET /tasks
List tasks with filters.

**Query Parameters:**
- `area_id` (int, optional)
- `status` (todo|doing|done, optional)
- `priority` (low|medium|high, optional)

**Response 200:**
```json
{
  "data": [
    {
      "id": 1,
      "title": "Schedule annual checkup",
      "description": "Call Dr. Johnson",
      "status": "todo",
      "priority": "high",
      "due_date": "2025-10-20",
      "area": {"id": 1, "display_name": "Physical/Health"},
      "contact": {"id": 5, "name": "Dr. Sarah Johnson"},
      "created_at": "2025-10-10T09:00:00Z"
    }
  ]
}
```

---

### POST /tasks
Create task.

**Request:**
```json
{
  "title": "string (required)",
  "description": "string (optional)",
  "area_id": 1 (required, int),
  "status": "todo|doing|done (optional, default: todo)",
  "priority": "low|medium|high (optional, default: medium)",
  "due_date": "YYYY-MM-DD (optional)",
  "contact_id": 5 (optional, int)
}
```

**Response 201:** Created task.

---

### PUT /tasks/{id}
Update task (including status transitions).

### DELETE /tasks/{id}
Delete task.

---

## Contacts Endpoints

### GET /contacts
List contacts with area filter.

**Query Parameters:**
- `area_id` (int, optional)

**Response 200:**
```json
{
  "data": [
    {
      "id": 1,
      "name": "Dr. Sarah Johnson",
      "role": "Primary Care Physician",
      "phone": "555-0123",
      "email": "sjohnson@clinic.com",
      "address": "123 Medical Plaza",
      "birthday": "1975-06-15",
      "notes": "Accepts Blue Cross insurance",
      "areas": [
        {"id": 1, "display_name": "Physical/Health"}
      ],
      "created_at": "2025-05-01T10:00:00Z"
    }
  ]
}
```

---

### GET /contacts/birthdays
Upcoming birthdays with age calculation.

**Query Parameters:**
- `days_ahead` (int, optional, default: 30)

**Response 200:**
```json
{
  "data": [
    {
      "contact_id": 3,
      "name": "Mom",
      "birthday": "1965-11-02",
      "age": {
        "years": 59,
        "months": 11,
        "days": 14
      },
      "days_until_birthday": 17
    }
  ]
}
```

---

### POST /contacts
Create contact.

### PUT /contacts/{id}
Update contact.

### DELETE /contacts/{id}
Delete contact.

---

## References Endpoints

### GET /references
List references with filters.

**Query Parameters:**
- `area_id` (int, optional)
- `type` (website|scripture|law|note, optional)
- `law_level` (federal|state|local, optional)

**Response 200:**
```json
{
  "data": [
    {
      "id": 1,
      "title": "Medicare.gov",
      "type": "website",
      "url": "https://medicare.gov",
      "content": null,
      "law_level": null,
      "tags": "insurance,healthcare",
      "areas": [{"id": 1, "display_name": "Physical/Health"}],
      "created_at": "2025-07-15T12:00:00Z"
    },
    {
      "id": 2,
      "title": "Affordable Care Act",
      "type": "law",
      "url": null,
      "content": "Summary of ACA provisions...",
      "law_level": "federal",
      "tags": "healthcare,insurance",
      "areas": [{"id": 1, "display_name": "Physical/Health"}, {"id": 7, "display_name": "Politics/Civics"}],
      "created_at": "2025-07-20T09:00:00Z"
    }
  ]
}
```

---

### POST /references
Create reference.

### PUT /references/{id}
Update reference.

### DELETE /references/{id}
Delete reference.

---

## Health Catalog Endpoints

### GET /health
List health catalog items.

**Query Parameters:**
- `catalog_type` (doctor|food|supplement|medication|motion, optional)

**Response 200:**
```json
{
  "data": [
    {
      "id": 1,
      "catalog_type": "supplement",
      "name": "Vitamin D3",
      "description": "Supports bone health",
      "supplement_dosage": "2000 IU",
      "frequency_description": "daily with breakfast",
      "notes": "Take with fatty meal for absorption",
      "created_at": "2025-06-01T08:00:00Z"
    },
    {
      "id": 2,
      "catalog_type": "motion",
      "name": "Morning yoga",
      "description": "Vinyasa flow routine",
      "motion_duration": "30 min",
      "frequency_description": "5x per week",
      "created_at": "2025-06-05T07:00:00Z"
    }
  ]
}
```

---

### POST /health
Create health catalog item.

### PUT /health/{id}
Update health catalog item.

### DELETE /health/{id}
Delete health catalog item.

---

## Finance Endpoints

### GET /finance
List financial accounts.

**Query Parameters:**
- `account_type` (banking|asset|liability, optional)

**Response 200:**
```json
{
  "data": [
    {
      "id": 1,
      "account_type": "banking",
      "name": "Chase Checking",
      "institution": "Chase Bank",
      "account_number_last4": "4567",
      "current_balance": 5420.50,
      "created_at": "2025-01-15T10:00:00Z"
    },
    {
      "id": 2,
      "account_type": "liability",
      "name": "Home Mortgage",
      "institution": "Wells Fargo",
      "current_balance": 285000.00,
      "interest_rate": 3.75,
      "due_date": "2025-01-15",
      "created_at": "2020-03-01T14:30:00Z"
    }
  ]
}
```

---

### POST /finance
Create financial account.

### PUT /finance/{id}
Update financial account.

### DELETE /finance/{id}
Delete financial account.

---

## One-on-One Conflict Topics

### GET /one-on-one/conflicts
List conflict topics (max 3).

**Response 200:**
```json
{
  "data": [
    {
      "id": 1,
      "topic": "Household chores division",
      "description": "Disagreement on who does what",
      "resolution_strategy": "Create weekly rotation chart together",
      "progress_notes": "Chart implemented, seeing improvement",
      "updated_at": "2025-10-10T20:00:00Z"
    }
  ]
}
```

---

### POST /one-on-one/conflicts
Create conflict topic (max 3 enforced).

### PUT /one-on-one/conflicts/{id}
Update conflict topic.

### DELETE /one-on-one/conflicts/{id}
Delete conflict topic.

---

## Entries (Journal) Endpoints

### GET /entries
List journal entries.

**Query Parameters:**
- `area_id` (int, optional)
- `date_from` (YYYY-MM-DD, optional)
- `date_to` (YYYY-MM-DD, optional)

**Response 200:**
```json
{
  "data": [
    {
      "id": 1,
      "title": "Reflection on morning routine",
      "content": "Started the day with meditation, felt centered...",
      "area": {"id": 8, "display_name": "Spiritual"},
      "entry_date": "2025-10-16",
      "created_at": "2025-10-16T07:30:00Z"
    }
  ]
}
```

---

### POST /entries
Create entry.

### PUT /entries/{id}
Update entry.

### DELETE /entries/{id}
Delete entry.

---

## AI Content Endpoints (Stubbed)

### GET /ai/verse
Get AI-generated Bible verse.

**Query Parameters:**
- `area` (physical_health|hobby|..., required)

**Response 200:**
```json
{
  "data": {
    "verse": "Philippians 4:13 - I can do all things through Christ who strengthens me.",
    "area": "physical_health",
    "generated_at": "2025-10-16T10:00:00Z"
  }
}
```

---

### GET /ai/insight
Get AI-generated insight.

**Query Parameters:**
- `area` (required)

**Response 200:**
```json
{
  "data": {
    "insight": "Consider setting a consistent bedtime to improve sleep quality and energy levels.",
    "area": "physical_health",
    "generated_at": "2025-10-16T10:00:00Z"
  }
}
```

---

## Error Responses

### 400 Bad Request
```json
{
  "detail": "Validation error: title is required",
  "error_code": "VALIDATION_ERROR"
}
```

### 401 Unauthorized
```json
{
  "detail": "Authentication required",
  "error_code": "AUTH_REQUIRED"
}
```

### 404 Not Found
```json
{
  "detail": "Goal not found",
  "error_code": "NOT_FOUND"
}
```

### 500 Internal Server Error
```json
{
  "detail": "An unexpected error occurred",
  "error_code": "INTERNAL_ERROR"
}
```

---

## Rate Limiting (Future)
Not implemented in MVP. Consider adding for production.

---

## Pagination (Future)
Optional for MVP. Recommended pattern:
```
GET /goals?page=1&limit=20

Response includes:
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
