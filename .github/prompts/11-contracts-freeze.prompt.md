---
name: contracts-freeze
description: Define database, API, events and state contracts after design approval.
agent: architect
---

Proceed only if the conversation contains explicit `APPROVE DESIGN v1` (or the owner-approved version).

Define and cross-check:
- Entity relationships and migration plan.
- Pydantic request/response schemas.
- API endpoints and error contract.
- Job/event/SSE contracts.
- Processing, clip-version and publishing state machines.
- Idempotency, outbox and lease semantics.
- Storage keys and source-map format.

Add schema examples and contract tests plan. Do not implement business logic. Request `APPROVE CONTRACTS v1`.
