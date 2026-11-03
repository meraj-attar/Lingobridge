# LingoBridge — Cleanup Manifest

**Input archive:** `LingoBridge_Final_Release_Candidate_QA.zip` — 209 original files.
**Inventory:** 53 files deleted, 33 original files modified, 17 new files, 123 original files unchanged.

**No student database was accessed or changed. No migration was applied.**

## Deleted files — exact inventory and reasons

### Obsolete TTS documents and inventory
- `AUDIO_CONFIGURATION.md` — Audio-specific configuration, report, or generated artifact no longer applicable.
- `AUDIO_GENERATION_PLAN.json` — Audio-specific configuration, report, or generated artifact no longer applicable.
- `AUDIO_RECORDINGS.md` — Audio-specific configuration, report, or generated artifact no longer applicable.
- `AUDIO_SETUP_GUIDE.md` — Audio-specific configuration, report, or generated artifact no longer applicable.
- `BROWSER_AUDIO_SMOKE.json` — Audio-specific configuration, report, or generated artifact no longer applicable.
- `CONTENT_AND_AUDIO_AUDIT.json` — Audio-specific configuration, report, or generated artifact no longer applicable.
- `DEMO_AUDIO_MANIFEST.json` — Audio-specific configuration, report, or generated artifact no longer applicable.
- `FREE_TTS_MODELS_GUIDE.md` — Audio-specific configuration, report, or generated artifact no longer applicable.
- `QA_FINAL/TTS_VERIFICATION_REPORT.md` — Audio-specific configuration, report, or generated artifact no longer applicable.

### Redundant historical logs and diagnostics
- `BACKEND_COMPILE_LOG.txt` — Obsolete previous-run logs superseded by CLEANUP_EVIDENCE; historical written reports retained.
- `BROWSER_SMOKE_LOG.txt` — Obsolete previous-run logs superseded by CLEANUP_EVIDENCE; historical written reports retained.
- `FINAL_BACKEND_TEST_LOG.txt` — Obsolete previous-run logs superseded by CLEANUP_EVIDENCE; historical written reports retained.
- `FINAL_NODE_TEST_LOG.txt` — Obsolete previous-run logs superseded by CLEANUP_EVIDENCE; historical written reports retained.
- `FRONTEND_PARSE_LOG.txt` — Obsolete previous-run logs superseded by CLEANUP_EVIDENCE; historical written reports retained.
- `NEW_QA_EVIDENCE/TTS_STATUS.json` — Obsolete previous-run logs superseded by CLEANUP_EVIDENCE; historical written reports retained.
- `NEW_QA_EVIDENCE/build.log` — Obsolete previous-run logs superseded by CLEANUP_EVIDENCE; historical written reports retained.
- `NEW_QA_EVIDENCE/compileall.log` — Obsolete previous-run logs superseded by CLEANUP_EVIDENCE; historical written reports retained.
- `NEW_QA_EVIDENCE/npm_ci.log` — Obsolete previous-run logs superseded by CLEANUP_EVIDENCE; historical written reports retained.
- `NEW_QA_EVIDENCE/npm_lock_generation.log` — Obsolete previous-run logs superseded by CLEANUP_EVIDENCE; historical written reports retained.
- `NEW_QA_EVIDENCE/npm_test.log` — Obsolete previous-run logs superseded by CLEANUP_EVIDENCE; historical written reports retained.
- `NEW_QA_EVIDENCE/npm_test_final.log` — Obsolete previous-run logs superseded by CLEANUP_EVIDENCE; historical written reports retained.
- `NEW_QA_EVIDENCE/pytest.log` — Obsolete previous-run logs superseded by CLEANUP_EVIDENCE; historical written reports retained.
- `NEW_QA_EVIDENCE/pytest_after_patch.log` — Obsolete previous-run logs superseded by CLEANUP_EVIDENCE; historical written reports retained.
- `NEW_QA_EVIDENCE/pytest_final.log` — Obsolete previous-run logs superseded by CLEANUP_EVIDENCE; historical written reports retained.
- `NEW_QA_EVIDENCE/pytest_updated.log` — Obsolete previous-run logs superseded by CLEANUP_EVIDENCE; historical written reports retained.
- `NEW_QA_EVIDENCE/vitest.log` — Obsolete previous-run logs superseded by CLEANUP_EVIDENCE; historical written reports retained.
- `NPM_INSTALL_ATTEMPT.log` — Obsolete previous-run logs superseded by CLEANUP_EVIDENCE; historical written reports retained.
- `RELEASE_EVIDENCE/NPM_INSTALL_ATTEMPT.log` — Obsolete previous-run logs superseded by CLEANUP_EVIDENCE; historical written reports retained.
- `RELEASE_EVIDENCE/NPM_OFFLINE_ATTEMPT.log` — Obsolete previous-run logs superseded by CLEANUP_EVIDENCE; historical written reports retained.
- `RELEASE_EVIDENCE/VITE_BUILD_ATTEMPT.log` — Obsolete previous-run logs superseded by CLEANUP_EVIDENCE; historical written reports retained.
- `VITE_BUILD_ATTEMPT.log` — Obsolete previous-run logs superseded by CLEANUP_EVIDENCE; historical written reports retained.

