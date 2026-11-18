# Employee Support Ticket App

A locally runnable Employee Support Ticket Management Application built with React + Vite and FastAPI + SQLAlchemy. Employees can raise and manage their own tickets; Support Staff can review all tickets and advance statuses. Ticket comments are intentionally excluded from this initial version.

## Features

- Common login page and Employee-only public registration
- Secure Support Staff creation through an initialization script only
- Backend-enforced Employee/Support Staff roles and ticket ownership
- Employee dashboard with counts and latest 5 tickets (newest first)
- Employee ticket creation, viewing, and editing of title, description, category, and priority
- Support dashboard with all-ticket counts
- Support ticket list with title/description/creator search and status/category/priority filters
- One-step status workflow: Open → In Progress → Resolved → Closed
- UTC storage and Asia/Kolkata display (`18 Nov 2026, 09:15 AM`)
- Five idempotently seeded sample tickets and two demonstration accounts
- Argon2 password hashing and hashed, revocable server-side sessions
- Responsive desktop, tablet, and mobile UI with no dummy controls

## Architecture

```text
React + Vite SPA
  |  JSON + HttpOnly session cookie
  v
FastAPI
  |  auth dependencies -> role/ownership checks -> services -> SQLAlchemy
  v
SQLAlchemy ORM
  |  SQLite by default; DATABASE_URL may select PostgreSQL driver
  v
Persistent database
```

Key backend locations:

- `backend/app/main.py`: app setup, CORS, error handlers, routes
- `backend/app/api/deps.py`: authentication and role dependencies
- `backend/app/services/`: business rules and ticket queries
- `backend/app/models/`: `User`, `Ticket`, `UserSession`
- `backend/app/db/session.py`: engine, session factory, table creation
- `backend/scripts/`: initialization and seed scripts

Key frontend locations:

- `frontend/src/api/client.js`: single API wrapper
- `frontend/src/auth/`: auth context and route guard
- `frontend/src/pages/`: screens
- `frontend/src/components/`: reusable UI pieces
- `frontend/src/styles/`: design tokens, layout, components

## Prerequisites

- Python 3.11 or newer (tested with Python 3.14.7)
- Node.js 20 or newer (tested with Node.js 24.21.0)
- npm (tested with 11.19.0)

## Installation

From the project root:

```powershell
python -m venv .venv
.venv\Scripts\python.exe -m pip install -r backend\requirements.txt
cd frontend
npm install
cd ..
```

Copy the example environment file if you want to override defaults:

```powershell
Copy-Item .env.example .env
```

`.env` is ignored by Git. Never commit real passwords or secrets.

## Configuration

| Variable | Default | Purpose |
|---|---|---|
| `DATABASE_URL` | `sqlite:///./support_tickets.db` | SQLAlchemy database URL. A PostgreSQL URL such as `postgresql+psycopg://user:pass@host:5432/dbname` can be supplied without changing application code. Install the relevant driver separately. |
| `SESSION_COOKIE_NAME` | `support_tickets_session` | Session cookie name |
| `SESSION_TTL_HOURS` | `8` | Session lifetime |
| `SECURE_COOKIES` | `false` | Set to `true` behind HTTPS in non-local deployments |
| `CORS_ORIGINS` | localhost:5173 addresses | Comma-separated allowed origins |
| `SUPPORT_STAFF_NAME` | interactive prompt | Support Staff initialization |
| `SUPPORT_STAFF_EMAIL` | interactive prompt | Support Staff initialization |
| `SUPPORT_STAFF_PASSWORD` | interactive prompt | Support Staff initialization, minimum 8 characters |
| `SEED_EMPLOYEE_PASSWORD` | interactive prompt | Sample employee password, minimum 8 characters |
| `SEED_SUPPORT_PASSWORD` | interactive prompt | Sample Support Staff password, minimum 8 characters |

The Vite dev server proxies `/api` to `http://localhost:8000`, so `VITE_API_URL` is normally unnecessary. If the backend is hosted elsewhere, set `VITE_API_URL` in `frontend/.env`.

## Database initialization and sample data

Create tables:

```powershell
.venv\Scripts\python.exe -m backend.scripts.init_db
```

Seed the five sample tickets and two demonstration accounts:

```powershell
$env:SEED_EMPLOYEE_PASSWORD='EmployeeSeed123'
$env:SEED_SUPPORT_PASSWORD='SupportSeed123'
.venv\Scripts\python.exe -m backend.scripts.seed_sample_data
```

The seed is idempotent: repeated runs do not duplicate tickets. Use different passwords for any real demonstration.

Create an additional Support Staff account securely:

```powershell
$env:SUPPORT_STAFF_NAME='Support Admin'
$env:SUPPORT_STAFF_EMAIL='support2@company.com'
$env:SUPPORT_STAFF_PASSWORD='ChooseALongPassword'
.venv\Scripts\python.exe -m backend.scripts.create_support_staff
```

Omitting environment variables switches the script to interactive prompts. There is no public Support Staff registration page or API.

## Running the application

Start the backend from the project root:

```powershell
.venv\Scripts\python.exe -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000
```

Start the frontend in a second terminal:

```powershell
cd frontend
npm run dev
```

Open <http://127.0.0.1:5173>.

Seeded demonstration logins (using the passwords supplied to the seed command above):

- Employee: `ravi@company.com`
- Support Staff: `support@company.com`

## Tests

Backend:

```powershell
.venv\Scripts\python.exe -m pytest backend/tests -v
```

Latest recorded result: **22 passed, 1 warning**. The warning is a Starlette TestClient/httpx deprecation notice, not a failure.

Frontend production build:

```powershell
cd frontend
npm run build
```

Latest recorded result: build succeeded with Vite 8.3.8.

## Security notes

- Passwords are hashed with Argon2; plain passwords are never stored or returned.
- Password confirmation is compared exactly; passwords are never trimmed.
- Full names, ticket titles, and descriptions are trimmed before validation/storage.
- Emails are trimmed and lowercased for uniqueness and login.
- Session tokens are random, stored only as SHA-256 hashes, sent in HttpOnly/SameSite=Lax cookies, and revoked on logout.
- Every protected route resolves the user and role from the database on each request.
- Error responses use consistent JSON and do not expose stack traces, password hashes, or another employee's ticket contents.
- Failed writes leave ticket fields and timestamps unchanged.

## Known gaps

- Ticket comments are deliberately deferred to a separate enhancement after the initial app.
- No e-mail/SMS notifications, AI classification, chat, payments, or enterprise admin UI are included.
- `npm audit` currently reports high-severity advisories in Vite's development-server dependency chain (`picomatch`, `fdir`, `tinyglobby`). There is no published non-vulnerable `picomatch` version at the time of verification. These are development-only dependencies; `npm run build` succeeds. Do not expose the Vite dev server to untrusted networks.
- A PostgreSQL deployment requires installing the chosen driver and supplying `DATABASE_URL`; automated tests were executed against SQLite only.
- No GitHub remote was configured in this workspace at the time of writing, so the submission document records the GitHub link as Pending.

## Evidence

Genuine browser captures are in `evidence/`:

- `01-employee-dashboard.png`
- `02-login.png`
- `03-support-tickets.png`

Full verification details, prompts, and defect reports are in `Day4_Poojitha.md`.
