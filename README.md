# Employee Support Ticket App

A locally runnable Employee Support Ticket Management Application built with React + Vite and FastAPI + SQLAlchemy.

Employees can submit and track their own support requests. Support Staff can review all tickets, search and filter them, and move them through the status workflow. Both roles can discuss a ticket in its comment section, including after the ticket is Closed.

This README reflects the project as recorded on 18 Nov 2026. The original product prompt, requirements, implementation plan, verification record, and submission notes are preserved in [`PRODUCT_PROMPT.md`](PRODUCT_PROMPT.md), [`SPEC.md`](SPEC.md), [`PLAN.md`](PLAN.md), [`PROGRESS.md`](PROGRESS.md), and [`Day4_Poojitha.md`](Day4_Poojitha.md).

## Contents

- [Project overview](#project-overview)
- [Technologies](#technologies)
- [Project structure](#project-structure)
- [Features and permissions](#features-and-permissions)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Environment configuration](#environment-configuration)
- [Database setup and initialization](#database-setup-and-initialization)
- [Running the application](#running-the-application)
- [Troubleshooting: 502 when saving a ticket](#troubleshooting-502-when-saving-a-ticket)
- [API summary](#api-summary)
- [Tests and build](#tests-and-build)
- [Authentication and security](#authentication-and-security)
- [Evidence and verification record](#evidence-and-verification-record)
- [Authorship, decisions, and personal verification](#authorship-decisions-and-personal-verification)
- [Known limitations and remaining gaps](#known-limitations-and-remaining-gaps)

## Project overview

The application centralizes workplace and technical support requests so that:

1. Employees can submit support requests through a simple form.
2. Employees can monitor the status of their own tickets.
3. Employees can update permitted ticket fields while a ticket is not Closed.
4. Support Staff can view and manage all submitted tickets.
5. Only Support Staff can change ticket status.
6. Ticket access is controlled by backend role and ownership checks.
7. Ticket creation and modification information is retained.
8. Data is persisted in SQLite by default, with PostgreSQL-compatible configuration.
9. Employees and Support Staff can add authorized comments, including on Closed tickets.

The original implementation deliberately excluded comments. They were added later as a separate, non-destructive enhancement recorded in commit `32e8c72`.

## Technologies

| Layer | Technology |
|---|---|
| Frontend | React 19, React Router 7, Vite 8, plain CSS |
| Backend | FastAPI, Uvicorn, Pydantic, pydantic-settings |
| Data access | SQLAlchemy 2 |
| Database | SQLite by default; PostgreSQL URL support through `DATABASE_URL` |
| Passwords | Argon2 through `argon2-cffi` |
| Sessions | Random opaque tokens stored as SHA-256 hashes in HttpOnly cookies |
| Time handling | UTC storage, Asia/Kolkata display |
| Tests | pytest, Starlette `TestClient`, httpx |

Version constraints are listed in [`backend/requirements.txt`](backend/requirements.txt) and [`frontend/package.json`](frontend/package.json). Verification used Python 3.14.7, Node.js 24.21.0, npm 11.19.0, and Vite 8.3.8.

## Project structure

```text
Employee-Support-Ticket-App/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── deps.py                 # authentication and role dependencies
│   │   │   └── routes/                 # auth, tickets, comments, dashboards
│   │   ├── core/                       # config, security, validation, time handling
│   │   ├── db/                         # engine, sessions, table creation
│   │   ├── models/                     # User, Ticket, Comment, UserSession
│   │   ├── schemas/                    # request/response models
│   │   ├── services/                   # business rules and queries
│   │   └── main.py                     # FastAPI app and error handlers
│   ├── scripts/
│   │   ├── create_support_staff.py
│   │   └── seed_sample_data.py
│   ├── tests/
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── api/client.js               # API wrapper
│   │   ├── auth/                       # auth context and route guard
│   │   ├── components/                 # shared UI, including CommentSection
│   │   ├── pages/                      # login, dashboards, ticket screens
│   │   └── styles/                     # theme, layout, components
│   ├── .env.example
│   ├── package.json
│   └── vite.config.js                  # dev server and /api proxy
├── evidence/                           # genuine browser screenshots
├── .env.example
├── PRODUCT_PROMPT.md
├── SPEC.md
├── PLAN.md
├── PROGRESS.md
└── Day4_Poojitha.md
```

The SQLite database file, `.env` files, Python caches, `node_modules`, and built frontend output are ignored by Git.

## Features and permissions

### Employee

- Register through the public registration page. Registration always creates an Employee account.
- Log in and log out using the shared login page.
- View a dashboard with ticket counts and the five newest own tickets.
- Create a ticket with title, description, category, and priority.
- View only tickets created by that Employee.
- Edit title, description, category, and priority on own tickets that are not Closed.
- Track the current status, creator, creation date, and last-updated date.
- View and add comments on own tickets, including Closed tickets.

### Support Staff

- Log in with an authorized account created by the initialization script or seeded locally.
- View a dashboard with counts for all tickets.
- View all tickets and individual ticket details.
- Search by title, description, or creator name. Search characters such as `%` and `_` are treated literally.
- Filter by status, category, and priority; clear filters to see all tickets.
- Advance status one step at a time: Open → In Progress → Resolved → Closed.
- View and add comments on any ticket, including Closed tickets.
- Log out securely.

Support Staff cannot edit ticket content, change the original creator, or change the creation date.

### Comments

- A comment is stored with a unique ID, ticket ID, author ID, content, and UTC creation timestamp.
- The ticket-detail page displays comments chronologically with author, role, and Asia/Kolkata timestamp.
- Empty or whitespace-only comments are rejected by the backend; valid content is trimmed before storage.
- Employees can access comments only on their own tickets. Support Staff can access comments on all tickets.
- Adding a comment does not change ticket status or `updated_at`.

### Permission summary

| Action | Employee | Support Staff |
|---|---|---|
| Public registration | Yes, Employee role only | No |
| View own dashboard / tickets | Yes | Not applicable |
| View all tickets | No | Yes |
| Create ticket | Yes | No |
| Edit ticket content | Own, non-Closed tickets only | No |
| Change ticket status | No | Yes, one forward step only |
| View comments | Own tickets only | All tickets |
| Add comments | Own tickets, including Closed | All tickets, including Closed |
| Create Support Staff account | No | Initialization script only |

Frontend route guards and hidden controls are convenience only. All permissions are enforced in backend services and dependencies.

## Prerequisites

Commands in this README use **Windows PowerShell** and assume they are run from the project root unless stated otherwise.

- Python 3.11+ recommended; verified with Python 3.14.7
- Node.js `^20.19.0` or `>=22.12.0`; verified with 24.21.0
- npm; verified with 11.19.0
- Git is optional for running the app but is used for the repository history

## Installation

From the project root:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r backend\requirements.txt
cd frontend
npm install
cd ..
```

Copy the example environment file if you want to change the application defaults:

```powershell
Copy-Item .env.example .env
```

`.env` is ignored by Git. Never commit real passwords, tokens, or database credentials.

## Environment configuration

The backend reads application settings from process environment variables or the root `.env` file through pydantic-settings.

| Variable | Default | Purpose |
|---|---|---|
| `DATABASE_URL` | `sqlite:///./support_tickets.db` | SQLAlchemy database URL. The relative SQLite file is created in the current working directory, so run commands from the project root. |
| `SESSION_COOKIE_NAME` | `support_tickets_session` | Name of the session cookie |
| `SESSION_TTL_HOURS` | `8` | Session lifetime in hours |
| `SECURE_COOKIES` | `false` | Set to `true` only when serving over HTTPS |
| `CORS_ORIGINS` | `http://localhost:5173,http://127.0.0.1:5173` | Comma-separated browser origins allowed to call the API |

For PostgreSQL, set a URL such as `postgresql+psycopg://user:password@host:5432/dbname` and install the chosen Python driver separately. The driver is not included in `backend/requirements.txt`, and PostgreSQL was not exercised by the automated test suite.

The Vite dev server proxies `/api` to `http://localhost:8000`, so `VITE_API_URL` is normally unnecessary. If the backend is hosted elsewhere, set `VITE_API_URL` in `frontend/.env` to the backend origin and ensure that origin is covered by `CORS_ORIGINS`.

The initialization scripts read `SUPPORT_STAFF_*` and `SEED_*` values from the **current shell environment** or prompt for them. Setting those credential variables only inside `.env` is not enough for those scripts; use PowerShell variables as shown below or leave them unset for prompts.

## Database setup and initialization

### Create tables

Tables are created automatically when the FastAPI application starts. The explicit command is optional and safe to rerun:

```powershell
.\.venv\Scripts\python.exe -m backend.app.db.init_db
```

This uses SQLAlchemy `create_all()`: it creates missing tables but does not delete existing data and does not migrate changed columns.

### Seed sample data

The seed script creates five sample tickets and two local demonstration accounts if they do not already exist. It is idempotent: repeated runs do not duplicate the sample tickets.

Preferred interactive form, which avoids keeping passwords in shell history:

```powershell
.\.venv\Scripts\python.exe -m backend.scripts.seed_sample_data
```

The script prompts separately for the Employee password and Support Staff password. Each must contain at least eight characters.

Alternative non-interactive form for a local demonstration:

```powershell
$env:SEED_EMPLOYEE_PASSWORD='ChooseAnEmployeePassword'
$env:SEED_SUPPORT_PASSWORD='ChooseASupportPassword'
.\.venv\Scripts\python.exe -m backend.scripts.seed_sample_data
Remove-Item Env:SEED_EMPLOYEE_PASSWORD, Env:SEED_SUPPORT_PASSWORD
```

Demo logins after seeding:

- Employee: `ravi@company.com`
- Support Staff: `support@company.com`

Use the passwords supplied to the seed command. These accounts are local demonstration data; choose different values for any non-local use.

### Create another Support Staff account

There is no public Support Staff registration page or API. Preferred interactive form:

```powershell
.\.venv\Scripts\python.exe -m backend.scripts.create_support_staff
```

The script prompts for the full name and email, then requests the password without displaying it. The password must contain at least eight characters. If the email already exists, the script makes no changes.

Alternative non-interactive form:

```powershell
$env:SUPPORT_STAFF_NAME='Support Admin'
$env:SUPPORT_STAFF_EMAIL='support2@company.com'
$env:SUPPORT_STAFF_PASSWORD='ChooseALongPassword'
.\.venv\Scripts\python.exe -m backend.scripts.create_support_staff
Remove-Item Env:SUPPORT_STAFF_NAME, Env:SUPPORT_STAFF_EMAIL, Env:SUPPORT_STAFF_PASSWORD
```

## Running the application

Start the backend from the project root:

```powershell
.\.venv\Scripts\python.exe -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000
```

Start the frontend in a second PowerShell terminal:

```powershell
cd frontend
npm run dev
```

Open <http://127.0.0.1:5173>. The backend API is available under <http://127.0.0.1:8000/api>, including `GET /api/health`.

Both terminal sessions must remain running while you use the app. The Vite frontend on port 5173 proxies `/api` requests to the FastAPI backend on port 8000. Stopping the backend does not close the browser page, but every API action will fail until the backend is running again.

## Troubleshooting: 502 when saving a ticket

If ticket creation shows **Could not save ticket** followed by **Request failed with status 502**, the frontend is running but cannot reach the backend. This is a connection/proxy error, not a ticket validation failure and not evidence of lost ticket data.

Check which services are listening:

```powershell
Get-NetTCPConnection -LocalPort 8000,5173 -State Listen -ErrorAction SilentlyContinue | Select-Object LocalPort,OwningProcess
```

A healthy local setup lists both ports. You should also be able to call the health endpoint directly:

```powershell
Invoke-RestMethod http://127.0.0.1:8000/api/health
```

Expected result:

```text
status
------
ok
```

Fix the problem by restarting the backend in its own terminal from the project root:

```powershell
.\.venv\Scripts\python.exe -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000
```

Leave that terminal open, then reload the browser page and try again. If the frontend also stopped, start it in a second terminal:

```powershell
cd frontend
npm run dev
```

Additional checks:

- Keep both servers running in separate terminals. Closing the terminal, ending a background session, or pressing Ctrl+C stops that service.
- Use `npm run dev`, not `npm run preview`, for the normal local setup. Only the dev-server configuration in `frontend/vite.config.js` defines the `/api` proxy.
- If `frontend/.env` defines `VITE_API_URL`, it must point to the backend origin, normally `http://127.0.0.1:8000`, or be left blank. A wrong value bypasses the proxy and can cause API failures.
- If port 8000 is occupied by an old process, identify it with the `Get-NetTCPConnection` command above. Stop only a stale process belonging to this app, then start the backend again.
- The browser may sign you out after a 502 because the session check also fails. Sign in again after restoring the backend.

This exact 502 was reproduced during verification by leaving the frontend running while the backend was stopped. The same form then created a ticket successfully after the backend was restarted.

## API summary

All routes except registration and login require the session cookie.

| Method | Path | Access | Purpose |
|---|---|---|---|
| `POST` | `/api/auth/register` | Public, Employee only | Register an Employee |
| `POST` | `/api/auth/login` | Public | Log in and set session cookie |
| `GET` | `/api/auth/me` | Authenticated | Return current user |
| `POST` | `/api/auth/logout` | Authenticated | Revoke session and clear cookie |
| `GET` | `/api/employee/dashboard` | Employee | Employee counts and recent tickets |
| `GET` | `/api/employee/tickets` | Employee | List own tickets |
| `POST` | `/api/tickets` | Employee | Create ticket |
| `GET` | `/api/tickets/{id}` | Owner or Support Staff | Ticket detail |
| `PATCH` | `/api/tickets/{id}` | Owner, non-Closed | Edit ticket content |
| `POST` | `/api/tickets/{id}/status` | Support Staff | Advance status one step |
| `GET` | `/api/tickets/{id}/comments` | Owner or Support Staff | List comments chronologically |
| `POST` | `/api/tickets/{id}/comments` | Owner or Support Staff | Add trimmed, non-empty comment; returns HTTP 201 |
| `GET` | `/api/support/dashboard` | Support Staff | All-ticket counts |
| `GET` | `/api/support/tickets` | Support Staff | Search and filter all tickets |

Example comment request body:

```json
{ "content": "Please check the power cable." }
```

## Tests and build

Run the backend suite from the project root:

```powershell
.\.venv\Scripts\python.exe -m pytest backend/tests -v
```

Recorded after the 502 investigation on 18 Nov 2026:

```text
28 passed, 1 warning in 15.26s
```

The warning is a Starlette `TestClient`/httpx deprecation notice, not a test failure. Tests use a separate `test_support_tickets.db` that is reset between tests; they do not depend on the seeded demonstration database.

Coverage includes registration and login validation, ownership and role enforcement, HTTP status and check order, ticket create/edit/status rules, Closed-ticket restrictions, persistence, constraints, idempotent seeding, literal SQL LIKE wildcards, and comment authorization, ownership, validation, order, Closed tickets, unauthenticated access, and status preservation.

Build the frontend for production:

```powershell
cd frontend
npm run build
```

Recorded result: Vite 8.3.8 successfully transformed 46 modules and wrote the production output to `frontend/dist`.

At the time of review, `npm audit` reported five high-severity advisories in the Vite development dependency chain (`picomatch`, `fdir`, `tinyglobby`, `vite`, and `@vitejs/plugin-react`). `npm audit fix --force` proposed a breaking downgrade to Vite 6.2.7; it was not applied because the current toolchain builds successfully.

## Authentication and security

- One login page serves both roles; the frontend never assigns the authenticated role.
- Public registration creates Employee accounts only. Any client-supplied role value is ignored by the backend.
- Support Staff accounts are created only by the trusted initialization script or local seed script.
- Passwords are validated, confirmed exactly, and hashed with Argon2. Plain passwords are never stored or returned. Passwords are never trimmed.
- Email addresses are trimmed and lowercased for uniqueness and login. Names, ticket titles, descriptions, and comments are trimmed.
- Login creates a random opaque token. Only its SHA-256 hash is stored in the database.
- The token is sent in a cookie with `HttpOnly` and `SameSite=Lax`; the `Secure` flag is controlled by `SECURE_COOKIES` and should be enabled behind HTTPS.
- Each protected request resolves the user and role from the database. Expired or revoked sessions are rejected. Logout revokes the session and clears the cookie.
- Backend validation runs after authentication, ticket existence, and authorization checks. Invalid input returns HTTP 400; unauthenticated requests return 401; unauthorized requests return 403; missing tickets return 404.
- Ticket ownership is checked in backend services, including comment routes. Frontend hiding is not relied on for security.
- Support search escapes user-supplied SQL LIKE metacharacters so `%` and `_` are treated literally.
- Database constraints enforce non-empty titles/descriptions/comments and valid enums. Registration integrity errors are rolled back.
- FastAPI error handlers return consistent JSON messages and do not expose stack traces, password hashes, or other Employees' ticket contents.
- CORS accepts credentials only from the configured origins.

## Evidence and verification record

Genuine browser captures were saved at an 800 px viewport in [`evidence/`](evidence):

- [Login screen](evidence/02-login.png)
- [Employee dashboard](evidence/01-employee-dashboard.png)
- [Support ticket list](evidence/03-support-tickets.png)

The assisted-session browser smoke record in [`Day4_Poojitha.md`](Day4_Poojitha.md) reports:

- Employee and Support Staff login, dashboard counts, ticket creation, editing, and Closed-ticket edit restriction passed.
- Support search (`VPN`), `Resolved` status filter, Clear, and status advance passed.
- Registration passed.
- Direct Employee access to Support pages returned 403; unknown routes returned 404.
- Access to another Employee's ticket returned 403 from the backend; a missing ticket returned 404.
- No horizontal overflow was detected at 800 px (`scrollWidth` 785 ≤ `innerWidth` 800).
- Comment checks passed for Support Staff on In Progress and Closed tickets and for the owning Employee on a Closed ticket. Whitespace was trimmed, author and timestamp were displayed, chronological order was maintained, and ticket status and `updated_at` stayed unchanged.
- No comment-section console errors or overflow were detected.
- After the 502 investigation, both servers were restarted and ticket creation was repeated in the browser. The request returned HTTP 201 and opened the new ticket detail page. Browser console errors were none.

[`PROGRESS.md`](PROGRESS.md) records the commands, results, defects, and pending items in more detail. No dedicated comment-section screenshot was captured, and no screenshots were fabricated.

## Authorship, decisions, and personal verification

The repository records the following attribution. These statements are based on [`Day4_Poojitha.md`](Day4_Poojitha.md), not on assumptions about who ran later commands.

### AI-generated

- The finalized specification and implementation plan.
- All backend and frontend application code.
- Scripts, automated tests, and initial documentation, including the original README and submission document.
- The later Ticket Comments enhancement: its model, schema, service, API routes, tests, frontend component, and related documentation changes.

### User-supplied or decided

- The original product prompt and the later Ticket Comments enhancement prompt.
- Approval of review decisions RD-01 through RD-16 and technical decisions TD-01 through TD-05.
- Requests to implement the application, keep `SPEC.md` and `PLAN.md` as the source of truth, add comments separately, and commit with the exact message `Add ticket comments enhancement`.
- No additional manual source-code edits were reported in the submission record.

### Personally tested and verified by the repository owner

No record in the repository identifies any specific command, browser check, or screenshot as personally performed by the repository owner. Therefore, this README does not claim personal testing on that person's behalf. The recorded verification above was performed during the assisted implementation and review sessions and is described by command output, browser observations, and the linked evidence.

## Known limitations and remaining gaps

- No GitHub remote was configured at the time of writing, so the submission record lists the GitHub link as Pending.
- Screenshots beyond the 800 px browser viewport are not available. A dedicated comment-section screenshot is also unavailable.
- PostgreSQL configuration exists, but automated tests and the recorded runtime checks used SQLite.
- There is no schema migration tool; `create_all()` creates missing tables but does not migrate existing columns.
- `npm audit` development-dependency advisories remain unresolved. The production build succeeds, and the Vite development server should not be exposed to untrusted networks.
- Email/SMS notifications, AI classification, chat, payments, password reset, email verification, rate limiting, audit logs, and enterprise administration features are outside the implemented scope.
- Comments have no maximum-length rule or edit/delete workflow.

## Git history

Verified project checkpoints:

| Commit | Description |
|---|---|
| `b23edea` | FastAPI backend, database layer, authentication, ticket APIs, and tests |
| `ecc49a8` | React frontend and browser evidence |
| `9453886` | Literal LIKE wildcard search defect fix |
| `5c44034` | Final setup, verification, and submission documentation |
| `32e8c72` | Ticket Comments enhancement |