### Redundant older QA checklist
- `BROWSER_ACCEPTANCE_CHECKLIST.csv` — Older checklist; more detailed QA_FINAL copy retained as historical evidence.

### Backend TTS and audio-upload functionality
- `backend/app/audio_validation.py` — Old TTS/validation/upload module, no longer imported by runtime.
- `backend/app/azure_speech.py` — Old TTS/validation/upload module, no longer imported by runtime.
- `backend/app/local_tts.py` — Old TTS/validation/upload module, no longer imported by runtime.
- `backend/app/pronunciation.py` — Old TTS/validation/upload module, no longer imported by runtime.
- `backend/scripts/browser_audio_smoke.py` — Old TTS/validation/upload module, no longer imported by runtime.
- `backend/scripts/generate_azure_audio.py` — Old TTS/validation/upload module, no longer imported by runtime.
- `backend/scripts/generate_local_audio.py` — Old TTS/validation/upload module, no longer imported by runtime.

### Bundled audio samples and placeholders
- `backend/media/114a97af-fe35-41f5-89e8-52b1673b67cc.mp3` — Demo/placeholder audio bundled in source, no remaining playback endpoint; existing user uploads/database untouched.
- `backend/media/55aa31a3-f238-4238-9778-60a1f0a84b3a.mp3` — Demo/placeholder audio bundled in source, no remaining playback endpoint; existing user uploads/database untouched.
- `backend/media/5b553ace-ca1e-4620-a78b-da6bfa45ec42.mp3` — Demo/placeholder audio bundled in source, no remaining playback endpoint; existing user uploads/database untouched.
- `backend/media/6d2554ca-1a3a-49c3-b856-6ff381bdc178.mp3` — Demo/placeholder audio bundled in source, no remaining playback endpoint; existing user uploads/database untouched.
- `backend/media/f3007986-ed41-42af-a7bf-9a8912779fde.mp3` — Demo/placeholder audio bundled in source, no remaining playback endpoint; existing user uploads/database untouched.
- `backend/media/lb-demo-en-sentence-eb44e0905d13afe434fc.mp3` — Demo/placeholder audio bundled in source, no remaining playback endpoint; existing user uploads/database untouched.
- `backend/media/lb-demo-en-word-7cce0afe48bc4d268412.mp3` — Demo/placeholder audio bundled in source, no remaining playback endpoint; existing user uploads/database untouched.
- `backend/media/lb-demo-es-sentence-1b71f81c0fe619f734f5.mp3` — Demo/placeholder audio bundled in source, no remaining playback endpoint; existing user uploads/database untouched.
- `backend/media/lb-demo-es-word-474fb8f6b7efcb31e811.mp3` — Demo/placeholder audio bundled in source, no remaining playback endpoint; existing user uploads/database untouched.

### Obsolete voice-specific tests
- `backend/tests/test_local_audio_and_integrity.py` — Dedicated speech tests obsolete; non-speech regression cases preserved elsewhere.
- `tests/speech-voices.test.mjs` — Dedicated speech tests obsolete; non-speech regression cases preserved elsewhere.

### Frontend voice playback and audio-management modules
- `src/hooks/useSpeech.js` — Unused audio UI, selector, or hook after controls and routes removed.
- `src/pages/admin/AudioManagementPage.jsx` — Unused audio UI, selector, or hook after controls and routes removed.
- `src/utils/speechVoices.js` — Unused audio UI, selector, or hook after controls and routes removed.

