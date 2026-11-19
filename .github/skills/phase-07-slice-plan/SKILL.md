---
name: phase-07-slice-plan
description: "Break approved work into bounded vertical slices with acceptance criteria and dependencies."
disable-model-invocation: true
---

# Phase 07 — Vertical Slice Planning

Use `chunked-development`. No code changes.

Break the next approved milestone into small vertical slices. Each slice must describe one observable user/system behavior and be small enough to implement and test independently.

For each slice provide:
- ID and user outcome.
- In-scope / out-of-scope.
- Dependencies and prerequisite slices.
- Exact likely files/modules to change.
- DB/API/provider contract impact.
- Acceptance criteria.
- Unit/integration/contract/e2e tests.
- Failure/rollback plan.
- Risk and estimated complexity (S/M/L; avoid fake time estimates).
- Required external accounts, credentials or GPU.

Order slices by dependency and risk reduction. Identify a thin end-to-end vertical slice before expanding breadth. Stop and request `APPROVE SLICE <ID>`.


Global rules: Follow `.github/copilot-instructions.md` and the relevant skills. Inspect existing repository state before edits. Do not invent API/model facts. Keep the scope of this prompt only. Do not advance to the next phase automatically. End with a gate report and explicit status.
