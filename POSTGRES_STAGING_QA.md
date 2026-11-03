# PostgreSQL staging migration and preservation check (Windows PowerShell)

**Never run a migration, seed, restore or rollback against the student's existing database during QA.** This workflow reads production **only with `pg_dump`**, then restores to a new, isolated PostgreSQL database. PostgreSQL is **NOT TESTED** in the sandbox release environment; all commands below are for local execution.

Prerequisites: PostgreSQL 15+ and its `bin` directory on your `PATH`, Python venv with `psycopg[binary]` and `requirements.txt` installed, and enough disk space to hold a full encrypted/restricted backup and staging clone. Run these commands in the new project's `backend` folder. Use real credentials via `Read-Host`; **never** put passwords into a checked-in `.env` or ZIP.

## 1. Backup the existing database without changing it

```powershell
cd C:\path\to\LingoBridge\lingobridge\backend
$ProdDb = 'lingobridge' # change only if your actual database has another name
$StageDb = 'lingobridge_qa_20261029' # change suffix to a fresh, never-used name
if ($StageDb -eq $ProdDb -or $StageDb -notmatch '^[a-z][a-z0-9_]*_(qa|staging)(_[a-z0-9]+)?$') { throw 'Unsafe staging DB name' }
$Backups = Join-Path (Get-Location) 'private_qa_backups'
New-Item -ItemType Directory -Force -Path $Backups | Out-Null
$Dump = Join-Path $Backups 'before_upgrade.dump'
$env:PGPASSWORD = Read-Host 'Production DB password (read-only pg_dump)' # hidden echo NOT guaranteed: use a secure pgpass file if preferred
pg_dump -h 127.0.0.1 -p 5432 -U lingobridge -d $ProdDb --format=custom --file=$Dump
if ($LASTEXITCODE -ne 0) { throw 'pg_dump failed. Stop.' }
pg_restore --list $Dump | Select-Object -First 8
if ($LASTEXITCODE -ne 0 -or (Get-Item $Dump).Length -lt 1024) { throw 'Backup invalid. Stop.' }
Remove-Item Env:PGPASSWORD
```

Copy this `.dump` to protected offline storage and test restoring it before ever upgrading the real application.

## 2. Create/restore an isolated test database

```powershell
$env:PGPASSWORD = Read-Host 'PostgreSQL staging administrator password'
# Use a NEW staging name each run. createdb fails if it already exists (safe).
createdb -h 127.0.0.1 -p 5432 -U postgres -O postgres $StageDb
if ($LASTEXITCODE -ne 0) { throw 'Staging DB creation failed; no production operation should follow.' }
pg_restore -h 127.0.0.1 -p 5432 -U postgres -d $StageDb --exit-on-error --no-owner --no-acl $Dump
if ($LASTEXITCODE -ne 0) { throw 'Staging restore failed; stop.' }
$PgPass = $env:PGPASSWORD
$Encoded = [uri]::EscapeDataString($PgPass)
$env:DATABASE_URL = "postgresql+psycopg://postgres:${Encoded}@127.0.0.1:5432/$StageDb"
Remove-Item Env:PGPASSWORD
Remove-Variable PgPass, Encoded
```

Confirm that `DATABASE_URL` ends with **your staging database name**, not the production database. This release's `scripts.staging_postgres_qa` refuses non-PostgreSQL URLs and databases whose names do not end in `_qa` or `_staging` (optionally followed by an underscore suffix).

## 3. Snapshot preservation, migrate, check constraints, and seed twice

