# Detailed Independent Test Execution Report

## Verified environment

- Linux sandbox; Python **3.13.5** (NOT the user-targeted 3.11.6), Node.js **22.16.0**, npm **10.9.2**.
- Installed Python packages differ from the reported pinned release stack: FastAPI 0.128.2; SQLAlchemy 2.0.50; Alembic 1.18.4; PyJWT 2.13.0; Pydantic 2.13.5; pytest 9.0.2. Python dependencies in `backend/requirements.txt` use ranges, not exact pins. These observations do not prove compatibility with PostgreSQL 17.10 or exact Windows runtime versions.
- No Node dependencies installed; npm registry DNS lookup produced `EAI_AGAIN`; original source ZIP contains no lockfile. `psycopg`, PostgreSQL server/client, Piper/eSpeak NG and native browser-running frontend were unavailable. A Chromium binary exists, but no running React app could be launched.
- Tests use `backend/tests/test_integration.py` disposable temporary SQLite fixture, never the configured user database.

## Command / outcome / raw proof

| Action | Result | Raw evidence |
|---|---|---|
| `ZipFile.testzip()` on supplied archive | PASS; 182 entries | `ZIP_AND_HASHES.json` |
| `python -m compileall -q backend` | PASS | `../NEW_QA_EVIDENCE/compileall.log` |
| `cd backend && python -m pytest -q tests` before modifications | PASS, 114 tests | `../NEW_QA_EVIDENCE/pytest.log` |
| `npm test` before/after changes | PASS, 35 tests | `../NEW_QA_EVIDENCE/npm_test_final.log` |
| `cd backend && python -m pytest -q tests` after improvements | PASS, **122 tests** | `../NEW_QA_EVIDENCE/pytest_final.log` |
| TypeScript compiler syntax parse (`createSourceFile`) on 74 JS/JSX files | PASS; no parser errors | `../NEW_QA_EVIDENCE/JSX_PARSE.log` |
| `npm install --package-lock-only --fetch-retries=0` | BLOCKED, DNS **EAI_AGAIN** | `../NEW_QA_EVIDENCE/npm_lock_generation.log` |
| `npm ci --offline` | FAIL (preexisting missing lockfile, **EUSAGE**) | `../NEW_QA_EVIDENCE/npm_ci.log` |
| `npm run build` | BLOCKED (`vite: not found`) | `../NEW_QA_EVIDENCE/build.log` |
| `npm run test:frontend` | BLOCKED (`vitest: not found`) | `../NEW_QA_EVIDENCE/vitest.log` |
| Independent clean SQLite seeding and curriculum counts | PASS | `../NEW_QA_EVIDENCE/CONTENT_COUNTS.json` |
| All 267 browser checklist clicks | NOT RUN | `BROWSER_ACCEPTANCE_CHECKLIST.csv` |
| PostgreSQL concurrency and real migration | NOT RUN | `POSTGRESQL_STAGING_TEST_REPORT.md` |
| Actual ten-language voice synthesis / human listening | NOT RUN | `TTS_VERIFICATION_REPORT.md` |
| `run_all_checks.ps1` | NOT RUN (PowerShell unavailable in Linux) | inspection of script only |

## Eight newly added backend tests

- Bounded page/search/sort/filter behavior, parameterized inputs, escaped literal wildcard, stable pagination, and no password-hash exposure in student listing.
- Legacy list response preserves type while supporting limit/offset and rejecting out-of-range parameters.
- Server-side admin permissions on new page endpoint, including a student denial.
- Five invalid or missing JWT claim sets rejected as HTTP 401 rather than an unhandled exception.

Existing release regressions continue to cover **MCQ min=2/max=8**, answer uniqueness, transaction state on rejection, unsafe URL rejection on lesson create/update, and CSRF/admin access control.

## Test adequacy limitations

The expanded count is **122 backend + 35 Node = 157 executable checks**. It excludes the 74 syntax-only files, baseline reproduction duplicates, and the 267 unclicked browser controls. Vitest's current 2 test cases cannot be executed here. The Python suite's result proves the software works against its test SQLite fixture under this environment, not a Windows 3.11 + PostgreSQL deployment. `npm ci`, Vite build, browser tests, real audio and PostgreSQL tests remain acceptance blockers.
