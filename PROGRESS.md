# Progress

## Completed

- Finalized `SPEC.md` and created `PLAN.md` before implementation (no application code was written before approval).
- Created backend foundation: configuration, UTC/Asia-Kolkata time helpers, Argon2 password hashing, hashed server-side sessions, validation, SQLAlchemy models, relationships, constraints, session management, and table initialization.
- Implemented authentication API: registration, login, `/me`, logout with session revocation, and role-aware dependencies.
- Implemented Employee APIs: create ticket, list own tickets, read own ticket, edit permitted fields, and employee dashboard.
- Implemented Support Staff APIs: list all tickets, search/filter, read any ticket, status transitions, and support dashboard.
- Enforced required error order: authentication → missing ticket → authorization → invalid input.
- Added idempotent sample-data and Support Staff initialization scripts with passwords supplied by environment variables or interactive prompts.
- Added automated backend tests covering authentication, validation, permissions, ownership, ticket operations, status transitions, dashboards, search/filters, persistence, constraints, and idempotent seeding.
- Fixed genuine defect found during verification: SQLite table creation failed because a check constraint used `char_length()`; replaced it with portable `length()` and retested successfully.

## Verification

Command:

```powershell
.venv\Scripts\python.exe -m pytest backend/tests -v
```

Result on 18 Nov 2026: **21 passed, 1 warning** (the warning is a Starlette TestClient/httpx deprecation notice, not a test failure).

## Pending

- Build the React + Vite frontend and integrate it with the API.
- Verify responsive layout and every visible control in a browser.
- Add frontend build/manual checks and record genuine results.
- Write `README.md`.
- Exercise and document one additional genuine defect if one is found during frontend/review work; the database constraint defect above is already recorded as the required defect report candidate.
- Create `Day4_Poojitha.md` with product prompt, specification, plan, prompts, genuine evidence, defect report, test results, review notes, and GitHub link. Mark missing screenshots/evidence as Pending rather than inventing them.

## Commands

```powershell
python -m venv .venv
.venv\Scripts\python.exe -m pip install -r backend\requirements.txt
.venv\Scripts\python.exe -m pytest backend/tests -v
.venv\Scripts\python.exe -c "from backend.app.db.session import create_tables; create_tables(); print('tables ok')"
```

## Next step

Stage and commit the verified backend milestone, then scaffold the React + Vite frontend and integrate the login, Employee, and Support Staff screens.
