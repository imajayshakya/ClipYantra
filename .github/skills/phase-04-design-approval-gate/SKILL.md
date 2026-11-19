---
name: phase-04-design-approval-gate
description: "Enforce explicit human design approval before contracts or implementation proceed."
disable-model-invocation: true
---

# Phase 04 — Design Approval Gate

Act as the release manager. Do not edit files or start implementation.

Summarize the proposed design in a decision pack:
- Confirmed product requirements and exclusions.
- Architecture and module boundaries.
- Chosen tech stack and alternatives.
- Data/API contract decisions.
- NVIDIA provider plan and unknowns.
- Source rights and platform API assumptions.
- Deployment assumptions and cost drivers.
- Top risks and mitigations.
- Milestones and acceptance gates.
- Open questions requiring owner decisions.

Separate decisions already supported by repository evidence from recommendations and assumptions.

End with exactly one of:
- `NEEDS APPROVAL — no code may be changed.`
- `BLOCKED — list the blocker.`

Wait until the owner explicitly sends `APPROVE DESIGN v1` (or a revised version). A request for changes is not approval. After approval, record the approved design version and proceed only to contracts/data model.


Global rules: Follow `.github/copilot-instructions.md` and the relevant skills. Inspect existing repository state before edits. Do not invent API/model facts. Keep the scope of this prompt only. Do not advance to the next phase automatically. End with a gate report and explicit status.
