# Definition of Ready and Definition of Done

## Definition of Ready (slice may start only when all apply)
- Slice has a unique ID and one clear user/business outcome.
- Parent FR/NFR and AC IDs are approved.
- Scope, non-scope, dependencies and assumptions are explicit.
- Relevant UX, architecture, API/data/event contracts are approved/frozen.
- Test cases and test data are defined.
- Risks, security/privacy/rights impact and rollback are considered.
- Implementation plan is limited and reviewable.
- Human explicitly approves the slice.

## Definition of Done (slice may be submitted for acceptance only when all apply)
- Approved scope implemented without unrelated changes.
- Code reviewed; no unresolved critical/high findings.
- Unit/component tests pass.
- Relevant integration/contract/E2E tests pass.
- Static checks/type checks/build pass where configured.
- Visual/accessibility/security/performance checks completed where applicable.
- Acceptance criteria have evidence and traceability is updated.
- Defects are fixed or formally accepted/deferred by the human.
- Logs, docs, migrations and rollback notes updated.
- Independent verification completed.
- Phase status and changelog updated.

Human acceptance remains a separate explicit action; an agent cannot self-accept its work.
