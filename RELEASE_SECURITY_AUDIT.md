# LingoBridge — targeted security review

This review is limited to the code and checks actually performed. It is not a penetration test or a production-security certification.

| Issue / control | Severity | Verified finding / status |
|---|---|---|
| Persisted untrusted video URL and fallback href | Medium | Fixed server validation and sanitized external link; tested URL cases |
| MCQ history and content integrity | High/Medium | Fixed option boundary; 67 new Python regression cases |
| Admin-only role protection | High if absent | Relevant guest/student write endpoints tested and denied; other endpoints previously covered in base suite, not individually retested for this release |
| Password hash storage | Informational | Existing PBKDF2-HMAC SHA-256 hashing preserved, tests pass |
| CSRF on cookie-authenticated write APIs | Informational | Existing nonce-based check preserved, base tests pass |
| JWT expiration / inactive account | Informational | Existing 12-hour expiration and active-status checks reviewed; no complete revocation mechanism verified |
| Logout token revocation | Medium | Outstanding: logout clears the client cookie, but an independently copied unexpired JWT is not server-revoked. Requires a server-side denylist/token-version design for full revocation |
| Login rate limits across multiple servers | Medium | Outstanding: existing throttle is in-memory and per-process; use a shared store such as Redis for distributed deployment |
| Secure cookie production default | Low | This release defaults `COOKIE_SECURE=true` when `ENVIRONMENT=production`; explicit deployment config can override it. Verify HTTPS reverse proxy before production |
| Upload content/size limits | Informational | Existing audio type/header/decoding and 5 MB cap reviewed, not exhaustively fuzz-tested |
| Database SQL injection | Informational | Inspected changed routes use SQLAlchemy query constructs; no exploitability claim for unreviewed third-party dependencies |
| Large admin listing / pagination | Medium | Outstanding: multiple admin list endpoints materialize full result sets; add server-side pagination for large deployments |
| PostgreSQL concurrency | Unverified | Parent row `FOR UPDATE` used to serialize options; not tested against real PostgreSQL here |
| Frontend CSRF / XSS / injection | Unverified | No running browser or independent penetration test; safe external YouTube destination now verified at source level |

**No critical vulnerability is newly confirmed in the tested paths**, but unresolved medium concerns remain and untested areas could contain serious issues. These are documented rather than silently treated as production-secure. Production release requires additional hardening and staging verification.
