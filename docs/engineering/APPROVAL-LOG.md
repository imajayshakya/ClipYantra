# Human Approval Log

Record every material approval in this table. An agent must not add an approval on behalf of the user.

| Date | Gate | Version/ID | Approval token | Approved scope/notes |
|---|---|---|---|---|
| 2026-11-23 | Architecture | v1 | APPROVE ARCHITECTURE v1 | Architecture document `docs/02-ARCHITECTURE.md` approved as proposed. Logical components, data flow, worker model, storage abstraction, AI/provider registry, publishing and analytics isolation. Resilience boundaries and observability guidelines accepted. |
| 2026-11-23 | Full Design | v1 | APPROVE DESIGN v1 | UX, IA, visual direction, wireframes, design system, interaction, responsive, accessibility and visual QA plan approved for contract freeze and later implementation slices. |
| 2026-11-23 | Contracts | v1 | APPROVE CONTRACTS v1 | Entity/migration, Pydantic/API, SSE, state, edit/source-map, storage, provider-routing, idempotency, outbox and lease contracts frozen as documented. |
| 2026-11-23 | Placeholder Scaffold | v1 | APPROVE SCAFFOLD v1 | Authorized placeholder-only folders, empty interfaces, settings skeleton, health check skeleton, migration/CI/Docker skeleton and README updates. No business logic or dependencies authorized. |
| 2026-11-23 | Vertical Slice | FOUND-001 v1 | APPROVE SLICE FOUND-001 | Authorized app health, typed config and PostgreSQL readiness foundation only. Live PostgreSQL integration remains evidence-dependent. |
| 2026-11-23 | Vertical Slice Acceptance | FOUND-001 v1 | ACCEPT SLICE FOUND-001 | Accepted implementation and 16-test evidence. Live PostgreSQL runtime test/AC-FND-002 evidence is explicitly waived; no next slice is authorized. |
| 2026-11-23 | Vertical Slice | ING-001 v1 | APPROVE SLICE ING-001 | Authorized local upload-session and source-record vertical slice only. No media byte transfer, FFprobe, storage adapter, worker or processing behavior authorized. |
