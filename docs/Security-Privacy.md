# Security & Privacy Documentation
## AI-Assisted Life Management Application MVP

**Version:** 1.0
**Date:** 2025-10-16

---

## 1. Security Overview

### Threat Model

**Assets to Protect:**
- User passwords
- Personal health information (PHI)
- Financial data (accounts, balances)
- Relationship information
- Session tokens

**Threat Actors:**
- Malicious users attempting unauthorized access
- Attackers exploiting web vulnerabilities
- Accidental data exposure

**Attack Vectors:**
- Weak passwords
- Session hijacking
- SQL injection
- Cross-site scripting (XSS)
- Cross-site request forgery (CSRF)
- Insecure direct object references (IDOR)

---

## 2. Authentication & Authorization

### Password Security

**Hashing:**
- Algorithm: **bcrypt**
- Cost factor: **12** (configurable)
- Never store plaintext passwords
- Password validation on update

**Implementation:**
```python
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)
```

**Password Requirements:**
- Minimum 8 characters (enforced in Pydantic schema)
- Recommend: Mix of upper/lower/numbers/symbols (future enhancement)
- No password reset in MVP (future: email-based reset)

---

### Session Management

**Cookies:**
- **Signed cookies** using `itsdangerous` or Starlette's `SessionMiddleware`
- Signature prevents tampering
- Session data stored server-side (in-memory for MVP)

**Cookie Settings:**
```python
from starlette.middleware.sessions import SessionMiddleware

app.add_middleware(
    SessionMiddleware,
    secret_key=os.getenv("APP_SECRET"),  # Must be strong random string
    session_cookie="session_id",
    max_age=86400,  # 24 hours
    same_site="lax",
    https_only=False,  # Set True in production with HTTPS
    http_only=True  # Prevents JavaScript access (XSS protection)
)
```

**Session Lifecycle:**
1. User logs in → session created → cookie set
2. Subsequent requests → cookie validated → user ID extracted
3. User logs out → session destroyed → cookie cleared

**Session Expiry:**
- MVP: 24-hour max age
- Future: Configurable timeout, "Remember me" option

---

### Authorization

**Resource Ownership:**
- All resources (goals, habits, etc.) have `user_id` foreign key
- **Enforce:** Only allow users to access their own data

**Implementation:**
```python
from fastapi import Depends, HTTPException, status

def get_current_user(session: Session = Depends(get_session)) -> User:
    # Extract user_id from session cookie
    # Query user from database
    # If not found, raise 401 Unauthorized
    pass

@router.get("/goals")
def list_goals(current_user: User = Depends(get_current_user)):
    # Automatically filter by current_user.id
    goals = session.query(Goal).filter(Goal.user_id == current_user.id).all()
    return goals
```

**IDOR Prevention:**
```python
@router.get("/goals/{goal_id}")
def get_goal(goal_id: int, current_user: User = Depends(get_current_user)):
    goal = session.query(Goal).filter(
        Goal.id == goal_id,
        Goal.user_id == current_user.id  # Critical: ownership check
    ).first()

    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")

    return goal
```

---

## 3. Input Validation & Sanitization

### Pydantic Validation

**Automatic Validation:**
- FastAPI + Pydantic validate all inputs
- Type checking (str, int, date, etc.)
- Length limits (max_length on strings)
- Enum validation (status, timeframe, etc.)
- Custom validators for complex logic

**Example:**
```python
from pydantic import BaseModel, validator, Field

class GoalCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    timeframe: GoalTimeframe  # Enum: short|medium|long
    progress_percentage: int = Field(0, ge=0, le=100)

    @validator("title")
    def title_not_empty(cls, v):
        if not v.strip():
            raise ValueError("Title cannot be empty")
        return v.strip()
```

**Validation Failures:**
- Return **422 Unprocessable Entity**
- Include specific error messages
- Never expose internal implementation details

---

### SQL Injection Prevention

**SQLAlchemy/SQLModel Protection:**
- **Always use ORM methods** (no raw SQL strings)
- Parameterized queries automatically
- Never concatenate user input into SQL

**Safe:**
```python
# SQLAlchemy ORM automatically parameterizes
goals = session.query(Goal).filter(Goal.user_id == user_id).all()
```

