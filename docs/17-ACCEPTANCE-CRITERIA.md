# Acceptance Criteria — ClipYantra

**Status:** DRAFT; specific numeric thresholds require product-owner approval and baseline measurement.

## A. Foundation

- [ ] Frontend and API start using documented commands.
- [ ] Database migrations apply on clean database.
- [ ] Health/readiness checks distinguish DB, Redis, storage and worker availability.
- [ ] Secrets are absent from browser and logs.

### FOUND-001 slice criteria

- [x] AC-FND-001: Backend with no database URL starts and exposes liveness; readiness truthfully reports database `not_configured`.
- [x] AC-FND-002: With a reachable configured PostgreSQL database, readiness reports database `ready`. Live-runtime evidence is explicitly waived by `ACCEPT SLICE FOUND-001`.
- [x] AC-FND-003: With an unreachable configured PostgreSQL database, readiness is HTTP 503 and does not expose connection credentials.
- [x] AC-FND-004: Health responses contain no secret settings or URLs.
- [x] AC-FND-005: Redis, object storage and worker components are explicit `not_configured` until implemented.
- [x] AC-FND-006: Invalid database configuration produces a sanitized startup error.
- [x] AC-FND-007: Focused tests run from documented commands and evidence distinguishes live and mocked database checks.

## B. Ingestion

- [ ] Supported source file is uploaded and stored outside DB.
- [ ] Actual media streams validated through FFprobe.
- [ ] Rights/provenance record is required before processing.
- [ ] Upload failure can resume/retry without corrupt source.
- [ ] Malformed or disallowed input is rejected with useful error.

### ING-001 slice criteria

- [ ] AC-ING-001-001: Valid local upload request creates and returns source/upload-session IDs.
- [ ] AC-ING-001-002: Identical idempotency key/payload returns the same IDs without duplicate records.
- [ ] AC-ING-001-003: Reused key with different payload returns HTTP 409.
- [ ] AC-ING-001-004: Unknown/blocked rights return HTTP 422 and create no source records.
- [ ] AC-ING-001-005: Source list/detail return persisted metadata and rights without bytes/secrets.
- [ ] AC-ING-001-006: Invalid request fields use the frozen ErrorResponse shape.
- [ ] AC-ING-001-007: Unavailable source store returns HTTP 503 `SOURCE_STORE_UNAVAILABLE`.
- [ ] AC-ING-001-008: Separate SQLAlchemy sessions preserve source/rights data.

## C. AI processing

- [ ] Transcript segments are time-aligned and source-relative.
- [ ] Provider capabilities are checked before requests.
- [ ] Model/provider/version/prompt version is recorded.
- [ ] Candidate timestamps are in source bounds and backed by source transcript/visual evidence.
- [ ] Candidate includes reason, category, score breakdown and confidence/uncertainty.
- [ ] Four content profiles are tested against human-labelled fixtures.
- [ ] Provider failure does not erase completed stages.

## D. Rendering and editor

- [ ] Generated vertical output is playable and meets the active preset.
- [ ] Captions follow timestamps and remain within safe margins.
- [ ] Source clip remains immutable when drafts are edited.
- [ ] Trim/split/merge update captions/B-roll/effects source maps correctly.
- [ ] Undo/redo returns deterministic prior state.
- [ ] B-roll failure does not fail core render when optional fallback is enabled.
- [ ] QA failure prevents publish eligibility.

## E. Publishing

- [ ] OAuth account eligibility/permission is verified.
- [ ] Manual mode requires approval.
- [ ] Automatic mode requires explicit opt-in and policy pass.
- [ ] Duplicate and unknown-outcome cases are reconciled safely.
- [ ] Platform processing/publish state and external ID are retained.

## F. Learning and operations

- [ ] Analytics only show metrics actually returned/authorized.
- [ ] Metric timestamps and definitions are preserved.
- [ ] Job recovery and DB restore are tested.
- [ ] Worker queue and rendering resource use are observable.
- [ ] Cost/latency/quality benchmark report exists for representative inputs.
