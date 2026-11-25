---
name: phase-gate
description: Evaluate evidence for a phase and request human authorization to continue.
---

# Phase Gate

Evaluate the current phase against its acceptance criteria and the independent review.

Require actual evidence: commit/diff, exact test commands/results, migration status, E2E results if applicable, security/licence review and known limitations. No inferred test passes. Update `docs/engineering/PHASE-STATUS.md` only with observed evidence.

Return phase verdict and unresolved risks. Do not begin next phase. Ask for one explicit human action: approve phase, request fixes or defer.