# PostgreSQL Staging / Migration / Concurrency Verification

**Result: NOT RUN — PostgreSQL is unavailable in this execution environment.** Neither PostgreSQL 17.10 server/client nor a disposable PostgreSQL instance was available. The included Python integration suite uses SQLite only, and **cannot** prove PostgreSQL concurrency, row-level locking, FK handling, query plans or migration compatibility. The user's populated PostgreSQL instance was NEVER contacted.

## Preserved database boundaries

- `backend/alembic/versions/0001_initial.py` through `0004_flashcard_review_schedule.py` remain unchanged; source head `0004`.
- No new migrations; no modifications to existing schema or populated database.
- Temporary SQLite seed independently reproduced 10 languages, 60 courses, 192 lessons, 606 vocabulary items and 778 quiz questions. This is not a PostgreSQL staging run.
- Regression tests establish rejected deletion/creation and persistent student progress only under SQLite.

## Required staging plan (DO NOT run against the real database)

1. On a non-production workstation, create a **separate, empty, disposable** PostgreSQL database with a dedicated least-privilege user, using a **distinct** connection string from your production database; verify `SELECT current_database(), current_user` first.
2. Keep a production backup isolated and avoid copying sensitive production student data into demo/test. Connect a separate cloned source checkout, not your live app.
3. Verify Alembic's current and heads under the staging-only environment. Apply migrations `0001`→`0004` to **empty staging only** and verify constraints, indexes, referential actions and rollback.
4. Seed **only** the explicitly confirmed empty staging DB, using disposable account records.
5. Test concurrent insert of the eighth and ninth option, simultaneous deletion from 3→2 choices, multiple correct flags, atomic rollback and independent requests across multiple workers. Assert final count in [2,8] and exactly one correct answer.
6. Test duplicated course enrollment, multiple progress/flashcard updates, replayed quiz submissions, FK RESTRICT/CASCADE, attempted deletion of a lesson with progress, attempts, enrollments, bookmarks, schedules and activity rows; verify history retained.
7. Test student/admin access controls against a real PG server, transaction isolation and pool exhaustion. Capture exact PostgreSQL version, migrations, SQLSTATE, test logs, and `EXPLAIN (ANALYZE, BUFFERS)` for admin listing and course queries.
8. **Never** point pytest, Alembic or seed scripts at the user's existing PostgreSQL URL. Use staging credentials only; require written validation of the staging target before any destructive operations.

### PostgreSQL scorecard

| Case | Status |
|---|---|
| Connection to user PostgreSQL | NOT ATTEMPTED (required safety) |
| Disposable PostgreSQL database | NOT AVAILABLE |
| Alembic `0001`→`0004` live PG run | NOT RUN |
| Foreign-key and cascading delete integrity | NOT RUN on PG; partial SQLite tests PASS |
| Concurrency / MCQ parent row lock | NOT RUN |
| Progress and flashcard persistence | NOT RUN on PG; SQLite tests PASS |
| Session isolation and quiz replay race | NOT RUN on PG |
| PG EXPLAIN / query performance | NOT RUN |
