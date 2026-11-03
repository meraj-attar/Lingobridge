# LingoBridge — Post-Removal Focused Test Report

**Date:** 31 October 2026  
**Source:** Supplied `LingoBridge_Final_Release_Candidate_QA.zip` with voice-only cleanup.  
**Database safety:** No connection to the user's PostgreSQL database. The supplied pytest test fixtures create a disposable local SQLite database.

| Check | Result | Evidence / qualification |
|---|---|---|
| ZIP source integrity before extraction | **PASS** | Python `zipfile.testzip()` returned `None`; 209 entries in original source archive |
| Python compilation | **PASS** | `python -m compileall -q backend/app backend/scripts backend/tests` returned success |
| Backend pytest | **PASS — 110 tests** | `CLEANUP_EVIDENCE/backend_pytest.log` — 110 passed in isolated SQLite fixture |
| Node built-in tests | **PASS — 34 tests** | `CLEANUP_EVIDENCE/node_tests.log` — 34 passed |
| FastAPI import/startup | **PASS** | TestClient started with disposable SQLite URL, health route 200 and `/openapi.json` 200 |
| Retired TTS/API endpoints | **PASS** | No registered `/api/pronunciation`, `/api/pronunciation/status`, `/api/admin/audio`, or `/api/media` routes; requests return 404 |
| Ten-language inventory and core API | **PASS within tests** | Existing backend suite and new `test_voice_removal.py` check all ten languages |
| Authentication/course/lesson/vocabulary/quiz/flashcard/admin API regression | **PASS within tests** | Backend 110-test suite; not a production Postgres test |
| Static frontend relative-import integrity | **PASS** | `CLEANUP_EVIDENCE/import_reference_check.json`: 59 source JS/JSX files, zero unresolved local imports |
| React JS/JSX syntax parse | **PASS** | `CLEANUP_EVIDENCE/jsx_parse.log`: 59 files parsed, zero errors via locally installed TypeScript parser |
| Voice UI and hook removal assertions | **PASS** | `tests/voice-removal.test.mjs` and `CLEANUP_EVIDENCE/node_tests.log` |
| `npm ci` | **BLOCKED** | Supplied source ZIP has no `package-lock.json`; see `CLEANUP_EVIDENCE/npm_ci.log` |
| `npm install --offline` | **BLOCKED** | npm cache lacks registry metadata for `@playwright/test` (`ENOTCACHED`); see log |
| `npm install` online attempt | **BLOCKED / timed out** | Registry-bound install did not finish within 22 seconds and created no lockfile or modules; `CLEANUP_EVIDENCE/npm_install_online.log` |
| `npm run build` | **BLOCKED** | Vite is not installed locally (`vite: not found`); build **was not successful** |
| `npm run test:frontend` | **BLOCKED** | Vitest is not installed locally (`vitest: not found`) |
| Physical React browser acceptance | **NOT RUN** | Cannot launch a Vite build without installed dependencies |
| Real PostgreSQL verification | **NOT RUN** | Intentionally not connected to populated PostgreSQL; no disposable PostgreSQL staging service used |
| Actual Windows execution | **NOT RUN** | Windows commands supplied for user-side testing |

## Focused regression scope

- Removed voice/upload/media APIs return **404**, and `/api/health` and language inventory still function.
- New frontend checks verify no speech hooks, audio uploads, speaker icons or playback buttons remain in student learning screens or admin vocabulary.
- Existing integration tests exercise login, JWT/CSRF, enrollments, lessons, vocabulary, quizzes, MCQ limits, flashcards, spaced repetition, admin APIs, and ten-language inventory. The suite's 110 passes are **actual executions**, not copied counts from old reports.
- Core language-learning files (`backend/data/legacy_seed.json` and curriculum modules), migrations, and security modules were preserved.

## Windows follow-up

In a network-connected Windows PowerShell environment, use `WINDOWS_SETUP.md`; run `npm install` (to create a missing lockfile), `npm run build`, `npm run test:frontend`, and manually verify student and admin pages. Confirm absence of speaker buttons and audio management, and preserve the actual database and `.env` while upgrading.

**Decision:** Source cleanup and focused backend/Node regression suite passed. **Final frontend/build/browser and production deployment readiness remain unverified.**
