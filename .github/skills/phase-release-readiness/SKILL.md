---
name: phase-release-readiness
description: "Assess whether an implementation phase or release is complete using acceptance criteria, test evidence, security checks and operational readiness."
argument-hint: "[phase, feature, or slice ID]"
---

# Phase and Release Readiness

Use at the end of a milestone or before release.

## Review
1. Compare implementation against approved requirements and acceptance criteria.
2. Inspect changed files and git diff.
3. Run relevant unit, integration, contract and end-to-end tests.
4. Verify migrations, secrets, permissions and environment configuration.
5. Verify failure recovery, idempotency and logging for background/external operations.
6. Verify docs and operational runbooks.
7. Record remaining known issues and deferred scope.

## Status rules
- PASS: all required criteria met with evidence; no unresolved critical/high issue.
- BLOCKED: a required test, credential, permission, dependency or acceptance criterion is missing.
- NEEDS APPROVAL: a design, product, cost, security or scope decision requires owner choice.

Do not downgrade a failure to a warning merely to pass a phase. No deployment/publishing to production accounts without explicit user approval.