```powershell
.\.venv\Scripts\python.exe -m scripts.staging_postgres_qa --output .\qa_before.json
.\.venv\Scripts\python.exe -m alembic -c alembic.ini current
.\.venv\Scripts\python.exe -m alembic -c alembic.ini upgrade head
if ($LASTEXITCODE -ne 0) { throw 'Migration failed on staging. Stop.' }
.\.venv\Scripts\python.exe -m scripts.staging_postgres_qa --output .\qa_after_migrate.json --compare .\qa_before.json --inspect
if ($LASTEXITCODE -ne 0) { throw 'Historical data changed or schema invalid. Stop.' }
.\.venv\Scripts\python.exe -m app.seed
if ($LASTEXITCODE -ne 0) { throw 'First seed failed. Stop.' }
.\.venv\Scripts\python.exe -m scripts.staging_postgres_qa --output .\qa_seed_first.json --include-curriculum --inspect
.\.venv\Scripts\python.exe -m app.seed
if ($LASTEXITCODE -ne 0) { throw 'Second seed failed. Stop.' }
.\.venv\Scripts\python.exe -m scripts.staging_postgres_qa --output .\qa_seed_second.json --include-curriculum --compare .\qa_seed_first.json --inspect
if ($LASTEXITCODE -ne 0) { throw 'Seed was not idempotent. Stop.' }
.\.venv\Scripts\python.exe -m scripts.staging_postgres_qa --output .\qa_after_seed.json --compare .\qa_before.json --inspect
if ($LASTEXITCODE -ne 0) { throw 'Existing student history changed. Stop.' }
.\.venv\Scripts\python.exe -m app.quality_audit > .\qa_curriculum_audit.json
.\.venv\Scripts\python.exe -m app.deep_language_audit > .\qa_deep_language_audit.json
.\.venv\Scripts\python.exe -m alembic -c alembic.ini current
```

The fingerprint tool hashes **all pre-existing rows and selected column values**, not just record counts, in `users` (including password hashes), `student_languages`, `course_enrollments`, `lesson_progress`, `quiz_attempts`, `flashcard_states` (excluding only four newly added nullable schedule columns), `daily_activity`, `bookmarks`, and `user_achievements`. `--include-curriculum` also checks IDs/content/answers to catch unwanted changes from a repeated seed. It inspects PostgreSQL FK/index/unique-constraint counts, unvalidated constraints and Alembic head. The scope is meaningful regression assurance but not a full recovery or concurrency test.

## 4. Rollback and recovery

The `0001`–`0004` migration downgrades are **intentionally blocked**: dropping columns could destroy new flashcard data. **Do not run `alembic downgrade` against an existing student database**. The safe rollback test is to create **another new, isolated staging database** and restore the same `.dump` into it, then compare the pre-upgrade fingerprint. Do not restore into production during testing.

```powershell
$RollbackDb = 'lingobridge_qa_rollback2'
$env:PGPASSWORD = Read-Host 'PostgreSQL staging administrator password'
createdb -h 127.0.0.1 -p 5432 -U postgres -O postgres $RollbackDb
if ($LASTEXITCODE -ne 0) { throw 'Restore-test DB creation failed' }
pg_restore -h 127.0.0.1 -p 5432 -U postgres -d $RollbackDb --exit-on-error --no-owner --no-acl $Dump
if ($LASTEXITCODE -ne 0) { throw 'Restore rehearsal failed' }
$Encoded = [uri]::EscapeDataString($env:PGPASSWORD)
$env:DATABASE_URL = "postgresql+psycopg://postgres:${Encoded}@127.0.0.1:5432/$RollbackDb"
Remove-Item Env:PGPASSWORD
Remove-Variable Encoded
.\.venv\Scripts\python.exe -m scripts.staging_postgres_qa --output .\qa_rollback_restore.json --compare .\qa_before.json
if ($LASTEXITCODE -ne 0) { throw 'Rollback restore data differs from backup' }
```

If stage was restored from revision `0003`, then run `upgrade head` there for the genuine `0003→0004` PostgreSQL check. If the supplied backup was **already** revision `0004`, upgrading it does not establish an actual PostgreSQL `0003→0004` test; obtain an authorized **older staging backup** or construct a wholly synthetic `0003` test DB. Never downgrade production to fake a prior revision.

**Data security:** these snapshot JSON files contain only counts/hash digests and schema metadata, not raw emails or password hashes. The database dump itself contains private student records and must never be shared publicly or included in the project ZIP.
