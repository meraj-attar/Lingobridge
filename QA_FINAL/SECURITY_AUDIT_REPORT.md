# Independent Security Audit — LingoBridge

**Date:** 31 October 2026  
**Scope:** FastAPI auth, routing, admin CRUD, question/video mutation, audio upload, student listing, frontend API transport; isolated tests. Not a penetration test or production security certification.

| Topic | Severity / Status | Evidence and action |
|---|---|---|
| JWT signing / expiration | PARTIAL PASS | HS256+issuer configured, signed 12-hour cookie, `exp/sub/csrf/iss` now required. Five signed malformed-token tests PASS. No server-side revocation. |
| Logout / stolen cookie | **HIGH OPEN** | `/api/auth/logout` removes client cookie only. Existing token remains cryptographically valid until expiry. Implement DB/shared-store revocation and test across workers before production. |
| Distributed login throttling | **HIGH OPEN** | In-process Python dict keyed by IP+email, 8 failed attempts/15 minutes. No shared store across worker processes and not a global IP gate. Use trusted reverse-proxy + centralized limiter. |
| Auth and roles | PARTIAL PASS | `current_user`, admin dependencies, CSRF protected mutations, student forbidden from admin endpoint in new tests. Full authorization matrix/browser testing NOT RUN. |
| Password security | SOURCE REVIEW | Salted PBKDF2-HMAC-SHA256 with 390,000 iterations, password-policy validation for registration. External password risk review NOT RUN. |
| CSRF / cookie | PARTIAL PASS | HttpOnly cookie, SameSite Lax and CSRF header on writes. `COOKIE_SECURE=true` must be enforced with HTTPS in deployment. |
| MCQ integrity | SQLITE PASS | 2–8 choices, one correct answer, parent row lock for PG, failed mutations state unchanged. **PG concurrency NOT RUN.** |
| Video links | SQLITE + UNIT PASS | Only explicit HTTPS YouTube hosts and 11-character video IDs; reject unsafe schemes, userinfo, deceptive hostnames and custom ports; both lesson create/update validated. Legacy unsafe DB records not automatically cleaned. |
| Audio upload | SOURCE REVIEW | Admin-only, whitelist MIME + byte signatures + decoding, 5 MiB cap, removes rejected temp file. Fuzz testing NOT RUN. |
| Admin student listing | FIXED / SQLITE PASS | Added server-side page boundaries (page_size max 50), validated search/sort/status, SQLAlchemy parameterization and literal wildcard escaping; UI wired to API. Browser behavior NOT RUN. |
| Generic admin listing | **MEDIUM OPEN** | `GET /api/admin/manage/{table}` still loads entire table; integrate pagination plus UIs before scale. |
| SQL injection | SOURCE REVIEW + SELECTIVE TESTS | ORM queries and escaped case-insensitive search; no comprehensive fuzzing. |
| N+1 queries / performance | **MEDIUM OPEN** | Student detail contains multiple queries per student, now capped by page size. Other listings and course summaries may be costly. Explain/query-plan/load test. |
| Rate limit other endpoints | OPEN / NOT VERIFIED | No comprehensive endpoint-wide throttling / rate control established. |
| CORS | SOURCE REVIEW | Allowed origins come from `FRONTEND_ORIGIN`, credentials=true; verify exact trusted deploy domains. |
| Dependency vulnerabilities | **NOT RUN** | Registry unavailable; no npm audit or real package lock, no environment-equivalent Python audit. |
| Headers | SOURCE REVIEW | `nosniff`, referrer policy, frame denial, frame-ancestors CSP, cache no-store for auth. Full CSP/XSS hardening and browser verification remain open. |

### Release security conclusion

Significant improvements are independently tested, but **HIGH issues remain**: reusable JWT after logout, distributed login throttling, and missing real deployment testing. Do not claim high-security/production certification. The audit did not test malicious concurrency on PostgreSQL, external services, real browser sessions, rate-limit flooding, or dependency CVEs.
