# Progress

## Completed

- Finalized `SPEC.md` and created `PLAN.md` before implementation; no application code was written before approval.
- Built and verified the FastAPI/SQLAlchemy backend with SQLite/PostgreSQL-compatible configuration, Argon2 password hashing, hashed server-side sessions, backend-enforced RBAC, ticket workflows, dashboards, search/filters, idempotent seed scripts, and safe error handling.
- Built and verified the React + Vite frontend with login, registration, Employee dashboard/tickets/create/edit/detail, Support dashboard/tickets/detail, role guards, responsive navigation, badges, alerts, and functional filters/status actions.
- Captured genuine browser screenshots in `evidence/`: login, employee dashboard, support ticket list.
- Fixed two genuine defects:
  1. SQLite table creation failed because a check constraint used `char_length()`; changed to portable `length()` and retested.
  2. Support search treated `%` and `_` as SQL LIKE wildcards, so searching `%` returned every ticket. Escaped user-supplied LIKE metacharacters and added a regression test.
- Wrote `README.md` and `Day4_Poojitha.md` with setup, run, and test instructions; prompt/spec/plan references; genuine browser evidence; defect reports; review notes; and explicitly Pending gaps.
- Implemented the separately requested Ticket Comments enhancement:
  - Added `Comment` model, schema, service, and REST endpoints without rebuilding existing modules.
  - Employees can comment on their own tickets; Support Staff can comment on any ticket.
  - Both roles can view authorized comments, including on Closed tickets.
  - Added backend validation for empty/whitespace-only comments and stored trimmed content.
  - Added a styled, functional comment section to ticket details with chronological display, author, role, and timestamp.
  - Added six backend tests covering both roles, ownership, Closed tickets, validation, order, status preservation, unauthenticated access, and missing-ticket error order.

## Defect 2 Record

- Reproduction: sign in as Support Staff, call `GET /api/support/tickets?search=%25` with two existing tickets, or run `test_search_treats_sql_like_wildcards_literally`.
- Expected: no tickets, because no title, description, or creator contains a literal `%`.
- Actual before fix: both tickets were returned. The pre-fix regression test failed.
- Cause: the search pattern was built directly from user input and passed to SQLAlchemy `ilike()` without escaping LIKE metacharacters.
- Fix: escape backslash, `%`, and `_` in the search term and pass `escape="\\"` to each `ilike()` comparison.
- Retest: full backend suite passes with 28 tests, including the new regression test.

## Verification

Backend command:

```powershell
.venv\Scripts\python.exe -m pytest backend/tests -v
```

Current result on 18 Nov 2026: **28 passed, 1 warning** (Starlette TestClient/httpx deprecation notice only).

Frontend command:

```powershell
cd frontend
npm run build
```

Current result on 18 Nov 2026: build succeeded with Vite 8.3.8.

Browser smoke results on 18 Nov 2026 at an 800 px viewport:

- Employee login and seeded dashboard showed 5 tickets with correct counts and Asia/Kolkata times.
- Create ticket saved a new ticket and opened its detail page.
- Edit ticket saved changes and updated Last Updated Date.
- Closed ticket detail showed no Edit control.
- Support login showed dashboard counts and all tickets.
- Support search (`VPN`), status filter (`Resolved`), Clear, and status advance all worked.
- Registration created an employee and showed a success message on the login page.
- Employee direct access to `/support` redirected to 403; unknown route showed 404.
- Employee direct access to another employee's ticket showed the backend 403 message; missing ticket showed 404.
- No horizontal page overflow was detected at 800 px (`documentElement.scrollWidth` 785 <= `window.innerWidth` 800).
- Comment smoke test: Support Staff added a trimmed comment to an In Progress ticket; status and Last Updated Date remained unchanged.
- Comment smoke test: Support Staff added a comment to a Closed ticket; status remained Closed.
- Comment smoke test: the owning Employee saw both comments and added a trimmed comment on the Closed ticket; no console errors and no horizontal overflow were detected.

`npm audit` reports high-severity advisories in Vite's development-server dependency chain (`picomatch`/`fdir`/`tinyglobby`) with no non-vulnerable published `picomatch` version available. These are development-only dependencies; the production build succeeds. This remains a known dependency-review gap.

## Pending / Known gaps

- GitHub link: Pending — no remote was configured in this workspace.
- Screenshots at desktop and phone widths beyond 800 px: Pending — no evidence was fabricated.
- A dedicated screenshot of the comment section: Pending — the browser capture tool was unavailable during the comment smoke test.
- PostgreSQL runtime test: Pending — configuration supports `DATABASE_URL`, but automated verification used SQLite.
- `npm audit` development-dependency advisories remain unresolved because no fixed published `picomatch` version is available.

## Commands

```powershell
python -m venv .venv
.venv\Scripts\python.exe -m pip install -r backend\requirements.txt
.venv\Scripts\python.exe -m pytest backend/tests -v
$env:SEED_EMPLOYEE_PASSWORD='EmployeeSeed123'; $env:SEED_SUPPORT_PASSWORD='SupportSeed123'; .venv\Scripts\python.exe -m backend.scripts.seed_sample_data
.venv\Scripts\python.exe -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000
cd frontend
npm install
npm run dev
npm run build
```

## Next step

Commit the verified Ticket Comments enhancement with the required commit message, then submit the repository. Add the GitHub remote/link and missing screenshots if those become available.
