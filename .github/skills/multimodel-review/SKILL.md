---
name: multimodel-review
description: "Coordinate independent reviews using different coding models without conflicting edits or treating model consensus as proof."
argument-hint: "[phase, feature, or slice ID]"
---

# Multi-model Review

Use when a design, risk register, provider integration or completed slice needs a second opinion.

## Workflow
1. Freeze the reviewed artifact/commit hash and define the review question.
2. Give each model identical source artifacts and the same checklist.
3. Ask reviewers to report findings only; do not let parallel reviewers modify the same working tree.
4. Require file/line or design-section references and severity.
5. Classify each finding: confirmed, plausible, false positive, or unresolved.
6. Reproduce technical findings using tests/docs.
7. Reconcile disagreements in an ADR or review log.
8. Only the designated implementer applies approved changes.

## Suggested reviewer roles
- Architecture reviewer: coupling, reliability, scalability, security boundaries.
- Model specialist: modality support, endpoint compatibility, schema and fallback.
- Security reviewer: OAuth, SSRF, tokens, media access, secrets, licensing.
- QA reviewer: acceptance criteria, test coverage, failure modes.

Model agreement is not evidence. Official documentation, reproducible tests and inspected code are evidence.
