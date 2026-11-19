---
name: phase-08-implement-one-slice
description: "Implement exactly one explicitly approved vertical slice and validate its behavior."
disable-model-invocation: true
---

# Phase 08 — Implement Exactly One Approved Slice

Use `chunked-development` and `testing-verification`.

Input: the approved slice ID and its acceptance criteria. If no explicit slice ID or approval exists, stop and ask.

1. Inspect git status and the approved design/contracts.
2. Read all affected code and tests.
3. State the exact file-level plan before editing.
4. Implement only this slice; avoid unrelated refactoring.
5. Add/update tests with the behavior.
6. Run targeted tests, lint/type checks and relevant integration tests.
7. Inspect the final diff for secrets, scope creep and untracked artifacts.
8. Update phase status and docs.

Do not automatically implement the next slice. If an architectural decision is needed, stop and create an ADR proposal. Report exact test commands and actual outcomes. End with `SLICE PASS`, `SLICE BLOCKED`, or `NEEDS APPROVAL`.


Global rules: Follow `.github/copilot-instructions.md` and the relevant skills. Inspect existing repository state before edits. Do not invent API/model facts. Keep the scope of this prompt only. Do not advance to the next phase automatically. End with a gate report and explicit status.
