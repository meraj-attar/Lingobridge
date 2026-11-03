# LingoBridge — Multilingual Language-Learning Application

LingoBridge is an MCA project built with **React, Vite and Tailwind CSS** on the frontend and **FastAPI, SQLAlchemy, PostgreSQL and Alembic** on the backend. It supports **English, Hindi, Marathi, Gujarati, Bengali, Tamil, Telugu, Kannada, Urdu and Spanish**, with courses, lessons, vocabulary, quizzes, MCQs, flashcards, spaced repetition, enrollments, progress, XP, streaks and student/admin accounts.

## Voice/TTS removal (31 October 2026)

This build **does not contain text-to-speech, recorded pronunciation playback, audio uploads or audio management**. No Piper, eSpeak NG, Azure Speech or browser SpeechSynthesis integration remains. Written phonetic pronunciation hints on vocabulary cards may still appear: these are **text content**, not spoken audio.

The application retains legacy database columns (`Language.tts_locale`, `Lesson.audio_url`, `Vocabulary.audio_url`, and the written `Vocabulary.pronunciation` field) to avoid destructive changes to existing student records. Old audio URLs may remain stored in an existing database, but this release no longer exposes audio routes or controls and does not modify those records. Alembic revisions **0001–0004** remain untouched. No migration or seed is needed to upgrade a database already at 0004.

**Important:** Historical release reports under `QA_FINAL/` and other retained reports refer to the previous version. They are retained for traceability, not proof of this voice-free build's browser or production readiness. See `CLEANUP_MANIFEST.md`, `IMPLEMENTATION_CLEANUP_REPORT.md`, and `CLEANUP_TEST_REPORT.md` for current information.

## Windows setup

See [WINDOWS_SETUP.md](WINDOWS_SETUP.md) for steps and database-safety precautions. Python **3.11.x**, Node.js **20+**, npm and a user-managed PostgreSQL server are needed.

In PowerShell, from the extracted `lingobridge` directory:

```powershell
cd backend
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
# On a NEW installation only, configure .env based on .env.example.
python -m uvicorn app.main:app --host 127.0.0.1 --port 8003 --reload
```

Open another PowerShell terminal in the project root:

```powershell
npm install
npm run dev -- --host 127.0.0.1 --port 5175
```

The source ZIP originally **did not include a `package-lock.json`**. On a connected Windows installation, `npm install` will create one; commit and retain it for reproducible future `npm ci` runs. Do not delete a valid lockfile from an existing working installation.

## Focused checks

Run backend tests **only with the provided disposable-test fixtures**, not with a production database:

```powershell
cd backend
python -m compileall -q app scripts tests
python -m pytest -q tests
cd ..
npm test
npm run build
npm run test:frontend
```

The test suite creates a disposable SQLite test file; it does **not** require or access the production PostgreSQL database. Backend application startup, production build and full browser journeys are distinct verification tasks; consult the current cleanup test report for what actually ran.

**Never** run a seed command, migration or database-reset script on your populated PostgreSQL database. Back up your current installation before deployment. Video-management functionality is retained for compatibility; the legacy student YouTube section is intentionally not re-enabled.
