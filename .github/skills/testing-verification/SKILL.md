---
name: testing-verification
description: "Create and execute tests, verify changed behavior, distinguish mocks from real integrations, and produce evidence-based release/gate reports."
argument-hint: "[phase, feature, or slice ID]"
---

# Testing and Verification

Use after each implementation slice and before a phase/release gate.

## Test layers
- Unit: pure functions, validation, score normalization, timestamp arithmetic, provider capability rules.
- Component: repositories, services, task state transitions, render command construction.
- Integration: PostgreSQL, Redis/Celery, local storage, FFmpeg, provider mocks.
- Contract: OpenAPI schemas, provider adapters, OAuth callbacks and publishing request schemas.
- End-to-end: upload→transcribe→candidate→render→review→publish using fixtures and sandbox/test accounts.
- Resilience: timeouts, duplicate task delivery, worker restart, partial upload, provider outage, uncertain publish outcome.

## Rules
- Never label a mocked API test as a live provider test.
- Never claim a test passed without running the exact command and inspecting its exit code/output.
- Record tests skipped and why.
- Use small deterministic media fixtures; do not commit copyrighted sample videos or secrets.
- Include Hindi/English/Hinglish transcript fixtures where permitted.
- Include gaming and comedy edge cases in the benchmark corpus.
- Validate media output with FFprobe and playback/synchronization checks.
- Check migrations both forward and, where supported, rollback/restore strategy.

## Report format
Scope; files changed; commands run; test counts/results; untested risks; security/quality findings; regressions; gate status. For failures, include concise relevant logs and a reproduction path.
