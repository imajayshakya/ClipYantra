---
name: phase-15-clip-review-studio
description: "Build a human review workflow for inspecting and approving generated clips."
disable-model-invocation: true
---

# Feature Phase — Clip Review Studio

Implement the approved frontend/backend slice for reviewing candidates and rendered clips.

Required UX: source preview, transcript synced to time, candidate cards, editorial score/rationale, start/end adjustment, subtitle correction, crop controls, template selection, rerender, version history, approve/reject and platform-specific metadata editor. Persist all changes and retain source lineage. Use typed APIs, loading/error/empty states and keyboard-accessible controls. Do not create UI controls with no backend behavior. Add component/API tests. Stop at gate.


Global rules: Follow `.github/copilot-instructions.md` and the relevant skills. Inspect existing repository state before edits. Do not invent API/model facts. Keep the scope of this prompt only. Do not advance to the next phase automatically. End with a gate report and explicit status.
