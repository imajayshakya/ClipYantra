# Deployment and Operations

**Status:** IN PROGRESS - proposed self-hosted MVP deployment baseline

## 1. Development topology

- Windows development machine: VS Code, source tree, frontend/backend dev, optional local media worker.
- Docker Compose: API, frontend, PostgreSQL, Redis and workers where supported.
- Local media storage for development.
- Azure Blob adapter for remote/cloud storage.
- Optional NVIDIA GPU worker/NIM host, only after runtime compatibility check.

The MVP deployment model is:

- Docker-based.
- Initially one owner/workspace.
- Secure application authentication.
- No billing or subscription module.
- SaaS-ready workspace/brand/resource boundaries.
- Local GPU processing and remote/cloud AI providers are supported but not assumed interchangeable.

## 2. Production topology

Separate API/web from asynchronous workers. Suggested pools:
- CPU/general workers: ingestion, orchestration, analytics.
- AI workers: transcription and model orchestration.
- Media workers: FFmpeg rendering, tracking and QA.
- Publishing workers: platform upload and reconciliation.

Scale workers based on queue depth, media duration, GPU availability and cost. Do not put long FFmpeg jobs inside API request processes.

## 3. Configuration

- Typed settings with validation at startup.
- Separate `.env.example` for names/defaults only; never real secrets.
- Production secret manager or encrypted configuration.
- Per-provider enabled/disabled status and health checks.
- Workspace timezone, retention, maximum duration, upload size and cost budgets configurable.

## 4. Observability

- Structured JSON logs with correlation IDs.
- Metrics: queue depth, stage duration, render throughput, worker memory/GPU use, provider failures, API latency, publish outcomes, storage bytes and cost.
- Traces across API → outbox → worker → provider/media operation.
- Alert on stuck jobs, repeated provider failures, expiring OAuth credentials, storage failures and queue growth.

## 5. Recovery

- Database backups and tested restore.
- Blob lifecycle/backup policy.
- Worker lease expiry/requeue.
- Reconciliation job for orphaned or unknown publishing outcomes.
- Clean temporary workspaces with retention safeguards.
- Graceful shutdown and cancellation checkpoints.

## 6. Raspberry Pi guidance

Raspberry Pi can run lightweight monitoring/control or a small API in constrained deployments, but it should not be assumed to handle high-resolution video rendering or large local AI models. Detect resources and schedule heavy jobs on the development PC, a compatible GPU machine or cloud worker.
