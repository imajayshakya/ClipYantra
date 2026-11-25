---
name: independent-review
description: Review one slice independently for correctness, safety and maintainability.
---

# Independent Review

Review the approved slice diff as an independent reviewer. Do not edit files unless asked to prepare a separate fix proposal.

Check: requirements coverage, regressions, auth/workspace boundaries, secret handling, SQL/migrations, concurrency, idempotency, time/timestamp math, AI-output validation, file/resource safety, rights/licensing, platform API usage, tests and observability.

Report findings by severity with file/line references, reproduction steps and required tests. Distinguish blocker from suggestion. Do not approve your own implementation. Finish `PASS`, `BLOCKED` or `NEEDS FIXES`.