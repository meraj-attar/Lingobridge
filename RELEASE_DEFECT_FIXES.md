# LingoBridge — QA defect fixes and root-cause analysis

Date: 30 October 2026. Source: enhanced LingoBridge archive (164 original files). Evidence: supplied expanded QA report, separate **independent** pre-fix reproduction, and post-fix validation. All changes were made in a working copy, never the user's PostgreSQL instance.

## BUG-01: deleting a distractor can leave a one-option MCQ (HIGH data integrity)

- **Root cause:** generic `DELETE /api/admin/manage/options/{id}` in `backend/app/main.py` blocked deleting the correct option but never checked the remaining option count.
- **Pre-fix:** HTTP **200**, count **2 → 1**.
- **Fix:** lock the parent MCQ row using `SELECT ... FOR UPDATE` where supported; reject any option deletion unless the question currently has more than two choices, exactly one correct answer, and the target is incorrect. Error: **409**. Check before any modification; rejected requests do not commit partial changes.
- **Post-fix:** HTTP **409**, count **2 → 2**; DB unchanged. Deleting a distractor from three options still works. A legacy one-option question cannot be deleted further; adding a second choice can repair it.

## BUG-02: ninth option accepted (MEDIUM integrity)

- **Root cause:** generic `POST /api/admin/manage/options` checked the correct-answer flag but not the maximum count, unlike the complete-question editor.
- **Pre-fix:** HTTP **201**, count **8 → 9**.
- **Fix:** central MCQ parent locking and count validation **max 8** in generic option creation; reject additional correct answers; reject blank option text; reject option changes to questions used by learners. Existing MCQ `PUT` bulk editor already enforces **2–8** and **exactly one** correct answer, covered by additional regression tests. Correct-answer options cannot be removed individually.
- **Post-fix:** HTTP **409**, count **8 → 8**; DB unchanged. Adding an eighth option to a seven-option question succeeds.
- **Concurrency:** `SELECT ... FOR UPDATE` serializes mutation through the parent question on **PostgreSQL**. SQLite has no equivalent row-lock semantics. PostgreSQL concurrent-request behavior was not run in this environment and remains a staging acceptance item. No schema change is made.

## BUG-03: unsafe video URL persisted (MEDIUM input validation)

- **Root cause:** `POST/PATCH /api/admin/manage/lessons` accepted any text for `video_url` in the generic editor; the UI's YouTube matcher was also unanchored. Previously the fallback video preview rendered the raw stored URL as a clickable external link.
- **Pre-fix:** PATCH with `javascript:alert(1)` returned **200** and stored it.
- **Fix:** new `backend/app/video_urls.py` contains one strict URL parser plus a Pydantic field-validator schema `VideoURLInput`; both lesson create and update call the same validation. Accept only exact HTTPS YouTube hosts and valid video identifiers; reject credentials, nonstandard ports, deceptive hosts, unsafe schemes, malformed IDs and duplicate video ID parameters. React `src/utils/youtube.js` uses equivalent strict extraction; admin video/lesson forms perform pre-submit checks and preserve server error messages. `VideoPlayer.jsx` only exposes sanitized YouTube links.
- **Post-fix:** unsafe PATCH returns **422**, stored URL unchanged.
- **Supported formats:** `https://www.youtube.com/watch?v=<11-character-ID>`, `https://youtu.be/<ID>`, `https://www.youtube.com/embed/<ID>`, YouTube `/shorts/`, `/live/`, `/v/`, mobile YouTube and YouTube-nocookie embed. All domains must match an explicit allowlist; non-YouTube providers were not used by this application's video player, so none was added.
- **Clearing links:** `""` intentionally means *remove this lesson's video link* and is accepted; **null is rejected**. Pre-existing records are not rewritten, deleted, or migrated; invalid legacy URLs are never rendered as clickable external links.

## Admin quiz editor update

- `src/pages/admin/ManageQuizzesPage.jsx` now exposes **Add option** and **Remove last incorrect option**, with two-option floor / eight-option ceiling. A correct answer cannot be removed until a different answer is selected as correct. Save is disabled while the request runs, validation errors remain visible, and the complete-question API remains the authoritative validation layer.
- Existing student quiz grading, four question types, progress, and previous learner attempts are preserved.

## Files changed

1. `backend/app/main.py`
2. `src/utils/youtube.js`
3. `src/components/lessons/VideoPlayer.jsx`
4. `src/pages/admin/ManageVideosPage.jsx`
5. `src/pages/admin/ManageLessonsPage.jsx`
6. `src/pages/admin/ManageQuizzesPage.jsx`

## New code / tests

- `backend/app/video_urls.py`
- `backend/tests/test_release_defect_fixes.py` (67 parametrized tests)
- `tests/video-url.test.mjs` (27 new Node subtests)

No previously existing application file or test was removed, and no existing test was modified or skipped. There are no Alembic migrations or schema changes; revision **0004** stays the head. No production data is accessed.
