# Admin API — MCQ and lesson video validation

All endpoints require a valid **admin session cookie** and a valid `X-CSRF-Token` on writes. Use your locally generated test accounts in a disposable database for QA, never real student credentials.

## MCQs

- `POST /api/admin/lessons/{lesson_id}/questions` creates a complete MCQ with `options` array of **2–8** choices and **exactly one** `is_correct: true`. Invalid input returns **400**. The entire transaction creates question/options together.
- `PUT /api/admin/questions/{question_id}` updates the complete question and validates the full 2–8 range and exactly one correct choice; fails with **400** if invalid, **409** if learner history prevents modification.
- `POST /api/admin/manage/options` adds an option to an existing MCQ. A ninth option returns **409** and a second correct choice returns **409**. Existing attempted questions cannot be changed. Legacy malformed 1-choice questions may be repaired by adding a non-correct second choice if not attempted.
- `PATCH /api/admin/manage/options/{option_id}` may change an incorrect option's text; moving an option to another MCQ, empty text, or changing the answer key to an invalid state is rejected.
- `DELETE /api/admin/manage/options/{option_id}` rejects deletion of a correct choice and rejects deletion if it would leave fewer than two choices (**409**). Any existing learner history also prevents destructive deletion.
- Concurrent option writes to a single question are serialized through a PostgreSQL parent-question row lock; the actual PostgreSQL concurrency scenario has not yet been executed.

## Lesson video URLs

- `POST /api/admin/manage/lessons` and `PATCH /api/admin/manage/lessons/{lesson_id}` validate `video_url` through the same Pydantic-backed service.
- Accepted: **HTTPS** YouTube watch, short (`youtu.be`), embed, `/shorts/`, `/live/`, `/v/`, and YouTube-nocookie embed using one **11-character** identifier. Hostname must match the explicit allowlist exactly.
- Rejected **422**: `javascript:`, `data:`, HTTP, `ftp:`, userinfo, custom ports, unrelated providers, deceptive hosts/subdomains, malformed IDs, duplicate `v` values, control characters and `null`.
- `"video_url": ""` is a valid explicit request to remove a video link from a lesson. Omission leaves the field unchanged during PATCH.
- Validation never fetches user-submitted URLs. Existing records are left untouched; the preview derives outbound links only from a validated YouTube ID.
- The supported player is YouTube; no legitimate alternate video-host implementation was found in the application.

## Example

```json
{"video_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"}
```

This document describes the release source, not a running production instance.
