# Progress

## Completed

- Finalized `SPEC.md` and created `PLAN.md` before implementation; no application code was written before approval.
- Built and verified the FastAPI/SQLAlchemy backend with SQLite/PostgreSQL-compatible configuration, Argon2 password hashing, hashed server-side sessions, backend-enforced RBAC, ticket workflows, dashboards, search/filters, idempotent seed scripts, and safe error handling.
- Fixed a genuine SQLite defect found during verification: table creation used `char_length()` and failed; replaced with portable `length()` and retested.
- Built the React + Vite frontend with login, registration, Employee dashboard/tickets/create/edit/detail, Support dashboard/tickets/detail, role guards, responsive navigation, badges, alerts, and functional filters/status actions. Comments are not present.
- Verified the frontend with `npm run build` and a live browser smoke test against the running backend.
- Captured genuine browser screenshots in `evidence/`: login, employee dashboard, support ticket list.

## Verification

Backend command:

```powershell
.venv\Scripts\python.exe -m pytest backend/tests -v
```

Result on 18 Nov 2026: **21 passed, 1 warning** (Starlette TestClient/httpx deprecation notice only).

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

- Add and commit a separately verified defect fix for literal handling of `%` and `_` in Support Staff search.
- Write `README.md` with setup, run, test, and known-gap details.
- Create `Day4_Poojitha.md` with product prompt, specification, plan, prompts, genuine evidence, defect report, test results, review notes, and GitHub link. Mark missing screenshots/evidence as Pending rather than inventing them.
- Final full test run and final documentation commit.

## Commands

```powershell
python -m venv .venv
.venv\Scripts\python.exe -m pip install -r backend\requirements.txt
.venv\Scripts\python.exe -m pytest backend/tests -v
.venv\Scripts\python.exe -m backend.scripts.seed_sample_data
.venv\Scripts\python.exe -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000
cd frontend
npm install
npm run dev
npm run build
```

## Next step

Commit the verified frontend milestone, then add the search-wildcard regression test, fix, retest, and commit that defect fix separately.