## Modified original files

- `ADMIN_MODULE_GUIDE.md`
- `QA_FINAL/README_FIRST.md`
- `QA_FINAL/WINDOWS_SETUP_AND_ACCEPTANCE.md`
- `README.md`
- `WINDOWS_SETUP.md`
- `backend/.env.example`
- `backend/app/audit_curriculum.py`
- `backend/app/content_quality.py`
- `backend/app/deep_language_audit.py`
- `backend/app/main.py`
- `backend/app/quality_audit.py`
- `backend/app/seed.py`
- `backend/requirements.txt`
- `backend/tests/test_course_learning.py`
- `backend/tests/test_extended.py`
- `backend/tests/test_final_release.py`
- `backend/tests/test_language_quality.py`
- `backend/tests/test_learning_improvements.py`
- `run_all_checks.ps1`
- `src/App.jsx`
- `src/components/common/Footer.jsx`
- `src/components/layout/AdminLayout.jsx`
- `src/components/lessons/VocabularyCard.jsx`
- `src/components/lessons/VocabularyList.jsx`
- `src/components/quiz/QuizQuestion.jsx`
- `src/pages/admin/ManageVocabularyPage.jsx`
- `src/pages/public/LandingPage.jsx`
- `src/pages/student/FlashcardsPage.jsx`
- `src/pages/student/LanguageSelectPage.jsx`
- `src/pages/student/LessonDetailPage.jsx`
- `src/pages/student/QuizPage.jsx`
- `src/services/api.js`
- `tests/source-contract.test.mjs`

## Added files

- `CLEANUP_EVIDENCE/backend_pytest.log`
- `CLEANUP_EVIDENCE/backend_startup.log`
- `CLEANUP_EVIDENCE/frontend_vitest.log`
- `CLEANUP_EVIDENCE/import_reference_check.json`
- `CLEANUP_EVIDENCE/jsx_parse.log`
- `CLEANUP_EVIDENCE/node_tests.log`
- `CLEANUP_EVIDENCE/npm_ci.log`
- `CLEANUP_EVIDENCE/npm_install_offline.log`
- `CLEANUP_EVIDENCE/npm_install_online.log`
- `CLEANUP_EVIDENCE/vite_build.log`
- `CLEANUP_MANIFEST.json`
- `CLEANUP_MANIFEST.md`
- `CLEANUP_TEST_REPORT.md`
- `IMPLEMENTATION_CLEANUP_REPORT.md`
- `backend/tests/test_password_and_integrity.py`
- `backend/tests/test_voice_removal.py`
- `tests/voice-removal.test.mjs`

## Intentionally preserved files and why

- **`backend/alembic/versions/0001_initial.py` through `0004_flashcard_review_schedule.py`**, including `0003_language_voice_locale.py`: deployed migration history must not be rewritten.
- **`backend/app/models.py`**, including `Language.tts_locale`, `Lesson.audio_url`, `Vocabulary.audio_url`, and the written phonetic `Vocabulary.pronunciation` field: legacy columns remain for safe DB/API compatibility; no voice engine or playback uses them.
- **`backend/scripts/staging_postgres_qa.py`**: checks the existing schema against historical migration 0003, not speech runtime.
- **`backend/data/legacy_seed.json`**, curriculum modules, login/security/progress/MCQ code: preserve the 10-language learning experience, students and learning-history schema.
- **`package.json` and current frontend setup files:** no TTS-only npm packages identified; avoid unrelated dependency changes.
- **`package-lock.json`:** absent in original ZIP; it was not deleted and cannot be regenerated without npm registry access.
- **`QA_FINAL/` historical QA reports and checklist**, plus `RELEASE_EVIDENCE/PRIOR_DEEP_QA_EVIDENCE_PACK.zip`: retained for provenance, not a claim that removed TTS still works.
- **User-specific PostgreSQL, `.env` secrets and personal recordings:** never supplied, never connected to or modified.

## Test artifacts

Current focused results are in `CLEANUP_TEST_REPORT.md`; logs are in `CLEANUP_EVIDENCE/`. The old archive is preserved at its original uploaded path.
