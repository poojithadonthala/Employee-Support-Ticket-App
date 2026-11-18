# Progress

## Completed

- Finalized `SPEC.md` and created `PLAN.md` before implementation; no application code was written before approval.
- Built and verified the FastAPI/SQLAlchemy backend with SQLite/PostgreSQL-compatible configuration, Argon2 password hashing, hashed server-side sessions, backend-enforced RBAC, ticket workflows, dashboards, search/filters, idempotent seed scripts, and safe error handling.
- Built and verified the React + Vite frontend with login, registration, Employee dashboard/tickets/create/edit/detail, Support dashboard/tickets/detail, role guards, responsive navigation, badges, alerts, and functional filters/status actions. Comments are not present.
- Captured genuine browser screenshots in `evidence/`: login, employee dashboard, support ticket list.
- Fixed two genuine defects:
  1. SQLite table creation failed because a check constraint used `char_length()`; changed to portable `length()` and retested.
  2. Support search treated `%` and `_` as SQL LIKE wildcards, so searching `%` returned every ticket. Escaped user-supplied LIKE metacharacters and added a regression test.

## Defect 2 Record

- Reproduction: sign in as Support Staff, call `GET /api/support/tickets?search=%25` with two existing tickets, or run `test_search_treats_sql_like_wildcards_literally`.
- Expected: no tickets, because no title, description, or creator contains a literal `%`.
- Actual before fix: both tickets were returned. The pre-fix regression test failed.
- Cause: the search pattern was built directly from user input and passed to SQLAlchemy `ilike()` without escaping LIKE metacharacters.
- Fix: escape backslash, `%`, and `_` in the search term and pass `escape="\\"` to each `ilike()` comparison.
- Retest: full backend suite passes with 22 tests, including the new regression test.

## Verification

Backend command:

```powershell
.venv\Scripts\python.exe -m pytest backend/tests -v
```

Result on 18 Nov 2026: **22 passed, 1 warning** (Starlette TestClient/httpx deprecation notice only).

Frontend command:

```powershell
cd frontend
npm run build
```

Result on 18 Nov 2026: build succeeded with Vite 8.3.8.

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

`npm audit` reports high-severity advisories in Vite's development-server dependency chain (`picomatch`/`fdir`/`tinyglobby`) with no non-vulnerable published `picomatch` version available. These are development-only dependencies; the production build succeeds. This remains a known dependency-review gap.

## Pending

- Write `README.md` with setup, run, test, and known-gap details.
- Create `Day4_Poojitha.md` with product prompt, specification, plan, prompts, genuine evidence, defect report, test results, review notes, and GitHub link. Mark missing screenshots/evidence as Pending rather than inventing them.
- Final full test run and final documentation commit.

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

Commit the verified defect fix separately, then write the final documentation and run one final verification pass.
