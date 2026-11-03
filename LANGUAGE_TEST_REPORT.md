# Ten-language test report (source ZIP repair, 29 October 2026)

Every count below was measured in a **temporary SQLite installation** created from the revised source and migrations, not from your live PostgreSQL database. A second seed produced identical records.

| Language | Locale | Courses | Modules | Lessons | Vocabulary | Questions | Script/structure | Live pronunciation |
|---|---|---:|---:|---:|---:|---:|---|---|
| English (`en`) | `en-US` | 6 | 6 | 22 | 86 | 93 | Pass: codepoint/seed/API checks | **Not tested on device** |
| Hindi (`hi`) | `hi-IN` | 6 | 6 | 22 | 86 | 93 | Pass: codepoint/seed/API checks | **Not tested on device** |
| Marathi (`mr`) | `mr-IN` | 6 | 6 | 22 | 56 | 88 | Pass: codepoint/seed/API checks | **Not tested on device** |
| Gujarati (`gu`) | `gu-IN` | 6 | 6 | 18 | 54 | 72 | Pass: codepoint/seed/API checks | **Not tested on device** |
| Bengali (`bn`) | `bn-IN` | 6 | 6 | 18 | 54 | 72 | Pass: codepoint/seed/API checks | **Not tested on device** |
| Tamil (`ta`) | `ta-IN` | 6 | 6 | 18 | 54 | 72 | Pass: codepoint/seed/API checks | **Not tested on device** |
| Telugu (`te`) | `te-IN` | 6 | 6 | 18 | 54 | 72 | Pass: codepoint/seed/API checks | **Not tested on device** |
| Kannada (`kn`) | `kn-IN` | 6 | 6 | 18 | 54 | 72 | Pass: codepoint/seed/API checks | **Not tested on device** |
| Urdu (`ur`) | `ur-PK` | 6 | 6 | 18 | 54 | 72 | Pass: codepoint/seed/API checks | **Not tested on device** |
| Spanish (`es`) | `es-ES` | 6 | 6 | 18 | 54 | 72 | Pass: codepoint/seed/API checks | **Not tested on device** |

## Level-by-level coverage (measured record counts)

Each entry is `lessons / vocabulary / questions` for that language and level. All 60 course and 60 module paths were present.

| Language | A1 | A2 | B1 | B2 | C1 | C2 |
|---|---|---|---|---|---|---|
| English | 7/46/33 | 3/8/12 | 3/8/12 | 3/8/12 | 3/8/12 | 3/8/12 |
| Hindi | 7/46/33 | 3/8/12 | 3/8/12 | 3/8/12 | 3/8/12 | 3/8/12 |
| Marathi | 7/16/28 | 3/8/12 | 3/8/12 | 3/8/12 | 3/8/12 | 3/8/12 |
| Gujarati | 3/9/12 | 3/9/12 | 3/9/12 | 3/9/12 | 3/9/12 | 3/9/12 |
| Bengali | 3/9/12 | 3/9/12 | 3/9/12 | 3/9/12 | 3/9/12 | 3/9/12 |
| Tamil | 3/9/12 | 3/9/12 | 3/9/12 | 3/9/12 | 3/9/12 | 3/9/12 |
| Telugu | 3/9/12 | 3/9/12 | 3/9/12 | 3/9/12 | 3/9/12 | 3/9/12 |
| Kannada | 3/9/12 | 3/9/12 | 3/9/12 | 3/9/12 | 3/9/12 | 3/9/12 |
| Urdu | 3/9/12 | 3/9/12 | 3/9/12 | 3/9/12 | 3/9/12 | 3/9/12 |
| Spanish | 3/9/12 | 3/9/12 | 3/9/12 | 3/9/12 | 3/9/12 | 3/9/12 |

## What was individually tested

- **All 10 codes:** language row and `tts_locale`, six courses, matching modules/levels, published lesson content, vocabulary/question availability, registration/enrollment/A1 lesson retrieval through FastAPI, quiz answer secrecy, and no missing vocabulary/question-bearing lessons.
- **Hindi, Marathi, Gujarati, Bengali, Tamil, Telugu, Kannada, Urdu:** script ranges checked in target examples; Urdu RTL was checked at source level. **Spanish and English:** alphabetic target sentences, course presence and routing checked. Script tests do not validate grammar or typography on Windows.
- **Seven additional languages:** all 18 balanced lessons per language contain three vocabulary cards and all four question formats; MCQs have four distinct target-language options, with one correct answer. New words were checked mechanically against the original phrase.
- **All 10 voice codes:** mocked online-TTS endpoint accepted a request and returned audio/mpeg for the mapped voice; provider-disabled and invalid requests returned errors. The fake audio is not real speech.
- **Existing English/Hindi/Marathi lessons:** retained the original larger curricula and course IDs; extension wording/vocabulary fixes were guarded. Their 22 lessons per language have different question counts due to the original authored content.

## Audio verification per language

For **English, Hindi, Marathi, Gujarati, Bengali, Tamil, Telugu, Kannada, Urdu, Spanish**, live word pronunciation and live sentence pronunciation were **not tested** on a real device. The seed has **zero attached recorded lesson or vocabulary audio URLs** for all ten languages. Runtime pronunciation depends on recorded instructor files, an installed matching-language browser voice, or explicitly enabled online TTS. All require listening-based validation on the target system.

## Release limitations

Native speakers have **not** audited the complete 192-lesson curriculum. English reference meanings, some grammar explanations and legacy learner-interface labels remain intentionally in English, and must be reviewed for the intended audience. C1 and C2 are short sample lessons, not full proficiency certification. PostgreSQL, Windows, Vite build and browser/UI end-to-end tests remain **not executed**. See `QA_REPORT.md` for a complete status and `WINDOWS_SETUP.md` for an acceptance checklist.
