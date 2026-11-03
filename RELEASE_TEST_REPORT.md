# LingoBridge — release regression and acceptance evidence

Date: 30 October 2026. **This is not a production-ready or completely browser-verified release.** All counts below refer to this new updated source; older figures in the supplied independent QA pack refer to the previous baseline.

## Executed automated tests

| Verification | Result | Evidence |
|---|---|---|
| Original and new Python/pytest suite | **PASS: 114/114** | `RELEASE_EVIDENCE/BACKEND_PYTEST.log` |
| Existing and new Node built-in tests | **PASS: 35/35** | `RELEASE_EVIDENCE/FRONTEND_NODE_TESTS.log` |
| Python compileall | **PASS** | Execution log |
| Frontend JS/JSX syntax parse | **PASS: 62 files, zero parser errors** | `RELEASE_EVIDENCE/FRONTEND_SOURCE_INVENTORY.log` |
| Defect pre-fix reproduction | **CONFIRMED 3/3** | Original source inspected; pre-fix responses: 200, 201, 200 |
| Defect post-fix API and stored data | **PASS 3/3** | `RELEASE_EVIDENCE/REPRODUCED_FIXES.log` |
| Original tests retained | **PASS** | Original ZIP versus release file manifest |
| Existing user PostgreSQL | **NOT CONNECTED / UNMODIFIED** | Tests seed isolated SQLite only |

**Total tests executed in the final automated suites:** **149 passed, 0 failed** (114 pytest + 35 Node). Do not add source syntax files or the three independent HTTP rechecks to this total; they are reported separately to avoid double counting. Within the 114 Python tests, 67 are new focused regression cases. All existing backend pytest tests still pass.

### New backend scenarios

- Delete incorrect option from 3-choice MCQ: accepted; then deleting from 2-choice MCQ: rejected and state unchanged.
- Existing 1-choice legacy MCQ cannot be reduced further but can accept a new second distractor.
- Eight-choice MCQ cannot accept ninth; seventh-to-eighth works; answer key remains unique.
- Full-question editor rejects 0, 1, 9, 10 choices; rejects 0 or 2 correct answers.
- Option patch rejects empty text, second correct answer, moving option between questions.
- Allowed YouTube HTTPS formats and over twenty invalid/hostile URL forms checked at parser and backend PATCH boundary; rejected writes preserve the stored original.
- Admin lesson creation validates URL; empty string can clear URL; unauthorized student/guest admin writes rejected.

### Frontend automated scenarios

- Node tests cover safe/unsafe URL matching, deceptive host rejection, missing and malformed IDs, unsupported schemes, query duplication, and sanitized YouTube embed construction.
- Frontend JSX parsed using a local TypeScript compiler (syntax only, not a bundler). Current checklist identifies **267 source-level interactive elements across 21 routes**. The 267 count is **not browser clicks**.

## Blocked / not executed checks

| Criterion | Status | Reason / next step |
|---|---|---|
| Clean npm dependency installation | **BLOCKED** | Missing npm cache and registry fetch not completed; see install logs |
| Vite production build | **BLOCKED** | `vite` missing because npm dependencies unavailable |
| Vitest React frontend tests | **BLOCKED** | Vitest missing |
| Playwright full 21-route browser click-through | **BLOCKED** | UI cannot be launched without React dependencies |
| 267 individual source controls physically clicked | **NOT RUN** | `BROWSER_ACCEPTANCE_CHECKLIST.csv` covers each |
| Windows responsive tablet/mobile visual QA | **NOT RUN** | No live Vite app |
| Multi-request PostgreSQL concurrency | **NOT RUN** | No separate disposable PostgreSQL staging instance |
| Production PostgreSQL migration verification | **NOT APPLICABLE / NOT RUN** | No new migration, user DB intentionally untouched |
| Actual local Piper/eSpeak synthesis | **BLOCKED** | Neither engine/compatible voice available in this environment |
| Audible 10-language pronunciation review | **NOT RUN** | Requires real compatible voice installations and human listening |

### Pronunciation voice inventory

| Language | Locale | Piper configured | eSpeak available | Browser voice | Real spoken test |
|---|---|---|---|---|---|
| English | en-US | No | No | Device-dependent | NOT RUN |
| Hindi | hi-IN | No | No | Device-dependent | NOT RUN |
| Marathi | mr-IN | No | No | Device-dependent | NOT RUN |
| Gujarati | gu-IN | No | No | Device-dependent | NOT RUN |
| Bengali | bn-IN | No | No | Device-dependent | NOT RUN |
| Tamil | ta-IN | No | No | Device-dependent | NOT RUN |
| Telugu | te-IN | No | No | Device-dependent | NOT RUN |
| Kannada | kn-IN | No | No | Device-dependent | NOT RUN |
| Urdu | ur-PK | No | No | Device-dependent | NOT RUN |
| Spanish | es-ES | No | No | Device-dependent | NOT RUN |

Four existing bundled demonstration recordings were previously decoded in baseline tests; that is not evidence of working 10-language neural TTS. This release does not reassign fake audio or use paid Azure.

## Release gate

The three reproduced defects are fixed and validated in SQLite. **Do not label this a fully QA-verified production build** until npm/Vite/Vitest, browser scenarios, independent PostgreSQL concurrency tests, and spoken pronunciation acceptance are completed on Windows/staging.
