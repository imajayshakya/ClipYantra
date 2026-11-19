---
name: phase-05-contracts-and-data-model
description: "Define approved API contracts and data models without implementing application behavior."
disable-model-invocation: true
---

# Phase 05 — Contracts and Data Model

Proceed only if the owner has explicitly approved the design. Verify the approval message and approved version first. If absent, STOP.

Use `architecture-design` and `engineering-gates`.

Define and review:
- Database entities, relationships, keys, indexes, retention and migration strategy.
- API request/response schemas and error envelope.
- Job/task state machine and transition rules.
- Provider adapter contracts and capability schema.
- Media asset and timestamp conventions (integer milliseconds internally, UTC for persisted times).
- Publishing state machine and idempotency/reconciliation contract.
- Outbox/event contracts.
- OAuth credential references and secret handling.

Do not implement application behavior. Documentation and schema/interface definitions are allowed only within the approved design scope. Include examples and contract tests proposal. Stop for explicit `APPROVE CONTRACTS v1`.


Global rules: Follow `.github/copilot-instructions.md` and the relevant skills. Inspect existing repository state before edits. Do not invent API/model facts. Keep the scope of this prompt only. Do not advance to the next phase automatically. End with a gate report and explicit status.
