# Implementation Plan
## Employee Support Ticket Management Application

| Item | Detail |
|---|---|
| Document | `PLAN.md` |
| Status | Ready for review — implementation waits for explicit approval |
| Requirements baseline | `SPEC.md` with RD-01 through RD-16 |
| Source prompt | `PRODUCT_PROMPT.md` |

This plan resolves the technical decisions left in `SPEC.md` section 19. It does not change any confirmed requirement. No application code is to be written until this plan is explicitly approved.

---

## 1. Scope

### Initial version

Build a complete, locally runnable web application with:

- Common login page for Employee and Support Staff
- Public Employee registration only
- Secure Support Staff initialization outside public registration
- Backend-enforced role-based access control
- Employee ticket creation, viewing, and permitted editing
- Support Staff ticket viewing, search, filtering, and status updates
- SQLite persistence through SQLAlchemy, with PostgreSQL-compatible configuration where practical
- Five seeded sample tickets and two seeded demonstration identities
- Modern, clean, responsive UI with no dummy controls
- README and genuine test/evidence record

### Deferred enhancement

Ticket comments are **not** part of the initial version. They are added only after the initial application is working and tested, as a separate commit and separate test pass.

---

## 2. Resolved Technical Decisions

| ID | Decision |
|---|---|
| TD-01 | Keep the proposed stack: React + Vite + plain CSS frontend, Python + FastAPI backend, SQLAlchemy ORM, and SQLite database. Configure the database through `DATABASE_URL` so a PostgreSQL URL can be substituted without changing application logic. |
| TD-02 | Use opaque server-side sessions. The backend stores a hash of a random session token in a system `sessions` table, sends the raw token in an HttpOnly cookie, verifies it on every protected request, loads role from the database, and revokes it on logout. |
| TD-03 | Use the REST paths, request bodies, and success codes in section 6 of this plan. Failure codes remain exactly as specified in `SPEC.md` section 12.3. |
| TD-04 | Use integer auto-increment primary keys: `users.id`, `tickets.id`, and later `comments.id`. These are unique system identifiers, not additional business fields. |
| TD-05 | Support Staff and sample account passwords come from environment variables or an interactive initialization prompt. No password value is written in source code or committed. `.env` is ignored by Git. |

---

## 3. Architecture

```text
Browser
  |  HTTPS/HTTP JSON + session cookie
  v
React + Vite SPA
  |  fetch API wrapper; role from backend only
  v
FastAPI application
  |  auth dependencies -> role/ownership checks -> services -> SQLAlchemy
  v
SQLAlchemy ORM
  |  SQLite by default; DATABASE_URL may select PostgreSQL-compatible driver
  v
Database file / PostgreSQL database
```

### Principles

- Backend is the authority for authentication, role, ownership, validation, timestamps, and status transitions.
- Frontend hides unavailable actions but never relies on hiding for security.
- All database access goes through a single configured ORM session layer.
- Services hold business rules; route handlers stay thin.
- Responses never contain password hashes, session token hashes, or secrets.
- Every visible UI control has a real backend-backed action.

---

## 4. Proposed Folder Layout

```text
Employee-Support-Ticket-App/
  PRODUCT_PROMPT.md
  SPEC.md
  PLAN.md
  README.md                      # later milestone
  Day4_Poojitha.md               # later milestone
  PROGRESS.md                    # only if context/usage requires a handoff
  .env.example                   # variable names only, no values
  .gitignore

  backend/
    app/
      __init__.py
      main.py                    # FastAPI app, middleware, routers, error handlers
      core/
        config.py                # env-based settings, DATABASE_URL
        security.py              # Argon2 password hashing, session token creation/hashing
        errors.py                # 400/401/403/404 response helpers
        time.py                  # UTC now and Asia/Kolkata display formatting
        validation.py            # trim/normalize/validation helpers
      db/
        base.py                  # DeclarativeBase
        session.py               # engine, SessionLocal, get_db dependency
        init_db.py               # create tables, PRAGMAs, constraints setup
      models/
        user.py
        ticket.py
        session.py
        comment.py               # enhancement phase only
      schemas/
        auth.py
        ticket.py
        dashboard.py
        comment.py               # enhancement phase only
      services/
        auth_service.py
        ticket_service.py
        dashboard_service.py
        comment_service.py       # enhancement phase only
      api/
        deps.py                  # get_current_user, require_employee, require_support
        routes/
          auth.py
          tickets.py
          dashboards.py
          comments.py            # enhancement phase only
    scripts/
      init_db.py
      seed_sample_data.py
      create_support_staff.py
    tests/
      conftest.py
      test_auth.py
      test_permissions.py
      test_tickets.py
      test_status_transitions.py
      test_dashboards.py
      test_persistence.py
      test_comments.py           # enhancement phase only

  frontend/
    index.html
    package.json
    vite.config.js
    .env.example                 # VITE_API_URL only if needed
    src/
      main.jsx
      App.jsx
      api/client.js              # fetch wrapper, credentials: include
      auth/AuthContext.jsx
      auth/ProtectedRoute.jsx
      components/
        AppShell.jsx
        NavBar.jsx
        StatCard.jsx
        TicketTable.jsx
        TicketForm.jsx
        TicketDetail.jsx
        StatusBadge.jsx
        PriorityBadge.jsx
        Alert.jsx
        ConfirmButton.jsx
      pages/
        LoginPage.jsx
        RegisterPage.jsx
        EmployeeDashboard.jsx
        SupportDashboard.jsx
        NotFound.jsx
        Forbidden.jsx
      styles/
        theme.css                # colors, typography, spacing tokens
        layout.css               # responsive layout
        components.css           # forms, tables, cards, badges, feedback
```

