---
name: architecture-design
description: "Create and review system architecture, component boundaries, sequence diagrams, API contracts and architecture decision records for AI AutoClip Studio which named as ClipYantra."
argument-hint: "[phase, feature, or slice ID]"
---

# Architecture Design

Use during requirements/design phases or when a proposed change crosses module boundaries.

## Context
AI AutoClip Studio which named as ClipYantra supports mixed authorized video inputs; hybrid local/cloud inference; NVIDIA (hosted API and optional self-hosted NIM), Gemini, OpenAI, Anthropic, Groq, Deepgram, Ollama/Qwen and WhisperX; four content profiles (podcast/interview, educational/technical, gaming, entertainment/funny); vertical video rendering; review; and manual/automatic/hybrid publishing to Instagram and YouTube.

## Procedure
1. Inspect existing repository and deployment constraints; do not assume a greenfield app.
2. Identify actors, boundaries, trust boundaries and external dependencies.
3. Define modules for ingestion, media metadata, transcription/alignment, scene/frame sampling, video understanding, highlight detection/ranking, rendering/QA, review, publishing, scheduler, analytics, provider routing and observability.
4. Define data ownership and durable state. PostgreSQL is the workflow source of truth; Redis/Celery only transports/executes tasks; media bytes belong in object/file storage.
5. Define sequence diagrams for upload→process→render→review→publish and failure recovery.
6. Define API, event, persistence and provider adapter contracts.
7. Address retries/idempotency, cancellation, job leases, outbox, reconciliation, retention and cleanup.
8. Address security: OAuth, secret management, SSRF-safe URL ingestion, signed media URLs, access control, rights declaration and audit logs.
9. Record material decisions in ADRs with context, options, decision, consequences and status.
10. Identify alternatives and explain why rejected.

## Required output
- Context/container/component view.
- Component responsibility matrix.
- Key sequence diagrams (Mermaid where helpful).
- Data flow and trust boundaries.
- API/event contracts.
- Failure/retry model.
- Deployment topology (local development, cloud, optional GPU worker).
- ADR list and unresolved decisions.
- Risks and acceptance criteria.

Do not produce implementation code during design. Do not overengineer multi-tenancy, microservices or Kubernetes without a demonstrated requirement.
