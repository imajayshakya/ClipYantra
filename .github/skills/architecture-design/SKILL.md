---
name: architecture-design
description: Design and review the ClipYantra technical architecture without implementation.
---

# Architecture Design

Create/validate architecture using approved requirements and actual repository constraints.

Must cover: system context, containers/components, ingestion, async job/outbox, worker pools, provider/capability routing, media pipeline, Clip Studio, storage, PostgreSQL, realtime progress, publishing, analytics, observability, security and deployment.

Compare Redis/Celery with alternatives only if justified. SupoClip uses Redis/ARQ and documents SSE, layered services/repositories, a multi-track editor, immutable draft versions and typed AI edit operations. Evaluate these patterns; do not blindly copy its stack or source.

Deliver Mermaid diagrams, responsibilities, failure boundaries, sequence diagrams, technology rationale, ADRs and open questions. No source code or dependency installation. Finish `NEEDS APPROVAL`.