Files for comments are created only during the comments enhancement phase.

---

## 5. Database Design

### 5.1 Configuration

- `DATABASE_URL` defaults to `sqlite:///./support_tickets.db`.
- A PostgreSQL URL such as `postgresql+psycopg://user:pass@host:5432/dbname` may be supplied through environment variables.
- Use SQLAlchemy generic types and ORM queries only; no SQLite-specific SQL in application code.
- Enable SQLite `PRAGMA foreign_keys=ON` on connection.
- Use `pool_pre_ping=True` where supported.
- Use one `SessionLocal` factory and one `get_db` dependency. Route handlers do not create their own engines.

### 5.2 Tables

**users**

| Column | Type / rule |
|---|---|
| `id` | Integer primary key, auto-increment |
| `full_name` | String, required, trimmed before validation and storage |
| `email` | String, required, trimmed + lowercase, unique index |
| `password_hash` | String, required, Argon2 hash; never returned by API |
| `role` | Enum: `Employee` or `Support Staff`; backend-controlled |
| `created_at` | UTC timestamp |
| `updated_at` | UTC timestamp |

No arbitrary account-count limit is imposed.

**tickets**

| Column | Type / rule |
|---|---|
| `id` | Integer primary key, auto-increment |
| `title` | String, required, trimmed, max 100 characters |
| `description` | Text, required, trimmed, max 2,000 characters |
| `category` | Enum/check: Hardware, Software, Network, Access, Other |
| `priority` | Enum/check: Low, Medium, High |
| `status` | Enum/check: Open, In Progress, Resolved, Closed |
| `creator_id` | Foreign key to `users.id`, `ON DELETE RESTRICT`, immutable |
| `created_at` | UTC timestamp, immutable |
| `updated_at` | UTC timestamp, backend-managed |

These columns represent the eight specified business fields plus the required unique identifier and foreign key. No comment column exists in the initial version.

**sessions** (system table)

| Column | Type / rule |
|---|---|
| `id` | Integer primary key |
| `token_hash` | String, unique, hashed opaque token |
| `user_id` | Foreign key to `users.id`, `ON DELETE CASCADE` |
| `expires_at` | UTC timestamp |
| `revoked_at` | UTC timestamp, nullable |
| `created_at` | UTC timestamp |

Only the token hash is stored. Logout sets `revoked_at`.

**comments** (enhancement phase only)

| Column | Type / rule |
|---|---|
| `id` | Integer primary key |
| `ticket_id` | Foreign key to `tickets.id`, `ON DELETE CASCADE` |
| `author_id` | Foreign key to `users.id`, `ON DELETE RESTRICT` |
| `content` | Text, trimmed, non-empty |
| `created_at` | UTC timestamp |

Comments are displayed oldest first. Adding a comment never changes ticket status or `updated_at`.

### 5.3 Integrity and Reliability

- Define relationships with SQLAlchemy `relationship()` and `ForeignKey`.
- Add unique constraint on normalized email and session token hash.
- Add check constraints for enum-like fields and string lengths where the database supports them.
- Wrap each multi-step write in one transaction; commit only after validation succeeds.
- Roll back on validation, integrity, or database errors.
- Return clear 500-level error for unexpected database failure without leaking internals.
- Seed idempotently: check by natural keys before insert; never duplicate sample tickets on repeated runs.
- No credentials, tokens, or secret values in source code.

---

## 6. API Design

Base path: `/api`. JSON request/response bodies. Cookie-based session authentication.

### 6.1 Public endpoints

