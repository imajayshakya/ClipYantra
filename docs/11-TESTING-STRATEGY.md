# Testing Strategy

**Status:** PROPOSED

## 1. Test pyramid

### Unit tests

- Domain state transitions.
- Timestamp math and source-map transformations.
- Provider capability routing.
- Pydantic schema validation.
- Candidate scoring and deduplication.
- Edit operation validation/undo.
- Publish idempotency and state machine.

### Integration tests

- PostgreSQL repositories/migrations.
- Redis/Celery dispatch and retry.
- Storage adapters.
- FFmpeg probe/render against small licensed fixtures.
- Provider adapters with mocked HTTP responses.
- OAuth callback validation.
- Outbox and scheduler reconciliation.

### Frontend tests

- Components and hooks (Vitest/Testing Library).
- Form validation and editor state.
- Accessibility checks.

### End-to-end tests

- Upload → process → candidate → render → QA → edit → approve → mock publish.
- Reconnect/retry and interrupted task recovery.
- SSE reconnect/refetch.
- Workspace isolation and permission denial.

## 2. Media fixtures

Create short, rights-cleared, synthetic or public-domain fixtures for:
- Single-speaker podcast.
- Two-speaker interview with overlap.
- Hindi/English/Hinglish sample speech.
- Educational screen share/code.
- Gameplay with facecam and action moments.
- Comedy setup/punchline.
- No-audio, variable frame rate, rotated video, corrupt and long-duration edge cases.

Do not commit copyrighted sample media without permission. Large media fixtures may be stored in controlled CI artifact storage.

## 3. Model evaluation tests

Maintain a human-labelled benchmark set with expected moment ranges and annotations. Measure candidate recall, precision, boundary tolerance, completeness, context, language accuracy, false positive rate, latency and cost. Evaluate provider changes against a fixed prompt/data revision.

## 4. Required commands

Define and document actual repository commands after discovery. Proposed categories:
- backend lint/typecheck/unit/integration
- frontend lint/typecheck/unit
- migration validation
- container build
- E2E tests
- security/dependency scan

Do not invent command results. CI must run the same authoritative scripts as local development where possible.

## 5. Release evidence

For each slice, record commit, changed files, command, exit code, test count, skipped tests, known failures and reviewer findings. A green unit test suite does not by itself prove live Meta/YouTube publishing works; connected integration testing is separately labelled.
