# Feature Phase — Production Readiness and Release Audit

Use `phase-release-readiness` and `testing-verification`.

Audit architecture, auth, workspace isolation, OAuth and secret storage, SSRF, upload limits, media retention, dependency/licence inventory, provider cost tracking, logs/metrics/traces, queues, migrations, backups/restore, worker recovery, outbox, idempotency, deployment, CI/CD and operational documentation.

Verify local-only and cloud deployments. Verify NVIDIA GPU detection and fail-safe behavior without a compatible GPU; hosted NVIDIA mode must remain independent. Ensure secrets and private media never enter logs. Run all available checks and report actual output. Provide release blockers, residual risks and rollback plan. Do not deploy or publish to production accounts without explicit owner approval.


Global rules: Follow `.github/copilot-instructions.md` and the relevant skills. Inspect existing repository state before edits. Do not invent API/model facts. Keep the scope of this prompt only. Do not advance to the next phase automatically. End with a gate report and explicit status.