**Unsafe (NEVER DO THIS):**
```python
# VULNERABLE to SQL injection
query = f"SELECT * FROM goals WHERE user_id = {user_id}"
session.execute(query)
```

**Raw SQL (If Necessary):**
```python
# Use parameterized queries
from sqlalchemy import text

stmt = text("SELECT * FROM goals WHERE user_id = :user_id")
result = session.execute(stmt, {"user_id": user_id})
```

---

### XSS Prevention

**API-Only MVP:**
- JSON API returns structured data, not HTML
- XSS risk is minimal (frontend responsibility)

**Future Frontend:**
- Sanitize user input on render
- Use framework built-in protections (React escapes by default)
- Never use `dangerouslySetInnerHTML` without sanitization
- Content Security Policy (CSP) headers

---

### CSRF Prevention

**Session Cookies with SameSite:**
- `same_site="lax"` provides CSRF protection
- Cookies not sent on cross-origin POST requests

**Future Enhancement:**
- CSRF tokens for state-changing operations
- Double-submit cookie pattern
- Custom CSRF middleware

---

## 4. Data Privacy

### Personal Identifiable Information (PII)

**PII Stored:**
- Username (required)
- Email (optional)
- Full name (optional)
- Contact information (phone, email, address)
- Birthdays
- Health data (doctors, medications, supplements)
- Financial data (account balances, debts)
- Relationship data (conflict topics, journal entries)

**Privacy Measures:**
- **Local-first:** All data stays on user's machine (SQLite file)
- **No telemetry:** No data sent to external servers (except future AI API calls)
- **No analytics:** No tracking or usage analytics in MVP
- **Encryption at rest:** SQLite file unencrypted (future: SQLCipher for encryption)

---

### Data Sharing

**MVP: Zero Sharing**
- Single-user deployment per instance
- No multi-user features
- No data export endpoints (future enhancement)

**Future Considerations:**
- Family sharing: Implement permissions system
- Data export: Allow user to download JSON/CSV
- Data deletion: GDPR-compliant "right to be forgotten"

---

### AI Integration Privacy

**MVP (Stubbed):**
- No external API calls
- All AI content is static/local

**Future (Real AI):**
- **Minimize data sent:** Send only necessary context, not entire database
- **User consent:** Inform users that data is sent to AI provider
- **Provider choice:** Allow users to choose provider or use local LLM
- **Data retention:** Understand provider's data retention policies
- **Anonymization:** Remove PII when possible before sending to AI

**Example (Future):**
```python
# BAD: Sending entire user profile to AI
prompt = f"User's full data: {user.all_data}"

# GOOD: Sending only necessary context
prompt = f"Generate a Bible verse for someone focused on {area}"
```

---

## 5. Secrets Management

### Environment Variables

**.env File:**
```bash
APP_SECRET=random-64-character-secret-key-here
DATABASE_URL=sqlite:///./data/app.sqlite3
ENVIRONMENT=development
```

**Security Measures:**
- `.env` excluded from git (via `.gitignore`)
- `.env.example` provided with placeholders
- Strong `APP_SECRET` (min 32 characters, random)

**Generate Strong Secret:**
```python
import secrets
print(secrets.token_urlsafe(32))  # Use this in .env
```

**Production:**
- Use environment variables (Docker secrets, etc.)
- Never commit secrets to git
- Rotate secrets periodically

---

### API Keys (Future)

When integrating AI APIs:
- Store in `.env` (e.g., `OPENAI_API_KEY`)
- Use environment variables in production
- Never log API keys
- Rotate keys if exposed

---

## 6. Database Security

### SQLite File Protection

**File Permissions:**
```bash
chmod 600 data/app.sqlite3  # Owner read/write only
```

**Backup Security:**
- Backups should have same permissions
- Encrypt backups if storing remotely

**Encryption (Future):**
- Use **SQLCipher** for encrypted SQLite
- Requires encryption key (stored separately)

---

### Connection Security

**Local Deployment:**
- SQLite file-based, no network exposure
- Only accessible to local user

**Future (PostgreSQL):**
- Use SSL/TLS for database connections
- Strong database passwords
- Restrict database access by IP (firewall)

