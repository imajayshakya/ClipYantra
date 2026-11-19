---
name: phase-09-independent-test-review
description: "Test and independently review one completed slice against its acceptance criteria."
disable-model-invocation: true
---

# Phase 09 — Independent Test and Code Review

Use `testing-verification` and `multimodel-review`. Review the current slice/diff only. Prefer a separate QA Reviewer agent or a second model/harness. Findings only; do not modify files.

Check:
- Acceptance criteria and traceability.
- Correctness and error handling.
- Tests and uncovered edge cases.
- Security, secrets, permissions and data privacy.
- Idempotency, retries and recovery.
- Provider capability and response validation.
- Media timestamp/render quality where applicable.
- Platform API compliance where applicable.
- Documentation and migrations.

Report findings by severity with file/line evidence. Distinguish actual defects from concerns. Do not claim tests were run unless executed. The implementer may fix only confirmed findings within this slice, then rerun tests. Stop for human gate review.


Global rules: Follow `.github/copilot-instructions.md` and the relevant skills. Inspect existing repository state before edits. Do not invent API/model facts. Keep the scope of this prompt only. Do not advance to the next phase automatically. End with a gate report and explicit status.
