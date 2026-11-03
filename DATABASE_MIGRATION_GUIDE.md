# Database preservation and migration SQL review

**Existing revision:** `0004` (head). **Revisions in this ZIP:** 0001, 0002, 0003, 0004. **New migrations:** none. **Schema changes:** none. **DDL executed against the user's database:** none.

All implementation changes use existing tables and columns. For students/course enrollments, review histories, grades, passwords, and quizzes the exact same rows are retained. When `/api/admin/manage/languages/{id}` is called and dependent content/enrollment exists, the route updates `languages.is_active=false` rather than deleting. Lesson deletion with any progress, quiz, bookmark, quiz session or linked flashcard review is rejected with HTTP `409`.

No SQL migration is needed for this release. The installed original foreign keys still contain CASCADE relationships; API guards protect normal administrator actions but cannot protect against direct manual SQL deletes or scripts. Database-level RESTRICT constraints would require a separate reviewed migration and cleanup plan; do not change constraints without inspecting the actual PostgreSQL catalog and staging test.

## Precautions (on your PC only)

1. Back up and verify restore procedure in staging: `pg_dump -h localhost -U YOUR_USER -d YOUR_DB -Fc -f .\\pre_upgrade.dump`.
2. Check connection string points to the correct DB; never send a real password to anyone.
3. From `backend/`: `python -m alembic -c alembic.ini current`. Expected `0004`.
4. **Do not** run `upgrade`, `downgrade`, seed scripts, truncation or restore on your populated live DB for this release.
5. Test separately on a restored **disposable** PostgreSQL clone with anonymized data and confirm no rows disappear after admin UI actions.

**Staging test status:** new code's SQLite fixtures and HTTP regressions PASS; real PostgreSQL staging migration check NOT RUN (no target PostgreSQL or credentials supplied); no SQL migration produced.
