> **Historical QA document (pre-TTS removal).** For this cleaned build use `../WINDOWS_SETUP.md`, `../CLEANUP_TEST_REPORT.md` and `../CLEANUP_MANIFEST.md`. Voice setup instructions here are obsolete.

# LingoBridge — Windows Installation and Acceptance Guide

## 1. Protect your existing learning database

**Do not run seed, reset, migrations or tests against your populated PostgreSQL database.** Back it up before any later installation/change. This archive was processed without connecting to that database. The migrations in source are unchanged; existing head `0004`. Preserve your own `backend/.env`, local media, secrets and database files outside overwrite operations.

## 2. Supported toolchain and clean checkout

Install **Python 3.11.6**, Node.js 20+ with npm, and PostgreSQL 17 (if using a separate fresh staging database). Open PowerShell in the extracted `lingobridge` root. Review `backend/.env.example`; create a fresh, private `.env` only on a brand-new isolated instance. Do not paste database credentials or JWT secrets into reports or commits.

```powershell
py -3.11 --version
node --version
npm --version
cd backend
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m pytest -q tests
python -m compileall -q app scripts tests
cd ..
npm test
```

### Known frontend packaging blocker — no npm lockfile in uploaded release

The provided ZIP did **not** include `package-lock.json`. Accordingly **`npm ci` cannot run immediately** even on a working Internet connection. On a trusted Windows machine with registry access, do **not** delete or fake a lockfile. If there genuinely is no lockfile, generate it using:

```powershell
npm install --package-lock-only
npm ci
npm run build
npm run test:frontend
npm test
```

Keep and version-control the generated `package-lock.json` with this candidate once its installation and dependency audit succeed. If installation fails, capture the full npm error and correct actual dependencies rather than claiming PASS. A successful build creates `dist/` and should exit 0. Do not count a syntax parser run as equivalent.

## 3. Start isolated demo instance

For a **fresh isolated PostgreSQL staging database only**, explicitly set a new test `DATABASE_URL`, a 32+ character `JWT_SECRET`, `ENVIRONMENT=development`, and `FRONTEND_ORIGIN=http://localhost:5175`. Verify the exact DB name with an admin before applying migrations or seeding. Do not reuse the connection string of the populated app.

Open terminal A:

```powershell
cd backend
.\.venv\Scripts\Activate.ps1
python -m uvicorn app.main:app --host 127.0.0.1 --port 8003
```

Terminal B from root:

```powershell
npm run dev -- --host 127.0.0.1 --port 5175
```

Start with `http://127.0.0.1:5175` and confirm the HTTP `/api/health` response through the proxy.

## 4. Browser acceptance tests

Use `QA_FINAL/BROWSER_ACCEPTANCE_CHECKLIST.csv` **all 267 rows**, at desktop 1440 px, tablet 768 px and mobile 390 px. This review covered 21 app routes plus shared-component controls. Keep a spreadsheet with actual outcome, timestamps and browser console/API traces. Test temporary user registration/login, language selection, lessons, full quiz flow and scoring, flashcards, bookmarks, progress persistence across logout/login, and real admin student/content/video/audio management. Test negative validation, unauthorized access, duplicate submit, empty/loading/error states, and browser navigation. Mark only physically run cases PASS.

For browser automation, configure Playwright browsers on Windows **after npm installation**, then run `npx playwright install chromium` followed by `npm run test:e2e` against running, isolated frontend/backend. Existing E2E scripts are a starting point, not proof that all 267 controls were tested.

## 5. Staging database and audio

Follow `POSTGRESQL_STAGING_TEST_REPORT.md` for a genuinely disposable PostgreSQL 17 DB and concurrency/FK assertions; do not use production student data. For voice installs, follow `TTS_VERIFICATION_REPORT.md` and existing audio guides, then perform human listening to each of the ten languages.

## 6. Final release gate

Only mark demo PASS once clean frontend install, production build, frontend automated tests, backend regression, and real student/admin browser workflows all pass without high-severity defects. Production additionally requires persistent session revocation, multi-worker rate limiting, PostgreSQL staging concurrency, performance/security checks, real voices and version-locked dependencies.
