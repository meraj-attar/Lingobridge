# LingoBridge — Windows installation and safe upgrade

## Prerequisites

- Python 3.11.x, Node.js 20+, npm, PowerShell and PostgreSQL (existing installation supported).
- Your **existing `backend/.env` credentials**, which should never be included in the shared ZIP.
- A backup of the application files and your populated PostgreSQL database before any deployment.

**No TTS engines or voice models are required.** This version intentionally has no voice/audio functionality.

## Safely upgrade an existing LingoBridge installation

1. Stop the current frontend and backend, then back up the existing project and database. Example:

   ```powershell
   pg_dump -h localhost -U YOUR_POSTGRES_USER -d YOUR_DATABASE -Fc -f .\lingobridge_backup_before_upgrade.dump
   ```

2. **Preserve your existing `backend/.env`, PostgreSQL data directory and any personally retained media recordings outside the project archive.** Do not replace secret files with placeholders or delete real user assets during the upgrade.
3. Replace **source files** with the contents of this ZIP, after taking a copy of the previous installation. When upgrading by copying over an old directory, follow the **source-file deletion list** in `CLEANUP_MANIFEST.md` so obsolete TTS modules and controls are not left behind; do not blindly delete `backend/.env`, database files, uploads or personal recordings.
4. The bundled Alembic revision remains **0004**. There are **no new migrations** for voice removal and no migration command should be necessary for an existing installation already at revision 0004.
5. **Do not run `python -m app.seed`, truncate tables, or reset any student data.** The legacy voice/audio database columns remain in place for safety.

## Backend installation (PowerShell)

```powershell
cd C:\path\to\lingobridge\backend
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
# For a NEW installation, create backend/.env based on backend/.env.example.
# For an EXISTING installation, keep your present backend/.env.
python -m uvicorn app.main:app --host 127.0.0.1 --port 8003 --reload
```

## Frontend installation (second PowerShell terminal)

```powershell
cd C:\path\to\lingobridge
npm install
npm run build
npm run dev -- --host 127.0.0.1 --port 5175
```

The supplied original ZIP has no `package-lock.json`; create the lockfile via a successful `npm install` with registry access and retain it. Later clean installs should use `npm ci` once this lockfile is committed.

## Focused safety and regression checks

```powershell
cd C:\path\to\lingobridge\backend
python -m compileall -q app scripts tests
python -m pytest -q tests
cd ..
npm test
npm run test:frontend
npm run build
```

These backend pytest fixtures use an isolated SQLite database. Inspect and use only the supplied test suite, not any migration/seed script. For running against your actual populated installation, use temporary accounts and **read-only checks** as appropriate. Verify login, lessons, vocabulary, quizzes, flashcards and admin UI, and verify no voice/audio buttons remain.

For known limitations and exact checks performed, see `CLEANUP_TEST_REPORT.md` and `CLEANUP_MANIFEST.md`. Do not interpret historical `QA_FINAL/` results as current Windows or browser verification.
