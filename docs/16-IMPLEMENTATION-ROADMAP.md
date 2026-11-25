# Implementation Roadmap and Approval Gates

**Status:** PROPOSED

## Gate sequence

`Discovery → Requirements → Architecture → Risk prediction → Design approval → Contract freeze → Placeholder scaffold → Slice plan → Implement slice → Test/review → Phase approval`

No agent may jump a gate. Prompts are in `.github/prompts/`.

## Phase 0 — Discovery and requirements

- Inspect existing repository, hardware, git history, test commands and dependencies.
- Confirm product scope, tenancy, first supported sources and platforms.
- Output discovery report and PRD questions.
- Gate: `APPROVE REQUIREMENTS v1`.

## Phase 1 — Architecture and risk

- Create context/container/component diagrams, sequence diagrams, ADRs and risk register.
- Validate stack against repository/hardware.
- Review SupoClip patterns and legal boundary.
- Gate: `APPROVE DESIGN v1`.

## Phase 2 — Contracts

- Freeze entities/state machines, Pydantic schemas, API/OpenAPI shape, event contracts and storage conventions.
- Gate: `APPROVE CONTRACTS v1`.

## Phase 3 — Placeholder scaffold

- Create approved folders, empty modules, config samples, health endpoints, migrations skeleton and CI skeleton only.
- No fake integration success or unapproved feature logic.
- Gate: `APPROVE SCAFFOLD v1`.

## Phase 4 — Vertical slices

Suggested order:

1. `FOUND-001`: app health, config and DB connectivity.
2. `ING-001`: upload session and source record.
3. `ING-002`: FFprobe validation and storage adapter.
4. `JOB-001`: durable job + outbox + worker + progress events.
5. `TRN-001`: local transcription to normalized transcript.
6. `TRN-002`: provider fallback/alignment/diarization.
7. `AI-001`: candidate discovery from transcript and deterministic signals.
8. `AI-002`: multimodal evaluation and profile-specific ranking.
9. `REN-001`: vertical render and technical QA.
10. `EDIT-001`: draft clip, captions, trim/crop and version history.
11. `EDIT-002`: timeline, source maps and typed AI edit operations.
12. `PUB-001`: OAuth/account connection for first platform.
13. `PUB-002`: approved publish, status polling and reconciliation.
14. `PUB-003`: second platform and scheduler.
15. `AN-001`: analytics snapshots and recommendations.

Each slice needs an issue/spec, defined files, tests, non-goals and explicit approval.

## Phase 5 — Production hardening

Security review, resource limits, retention, monitoring, backups/restore, load/failure tests and operational runbooks.

## Definition of done for every slice

- Acceptance criteria pass.
- Tests run and exact output recorded.
- No unapproved architecture/contract change.
- Logs/errors are actionable without leaking sensitive data.
- Documentation and `PHASE-STATUS.md` updated.
- Independent review completed.
- Human approval requested before next slice.
