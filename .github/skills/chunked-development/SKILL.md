---
name: chunked-development
description: "Plan and implement one small vertical slice at a time with scope limits, tests, evidence and approval gates."
argument-hint: "[phase, feature, or slice ID]"
---

# Chunked Development

Use for implementation after design/contracts are approved.

## Slice sizing
A slice should deliver one observable behavior and normally touch a small, coherent set of modules. If it spans many subsystems, split it. Avoid broad multi-feature prompts.

## Before coding
- Read the approved design, ADRs, acceptance criteria and current phase status.
- Inspect relevant source/tests and `git status`.
- State slice ID, outcome, in/out of scope, affected files, dependencies, migration implications and test plan.
- Request `APPROVE SLICE <ID>` if not already explicitly approved.

## During coding
- Implement only the named slice.
- Follow existing patterns.
- Add/adjust tests with behavior.
- Keep provider/platform calls behind adapters.
- Add structured logs and useful error states.
- Handle retry/idempotency where relevant.
- Do not change unrelated files.
- Stop if scope expands or a new architectural decision is needed.

## After coding
- Run targeted tests first, then relevant full checks.
- Inspect diff for secrets, accidental changes and generated files.
- Report commands and pass/fail results accurately.
- List changed files and acceptance criteria satisfied/not satisfied.
- Update phase status and ADRs if approved.
- Do not start another slice automatically. Ask for the next approval.
