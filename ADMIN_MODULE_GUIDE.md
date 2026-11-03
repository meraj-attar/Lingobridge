# Admin module update

The original admin access control continues through server-side JWT role checks. The dashboards and core CRUD pages remain. **Audio Management (`/admin/audio`) has been retired** with the voice feature. Existing video administration remains accessible at `/admin/videos` for backward compatibility; YouTube tutorials remain hidden from student lesson pages.

## Dashboard

- Real statistics from `/api/admin/stats` only: students, active languages, total courses, published lessons, vocabulary, quizzes, quiz attempts and pass rate.
- Refresh data button; an API failure surfaces as an error/retry page, not a fictional metric.
- Existing recent student previews and links to management pages retained.

## Students

Student overview adds search (existing), active/inactive filter, name/date sorting, 10-row page navigation, activation/deactivation confirmation, error messages and responsive table overflow. Client pagination is suitable for the demo, but production-sized datasets would benefit from API pagination.

## Lessons, languages, MCQs

- A language with existing students, courses or lessons is **deactivated**, not cascade-deleted; enrollments remain.
- A lesson/course/module with learning history or a flashcard review cannot be deleted. API returns HTTP `409` and asks the admin to unpublish instead.
- MCQ create/edit uses `/api/admin/lessons/{lesson_id}/questions` and `/api/admin/questions/{question_id}` with 2–8 options and exactly one correct. The generic option editor blocks changes that would remove or duplicate the only correct answer.
- No database migration was required; the archive/deactivation uses existing `is_active` / `is_published` columns.

## Remaining limitations

Complex tables elsewhere use their original controls. This is a focused upgrade, not a verified complete usability audit of every CRUD screen. Confirm tablet/mobile layouts and end-to-end admin workflows on a real Windows browser. In-process login rate limiting is not a substitute for shared, persistent rate limiting at scale.
