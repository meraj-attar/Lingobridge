# Password creation policy

The new password-strength component on **student registration** shows an accessible 5-segment meter, requirements checklist, strength label, and show/hide control. React uses `src/utils/passwordPolicy.js`; FastAPI independently enforces matching rules in `app/password_policy.py`.

Rules: 8–128 characters, one uppercase, one lowercase, one number, one special character, and not a listed common/predictable password. The strength meter is heuristic rather than a cryptographic strength guarantee. Failed registrations return HTTP `422` with validation details.

**Existing login compatibility:** login continues to accept existing PBKDF2 password hashes; existing student accounts are not reset or rehashed. Stored passwords remain hashed and no password is added to logs or API responses. Login failures are counted per (IP, email) for short-lived, local in-process throttling; distributed production systems should use shared storage and proxy-aware configuration.

The existing `/forgot-password` page explicitly says self-service account recovery is not configured; this upgrade **does not** add an insecure reset form or an email-sending claim. No authenticated change-password form exists in the supplied source. Implement one only with robust identity verification and revocation design before claiming it works.

Security review remaining: JWT remains a 12-hour HttpOnly cookie with CSRF checks; logout deletes the browser cookie, but already issued JWTs are not centrally revoked. Review deployment security, HTTPS-only cookies, SMTP reset, server-side JWT revocation, shared rate limiting, logs, reverse proxy and host allowlisting before production.
