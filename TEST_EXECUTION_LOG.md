# Final executable QA evidence, 29–30 October 2026

- `cd backend && python -m pytest -q tests` → **PASS** `41 passed in 18.90s` (`FINAL_BACKEND_TEST_LOG.txt`).
- `node --test tests/*.test.mjs` → **PASS** 6 tests (`FINAL_NODE_TEST_LOG.txt`).
- Global TypeScript transpile parse of `src/**/*.js,jsx` → **PASS** 59 files, 0 syntax errors (`FRONTEND_PARSE_LOG.txt`). No bundler/runtime validation.
- Fresh isolated SQLite `DATABASE_URL=sqlite:////tmp/lingobridge_final_qa_seed.sqlite python -m alembic upgrade head` → **PASS**, four migrations `0001`→`0004`; seed and repeat-seed quality audit found 0 structural findings.
- `DATABASE_URL=... python -m app.quality_audit` and `python -m app.deep_language_audit` → **PASS**, 0 structural/script findings across 10 languages, 60 courses, 192 lessons, 606 vocabulary and 778 quiz questions.
- `ffmpeg -v error -xerror -i <each_demo>.mp3 -f null -`, `ffprobe` duration, PCM amplitude and SHA-256 → **PASS** 4/4 independent English and Spanish synthetic speech files (exact values in `DEMO_AUDIO_MANIFEST.json`). Five original 35-byte stubs are **invalid** and now HTTP-blocked.
- Python Playwright Chromium native `HTMLAudio` playback progress using each demo as a data URL → **PASS** 4/4; `BROWSER_AUDIO_SMOKE.json`. Chromium direct HTTP navigation to localhost → **FAIL** `ERR_BLOCKED_BY_ADMINISTRATOR`; this is **not React E2E**.
- `npm install --offline --ignore-scripts` → **FAIL** `ENOTCACHED @playwright/test` (`npm registry` DNS also `EAI_AGAIN`); `npm run build` → **FAIL** `vite: not found`; frontend bundle remains **NOT TESTED** at code-level.
- Live PostgreSQL Alembic/restore/seed tests → **NOT TESTED**; no PostgreSQL server/binaries or authorized staging backup.
- Live Azure Speech & full 10-language sound review → **NOT TESTED / MANUAL VALIDATION REQUIRED**. HTTP mock provider integration tests **PASS** within pytest.

Run the PowerShell steps in `POSTGRES_STAGING_QA.md` and `WINDOWS_SETUP.md`, then record the external test evidence instead of converting any unperformed check to PASS.
