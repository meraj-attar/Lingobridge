# Senior QA Final Audit and Release Verification

**Date:** 31 October 2026  
**Source:** User-supplied latest archive `LingoBridge_Final_Defect_Fixes_QA_Verified (1).zip` only.  
**Verdict:** **NOT READY FOR PRODUCTION; final demonstration acceptance BLOCKED until the frontend builds and core browser journeys pass.**

## Scope and independently established evidence

- Original ZIP: **182 entries; integrity PASS** (`ZipFile.testzip()` returned no corrupt item); original retained without overwriting. The nested previous evidence pack (19 files) also passed ZIP integrity.
- Original release's 114 backend tests: **reproduced PASS (114/114)** against disposable SQLite before changes. Node tests: **reproduced PASS (35/35)**.
- Updated source: **122/122 backend tests PASS** (114 original + 8 new) and **35/35 Node tests PASS**, 157 in these two suites. Python compileall PASS. Source **syntax parsing PASS for 74 JS/JSX files** (does not prove a Vite build).
- Clean isolated seed: **10 languages, 60 courses, 192 lessons, 606 vocabulary entries, 778 questions**; 928 options. Original production data was neither read nor modified.
- Previously fixed defect controls: two-to-eight option floor/ceiling, exactly one correct option, rejected mutations retain SQLite state, and HTTPS YouTube URL allowlist are covered by passing tests. PostgreSQL serialization is **NOT VERIFIED**.
- Historical reports reviewed for claims and compared against source; previous evidence was retained, not assumed to represent fresh test execution.

## Findings and changes

1. **HIGH / BLOCKER — Missing frontend lockfile and install dependencies.** The uploaded ZIP has no `package-lock.json`. `npm ci --offline` fails with **EUSAGE**; attempted lock generation via `npm install --package-lock-only` failed with **EAI_AGAIN** (cannot resolve `registry.npmjs.org`). `npm run build` and `npm run test:frontend` cannot run without Vite/Vitest. Do **not** interpret JSX parsing as a production build. Lockfile remains absent rather than fabricating one.
2. **MEDIUM / FIXED (SQLite regression verified) — Unbounded admin student listings.** `GET /api/admin/students` now returns at most 100 accounts per request with `limit/offset` preserving the list response type. A new bounded `/api/admin/students/page` exposes server-side search, status filter, sort, page size (max 50), and totals. The existing Student Overview UI now requests pages instead of all accounts at once. Parameter, access-control, search-escaping and pagination tests pass; React interactions cannot be accepted without a frontend build/browser test.
3. **MEDIUM / FIXED (SQLite regression verified) — Missing mandatory JWT claim enforcement.** `current_user` now requires `exp`, `sub`, `csrf`, `iss`, and validates types of essential claims. Five malformed signed-token cases correctly return HTTP 401. This is defense-in-depth, not server-side logout token revocation.
4. **HIGH / OPEN — Logout token revocation.** Logout clears the browser cookie but does not revoke a copied JWT on the server. A persistent token/session table and tested schema migration or an equivalent distributed revocation design are required before public deployment. No untested migration was introduced.
5. **HIGH / OPEN — Distributed login throttling.** Current in-process per-IP+email counters do not protect multiple workers/replicas and may be bypassed by rotating source identity. Needs shared rate limit storage or trusted gateway controls.
6. **MEDIUM / OPEN — Generic admin listings.** `/api/admin/manage/{table}` still materializes entire tables. Student pagination does not solve this separate endpoint. Add server-side pagination with coordinated UI changes before scaling.
7. **HIGH / RELEASE VERIFICATION GAP — No physical browser acceptance.** All 267 controls, all 21 actual app routes, student/admin end-to-end workflows, responsive layouts, and console/network inspections remain NOT RUN.
8. **HIGH / RELEASE VERIFICATION GAP — No disposable PostgreSQL test instance.** Migration head is `0004` by source inspection; PostgreSQL integration and option-concurrency tests NOT RUN. SQLite cannot substantiate PostgreSQL correctness.
9. **MEDIUM / RELEASE VERIFICATION GAP — Ten-language local audio.** No compatible Piper/eSpeak NG voice found here; four bundled English/Spanish recordings are decodable but have not been listened to; human pronunciation QA NOT RUN. The bundled five 35-byte MP3 stubs are invalid and are blocked by the existing media handler.
10. **MEDIUM / OPEN — Dependency and performance security.** Online vulnerability scans, concurrent load tests, query plans, cross-browser visual QA and fixed-version Python 3.11.6 runtime checks are NOT RUN. Version ranges in requirements cannot establish precise production dependency versions.

## Final release scorecard

| Category | Independently verified status |
|---|---|
| ZIP integrity | **PASS** original and nested evidence archive |
| Backend tests | **PASS — 122/122** (Python 3.13.5, isolated SQLite) |
| Node tests | **PASS — 35/35** (Node 22.16.0) |
| Python compile / JS/JSX syntax | **PASS** / **PASS** (74 files; syntax only) |
| Frontend production build | **BLOCKED** — missing npm lockfile/dependencies, registry DNS failure |
| Frontend React tests | **BLOCKED** — Vitest cannot install/run |
| Browser acceptance | **NOT RUN** — 267 controls, 21 routes |
| Student workflows | **PARTIAL** — tested API behavior, no browser E2E |
| Admin workflows | **PARTIAL** — tested API behavior, no browser E2E |
| MCQ validation | **PASS in isolated SQLite**; PostgreSQL concurrency NOT RUN |
| Video URL security | **PASS** parser and backend tests; browser NOT RUN |
| PostgreSQL staging | **NOT RUN** — PostgreSQL server/client unavailable |
| Data integrity | **PARTIAL PASS in SQLite**; real PG not verified |
| Security | **PARTIAL; unresolved HIGH risks** |
| Performance | **PARTIAL** — student pagination improved; load tests NOT RUN |
| Ten-language TTS | **BLOCKED / NOT RUN** — compatible engines missing, no listening |

## Release gate

**Demo:** Not yet approved: complete `npm install` (generate/commit lockfile on trusted network), `npm ci`, `npm run build`, `npm run test:frontend`, and manual/browser journeys with real screens first.  
**Production:** Additional separate PostgreSQL staging tests, distributed session/rate limiting, generic admin pagination, dependency audits, real spoken TTS QA, accessibility, security and load testing required.  
**No destructive DB operation, migrations, or reseeding was performed against any user database.**