---

## 7. API Security

### HTTPS (Production)

**MVP (Local):**
- HTTP is acceptable for `localhost`

**Production:**
- **MUST use HTTPS** for any networked deployment
- Use Let's Encrypt for free TLS certificates
- HSTS header to enforce HTTPS

---

### CORS Configuration

**Current (API-only MVP):**
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Future frontend dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**Production:**
- Restrict `allow_origins` to specific domains
- Avoid `allow_origins=["*"]` with `allow_credentials=True`

---

### Rate Limiting (Future)

**Not in MVP**

**Future Implementation:**
- Use `slowapi` or similar
- Limit requests per IP per time window
- Prevent brute-force login attempts
- Prevent API abuse

**Example:**
```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@app.post("/auth/login")
@limiter.limit("5/minute")  # Max 5 login attempts per minute
def login(request: Request, ...):
    pass
```

---

## 8. Error Handling & Logging

### Secure Error Messages

**Do:**
- Return generic error messages to users
- "Invalid credentials" (not "Username not found" or "Wrong password")
- "Goal not found" (don't reveal if ID exists for another user)

**Don't:**
- Expose stack traces to users (only log internally)
- Reveal database schema or internal paths
- Leak sensitive data in error responses

**Example:**
```python
# GOOD
raise HTTPException(status_code=401, detail="Invalid credentials")

# BAD
raise HTTPException(status_code=401, detail=f"User '{username}' not found in database")
```

---

### Logging

**What to Log:**
- Login attempts (success and failure)
- Authentication errors
- Authorization failures (user trying to access others' data)
- API errors (500 errors)

**What NOT to Log:**
- Passwords (plaintext or hashed)
- Session tokens
- API keys
- Full request bodies (may contain sensitive data)

**Logging Configuration:**
```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

# Log authentication
logger.info(f"User {user_id} logged in")

# Don't log sensitive data
logger.info(f"User {user_id} created goal")  # Good
logger.info(f"User created goal: {goal.title}")  # Bad if title is sensitive
```

---

## 9. Compliance & Regulations

### GDPR (If Deploying in EU)

**User Rights:**
- **Right to Access:** Users can view all their data (API provides this)
- **Right to Rectification:** Users can update their data (API provides this)
- **Right to Erasure:** Users can delete their account (future: add delete endpoint)
- **Right to Data Portability:** Users can export their data (future: export endpoint)

**Implementation (Future):**
- `DELETE /api/users/me` - Delete account and all data
- `GET /api/users/me/export` - Download all data as JSON

---

### HIPAA (If Storing PHI in US)

**Not Applicable for MVP:**
- Self-hosted, single-user deployment
- No healthcare provider involvement

**If Expanding to Multi-User SaaS:**
- PHI data (doctors, medications) requires HIPAA compliance
- Encryption at rest and in transit
- Audit logs
- Business Associate Agreements (BAAs)
- Consider NOT storing PHI or get legal guidance

---

### Data Retention

**MVP:**
- Data persists indefinitely (user manages database file)

**Future:**
- Configurable retention policies
- Auto-delete old entries (with user consent)
- Soft deletes with recovery period

---

## 10. Dependency Security

### Dependency Management

**requirements.txt:**
- Pin versions to avoid unexpected updates
- `fastapi==0.104.1` (not `fastapi>=0.104.1`)

**Security Updates:**
```bash
# Check for vulnerabilities
pip install safety
safety check

# Or use pip-audit
pip install pip-audit
pip-audit
```

**Update Strategy:**
- Review changelogs before updating
- Test after updating dependencies
- Subscribe to security advisories for key packages

---

### Known Vulnerabilities

**Check Before Release:**
```bash
pip-audit
```

**If Vulnerabilities Found:**
- Update to patched version
- If no patch available, consider alternatives
- Document known issues in README

---

## 11. Secure Development Practices

### Code Review

**MVP (Solo Dev):**
- Self-review code before committing
- Use linters (flake8, pylint)
- Use type checkers (mypy)

**Future (Team):**
- Require code reviews for all changes
- Automated security scans in CI/CD

---

### Testing for Security

**Security Test Cases:**
1. **Authentication Bypass:**
   - Try accessing protected endpoints without session
   - Verify 401 response

2. **Authorization Bypass (IDOR):**
   - User A tries to access User B's goal
   - Verify 404 response (not 403, to avoid info leak)

3. **SQL Injection:**
   - Input special chars in all string fields
   - Verify no errors, data sanitized

4. **XSS (Future Frontend):**
   - Input `<script>alert('xss')</script>` in text fields
   - Verify it's escaped on render

5. **CSRF (Future):**
   - Attempt cross-origin state-changing requests
   - Verify SameSite cookie blocks them

---

## 12. Incident Response

### Security Breach Procedure

**MVP (Self-Hosted):**
1. User discovers breach (e.g., unauthorized access)
2. Change all passwords immediately
3. Revoke all sessions (restart server)
4. Review logs for suspicious activity
5. Restore from backup if data tampered

**Future (Multi-User):**
1. Identify scope of breach
2. Notify affected users
3. Force password resets
4. Patch vulnerability
5. Document incident
6. Improve defenses

---

### Contact for Security Issues

**MVP:**
- User is developer/admin
- Self-service incident response

**Future:**
- security@example.com email
- Responsible disclosure policy
- Security bug bounty (optional)

---

## 13. Backup & Recovery

### Backup Strategy

**Database Backup:**
```bash
# Simple copy
cp data/app.sqlite3 data/backups/app_$(date +%Y%m%d).sqlite3

# Compressed backup
tar -czf backups/app_$(date +%Y%m%d).tar.gz data/app.sqlite3
```

**Automated Backups (Cron):**
```bash
# Run daily at 2 AM
0 2 * * * /path/to/backup-script.sh
```

**Backup Security:**
- Encrypt backups if stored remotely
- Secure backup storage (permissions, access control)
- Test restore procedure regularly

---

### Disaster Recovery

**Data Loss Scenarios:**
1. Accidental deletion
2. Database corruption
3. Hardware failure

**Recovery Procedure:**
1. Stop application
2. Restore SQLite file from backup
3. Verify data integrity
4. Restart application

**Future: Point-in-Time Recovery:**
- Use PostgreSQL with WAL archiving
- Restore to specific timestamp

---

## 14. Security Checklist

Before deploying (even locally):

- [ ] `APP_SECRET` is strong random string (min 32 chars)
- [ ] `.env` file excluded from git
- [ ] Passwords hashed with bcrypt (cost 12+)
- [ ] Session cookies HTTP-only and signed
- [ ] All endpoints check authentication
- [ ] User data isolation enforced (user_id filters)
- [ ] No raw SQL (use ORM)
- [ ] Input validation via Pydantic
- [ ] Error messages don't leak sensitive info
- [ ] No passwords or tokens in logs
- [ ] SQLite file has restrictive permissions (600)
- [ ] Dependencies checked for vulnerabilities
- [ ] HTTPS used if network-accessible (production)
- [ ] CORS restricted to specific origins
- [ ] Tests include security scenarios

---

## 15. Future Enhancements

### Post-MVP Security Improvements:

1. **Two-Factor Authentication (2FA)**
   - TOTP (e.g., Google Authenticator)
   - SMS backup codes

2. **Password Reset**
   - Email-based reset flow
   - Secure token generation
   - Time-limited reset links

3. **Audit Logs**
   - Track all data changes
   - Who, what, when
   - Tamper-proof logs

4. **Rate Limiting**
   - Prevent brute-force attacks
   - API abuse prevention

5. **Encryption at Rest**
   - SQLCipher for encrypted SQLite
   - Or migrate to PostgreSQL with transparent data encryption

6. **Penetration Testing**
   - Hire security firm for audit
   - Bug bounty program

7. **Compliance Certifications**
   - SOC 2 (if SaaS)
   - HIPAA (if handling PHI)

---

## Related Documents
- [PRD.md](PRD.md) - Product requirements
- [Architecture.md](Architecture.md) - System design
- [Implementation-Plan.md](Implementation-Plan.md) - Build steps
- [Acceptance-Tests.md](Acceptance-Tests.md) - Test scenarios
