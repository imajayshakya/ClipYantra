# ADR-001: SupoClip-Inspired Product and Architecture Patterns

- **Status:** PROPOSED — not approved
- **Date:** 2026-11-22
- **Decision owners:** Product owner / engineering owner

## Context

SupoClip documents a long-form video → transcript → LLM segment selection → render pipeline, asynchronous worker architecture, SSE progress, face-aware cropping, word-synced captions, B-roll, a multi-track editor, versioned drafts, typed AI edit workflows and platform publishing/performance feedback.

## Decision proposal

Adopt equivalent *product and architecture patterns* in ClipYantra, independently designed and implemented. Keep the current ClipYantra baseline (Next.js, FastAPI, PostgreSQL, Redis/Celery, FFmpeg, provider registry). Do not adopt SupoClip code or change queue framework/ORM without separate approval.

## Accepted patterns

- Async task creation and durable workflow status.
- Stage-level progress stream with status refetch.
- Route/service/repository backend layering.
- Multi-track editor with immutable source output and versioned drafts.
- Typed, reversible AI edit operations.
- Source-map metadata for time-aligned overlays.
- Optional fail-soft B-roll.
- Per-platform render presets.
- Performance feedback loop and layered tests.

## Rejected/deferred

- Direct source-code copy before licence review.
- ARQ migration at this stage.
- Dual ORM/schema ownership.
- Hosted billing and subscription complexity in MVP.
- Unofficial imports/publishing methods.

## Consequences

More editor flexibility and reproducibility, but increased complexity in draft versioning, timeline transforms and source maps. These are post-core-pipeline capabilities and need dedicated acceptance tests.

## Approval

Pending: `APPROVE ADR-001`.
