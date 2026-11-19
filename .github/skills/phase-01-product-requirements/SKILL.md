---
name: phase-01-product-requirements
description: "Define product requirements, assumptions, and measurable acceptance criteria."
disable-model-invocation: true
---

# Phase 01 — Product Requirements and Acceptance Criteria

Use `engineering-gates`. Base this document on Phase 00 findings and the user's product baseline. No application code.

Create a complete requirements specification covering:
- Users, workspaces, accounts and roles for initial release and future growth.
- Mixed source ingestion and rights declarations.
- Transcription, word alignment, diarization and language support.
- Four editorial profiles and their distinct selection criteria.
- AI providers and hybrid routing (including NVIDIA hosted API and optional NIM).
- Clip candidate ranking, human review, editing and render presets.
- Brand kit/caption templates.
- Manual, automatic and hybrid publishing per channel/category.
- Instagram and YouTube official API workflows.
- Scheduling, retries, duplicate protection, analytics and cost ledger.
- Security, privacy, retention, accessibility, observability and deployment.

For every requirement assign ID, priority (P0/P1/P2), rationale and testable acceptance criteria. List exclusions for v1. Separate required capability from future enhancement. Flag items needing human decisions.

Create or propose `docs/requirements/PRODUCT-REQUIREMENTS.md` and `TRACEABILITY-MATRIX.md` only if documentation creation is allowed by the current stage; do not create application code. Stop for owner review.


Global rules: Follow `.github/copilot-instructions.md` and the relevant skills. Inspect existing repository state before edits. Do not invent API/model facts. Keep the scope of this prompt only. Do not advance to the next phase automatically. End with a gate report and explicit status.