| Method | Path | Body | Success |
|---|---|---|---|
| POST | `/api/auth/register` | `full_name`, `email`, `password`, `confirm_password` | 201 with safe user fields |
| POST | `/api/auth/login` | `email`, `password` | 200 with safe user fields and role; sets session cookie |
| GET | `/api/health` | none | 200 |

Client-supplied `role` is ignored and never applied.

### 6.2 Authenticated endpoints

| Method | Path | Who | Body / query | Success |
|---|---|---|---|---|
| GET | `/api/auth/me` | Both | none | 200 safe user |
| POST | `/api/auth/logout` | Both | none | 204; session revoked and cookie cleared |
| POST | `/api/tickets` | Employee | `title`, `description`, `category`, `priority` | 201 ticket |
| GET | `/api/employee/dashboard` | Employee | none | 200 counts + latest 5 tickets |
| GET | `/api/employee/tickets` | Employee | none | 200 own tickets |
| GET | `/api/tickets/{ticket_id}` | Both | none | 200 full ticket; employee limited to own |
| PATCH | `/api/tickets/{ticket_id}` | Employee only | only `title`, `description`, `category`, `priority` | 200 ticket; 403 for Support Staff |
| GET | `/api/support/dashboard` | Support Staff | none | 200 all-ticket counts |
| GET | `/api/support/tickets` | Support Staff | `search`, `status`, `category`, `priority` | 200 filtered tickets |
| POST | `/api/tickets/{ticket_id}/status` | Support Staff | `status` | 200 ticket; only next-step transitions |

### 6.3 Comments enhancement endpoints

| Method | Path | Who | Success |
|---|---|---|---|
| GET | `/api/tickets/{ticket_id}/comments` | Employee on own ticket; Support Staff on any ticket | 200 chronological list |
| POST | `/api/tickets/{ticket_id}/comments` | Employee on own ticket; Support Staff on any ticket | 201 comment |

Comments remain allowed on Closed tickets and do not change ticket status or `updated_at`.

### 6.4 Error handling

Failure codes follow `SPEC.md` section 12.3 exactly:

- 400 for validation failure, duplicate registration, bad input, and illegal status transition
- 401 for missing, invalid, or expired authentication and failed login credentials
- 403 for authorization failures, including role restrictions and ownership failures
- 404 for a missing ticket identifier

Check order: authentication → ticket existence → authorization → input validation.

All errors use a consistent JSON shape such as `{"detail": "..."}`. No stack traces, password hashes, secrets, or another employee’s ticket content are exposed.

---

## 7. Authentication and Permissions

### 7.1 Password and email handling

- Hash passwords with Argon2 from `argon2-cffi`.
- Verify the exact submitted password; never trim passwords.
- Trim and lowercase email for storage, uniqueness, and login lookup.
- Trim full names, ticket titles, and ticket descriptions before validation and storage.
- Validate email using the exact simple rule in `SPEC.md` section 3.2.
- Confirm password must match exactly.
- No arbitrary Employee account maximum.

### 7.2 Session flow

1. Login verifies normalized email and exact password.
2. Backend reads role from `users`.
3. Backend creates a random opaque token, stores only its hash in `sessions`, and sets an HttpOnly cookie.
4. Cookie uses `SameSite=Lax`; `Secure` is enabled when not running locally.
5. Every protected request resolves the session, checks expiry/revocation, and loads the current user.
6. Logout revokes the session and clears the cookie.
7. Frontend redirects based only on the role returned by the backend.

### 7.3 Authorization rules

- Employee: own tickets only; may create; may edit four content fields when status is not Closed; cannot change status.
- Support Staff: all tickets; may search/filter; may advance status one step; cannot create tickets; cannot edit content.
- Unauthenticated protected API call: 401.
- Employee calling support-only API or status update: 403.
- Employee requesting another employee’s ticket: 403.
- Missing ticket: 404 after authentication.

---

## 8. Frontend and UI Plan

### 8.1 Structure

- React Router for public, employee, and support route groups.
- `AuthContext` loads `/api/auth/me` on startup and stores only safe user data.
- `ProtectedRoute` checks authenticated role; backend still enforces every rule.
- One shared API client sets `credentials: "include"` and surfaces backend error messages.
- Reusable `TicketTable`, `TicketForm`, `TicketDetail`, `StatCard`, badges, and `Alert` components.

### 8.2 Screens

- Login: common for both roles, no role selector.
- Register: Employee only, no role field.
- Employee dashboard: counts, recent 5 newest-first tickets, create-ticket action.
- Ticket create/edit form: title, description, category, priority only.
- Ticket detail: eight business fields, edit action only for owning employee and non-Closed status.
- Support dashboard: counts, all tickets, search, three filters, status advance action.
- Forbidden and Not Found pages.

### 8.3 Design requirements

- Modern, clean, professional visual style with a defined color and spacing system.
- Large readable fonts and clear visual hierarchy.
- Responsive CSS grid/flex layouts for desktop, tablet, and mobile.
- Tables become stacked cards at narrow widths; navigation collapses cleanly.
- No horizontal page scrolling, clipped content, or overlapping elements.
- Avoid duplicate information: counts appear once; the recent-ticket section remains separate from the full ticket list.
- Every button, link, form, filter, and navigation control has a real handler and visible feedback.

---

## 9. Implementation Sequence and Git Checkpoints

The repository currently has no commits; `PRODUCT_PROMPT.md` and `SPEC.md` are untracked. After approval, create the first code commit only when the backend and database milestone actually works.

| Phase | Work | Commit checkpoint |
|---|---|---|
| 0 | Approve `SPEC.md` and `PLAN.md` | No code yet |
| 1 | Backend foundation: config, DB session, models, error handlers, table creation, safe seed/init scripts | `backend and database` |
| 2 | Auth: Argon2, registration, login, sessions, logout, `/me`, dependencies | `authentication` |
| 3 | Employee ticket create/list/detail/edit and employee dashboard API | `employee functionality` |
| 4 | Support ticket list/detail/search/filter/dashboard/status API | `support staff functionality` |
| 5 | React/Vite UI integration, responsive styling, full manual smoke test of initial app | `frontend integration` |
| 6 | Ticket comments enhancement with model, API, UI, and tests | `comments enhancement` |
| 7 | Automated tests, security/authorization review, dependency review | `automated tests and review` |
| 8 | Find, document, fix, and retest one genuine defect | `defect fix and tests` |
| 9 | README, submission document, final evidence index | `final documentation` |

Before every commit:

- Run relevant backend/frontend tests or build checks.
- Confirm no secret or `.env` file is staged.
- Confirm the commit succeeded with Git output before reporting it.
- Record genuine pass/fail results; do not claim unverified behavior.

If context or execution must stop early, save working files, commit only verified milestones, and write `PROGRESS.md` with completed work, remaining work, and the exact next command/action.

---

## 10. Testing Strategy

### 10.1 Automated backend tests

Use `pytest` and FastAPI `TestClient` with a temporary database per test session.

Cover:

- Registration validation, trimming, exact password confirmation, 8-character minimum, case-insensitive duplicates, client role rejection
- Login with normalized email, wrong password 401, missing fields 400, role returned from database
- Session protection, logout invalidation, 401 for unauthenticated calls
- Employee ticket creation validation including 100-character title and 2,000-character description boundaries
- Category/priority enum rejection
- Ownership enforcement and 403 for another employee’s ticket
- Employee edit restrictions: content only, non-Closed only, no status change
- Support Staff status transitions: legal next step succeeds; skip/backward/same/Closed returns 400
- Support Staff cannot edit content; employee cannot call status endpoint
- Dashboard counts and recent-5 ordering
- Search over title, description, creator name; combined filters
- Missing ticket 404
- Persistence after re-created session against the same database file
- Comments enhancement: authorization, chronological order, Closed tickets allowed, no status/timestamp change

### 10.2 Frontend checks

- `npm run build` must succeed.
- Manual browser checks at desktop, tablet, and mobile widths.
- Every visible control checked against a written checklist.
- Verify no placeholder buttons, dead links, or decorative filters.
- Verify forms show validation and backend error messages.

### 10.3 Runtime checks

Commands expected after implementation:

```bash
python -m backend.scripts.init_db
python -m backend.scripts.seed_sample_data
uvicorn backend.app.main:app --reload --port 8000
```

```bash
cd frontend
npm install
npm run dev
```

Environment variables are documented in `.env.example` and README. The seed scripts refuse to run without required password variables unless interactive mode is selected.

### 10.4 Evidence

Genuine results and screenshots are recorded in `Day4_Poojitha.md`. If a screenshot or evidence item was not actually captured, it is marked **Pending**; nothing is fabricated.

---

## 11. Review Checklist Before Final Submission

- Requirements RD-01 through RD-16 still satisfied.
- Comments absent from initial version and present only as the separate enhancement.
- Input validation on backend; trimming/normalization rules correct.
- Password hashing and no secret exposure.
- Backend RBAC and ticket ownership verified through direct API calls.
- Correct 400/401/403/404 behavior and check order.
- Database transactions, constraints, relationships, and restart persistence verified.
- UTC storage and Asia/Kolkata display verified.
- Responsive layout and all controls verified.
- Tests run with actual pass/fail output recorded.
- README and submission document include what AI generated, what was changed manually, and what was actually checked.
