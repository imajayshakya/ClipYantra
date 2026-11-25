# Product Requirements — ClipYantra

**Status:** APPROVED v1 - requirements baseline approved  
**Version:** PRD-1.0  
**Approval:** `APPROVE REQUIREMENTS v1` and `APPROVE REQUIREMENTS REVIEW v1`  
**Date:** 2026-11-22

## 1. Product vision

ClipYantra turns long-form, rights-cleared video into a set of high-quality, editable short-form assets. It finds complete and compelling moments, creates platform-ready edits, supports human review or a user-configured automated publishing policy, and learns from available performance data.

The product is a workflow platform, not simply an LLM prompt wrapped around FFmpeg.

## 2. Target users

- Solo creators and podcasters repurposing their own recordings.
- Educators and technical creators producing tutorials.
- Gaming creators working with authorized gameplay and stream recordings.
- Entertainment creators producing sketches, commentary and reaction content.
- Small creator teams managing multiple brands and social accounts.

## 3. Primary jobs-to-be-done

1. Import a long video from a permitted source.
2. Understand what was said and shown, with timestamps.
3. Discover several self-contained clip candidates.
4. Review why each candidate was selected and edit it.
5. Render professional short-form variants.
6. Prepare different metadata for each platform.
7. Approve, schedule or automatically publish under explicit policy.
8. Measure available performance and use it to inform future editorial choices.

## 4. Supported source types

- Direct file upload (initially MP4/MOV; additional formats only after decoder validation).
- Authorized direct media URL.
- User-authorized cloud object import (local adapter and Azure Blob first).
- Watched folders for self-hosted installations.
- Platform import only where official/authorized access and user rights are established.
- YouTube/Twitch/Kick links are not a blanket permission to download/reuse media. Import adapters must document supported flows and terms.

## 5. Content profiles

### 5.1 Podcasts / Interviews

Identify complete answers, stories, questions, disagreements, explanations, guest reactions and context. Preserve speaker identity and avoid cuts that remove the question needed to understand an answer.

### 5.2 Educational / Technical

Identify problem → explanation → example/demo → conclusion. Preserve technical terminology, code context and factual caveats. Avoid cutting before a result is demonstrated.

### 5.3 Gaming

Combine transcript, game/audio events, scene changes, facecam reactions and optionally authorized chat/replay data. Support denser/event-triggered frame sampling. Keep gameplay legible and facecam placement configurable.

### 5.4 Entertainment / Funny

Preserve setup → punchline → reaction/payoff. Do not cut off the payoff or use a reaction without its context. Support multi-person layout and expressive captions.

## 6. Functional requirements

### Ingestion and library

- FR-001: User can create a source-video record and upload supported files.
- FR-002: System validates file type, size, duration and media streams before processing.
- FR-003: System records source, rights declaration, provenance and original metadata.
- FR-004: System supports local/Azure storage through an abstraction.
- FR-005: User can resume or safely retry interrupted upload/ingestion.

### Processing

- FR-010: System extracts normalized audio and technical metadata.
- FR-011: System transcribes supported languages and stores timestamped segments.
- FR-012: System can perform word alignment and optional speaker diarization.
- FR-013: System detects scene boundaries and representative frames.
- FR-014: System generates clip candidates with start/end, transcript evidence, category and explanation.
- FR-015: System validates candidate boundaries against source duration and word/scene boundaries.
- FR-016: System ranks candidates using configurable editorial rubric; score is not a guaranteed virality probability.
- FR-017: System supports one or more AI provider evaluations and records disagreements.
- FR-018: System de-duplicates overlapping candidates and can spread candidates across the source.

### Rendering and editing

- FR-020: System renders vertical 9:16 and original-aspect outputs; square output is optional.
- FR-021: System supports captions with word timing, templates and brand configuration.
- FR-022: System supports face/speaker-aware crop modes, with manual override.
- FR-023: System supports audio normalization and validated optional effects.
- FR-024: System supports optional B-roll with source/rights metadata and fail-soft behavior.
- FR-025: System preserves generated originals; edits create new versioned drafts.
- FR-026: Clip Studio exposes video, audio, captions, B-roll and effects timeline tracks.
- FR-027: User can trim, split, merge, reposition overlays, edit captions, crop and export.
- FR-028: Natural-language AI editing returns allow-listed typed operations with preview, validation and undo/redo.

### Metadata and publishing

- FR-030: Generate platform-specific title/caption/description/hashtags/CTA suggestions.
- FR-031: User can edit all metadata before publishing.
- FR-032: Connect eligible Instagram/Facebook and YouTube accounts through OAuth.
- FR-033: Publish and schedule only through official supported APIs.
- FR-034: Support manual, opt-in automatic and hybrid policies per account/category.
- FR-035: Record attempts, external IDs, status, errors and reconciliation state.
- FR-036: Prevent duplicate publication and handle uncertain upload outcomes.

### Analytics and feedback

- FR-040: Store available platform metrics as timestamped snapshots.
- FR-041: Associate analytics with source, candidate, creative variables, model and post.
- FR-042: Compare performance by category, hook, duration, format, provider and schedule.
- FR-043: Use historical data as a recommendation signal, not a guaranteed prediction.

### Administration and operations

- FR-050: Configure model providers, capabilities, default routing and cost limits.
- FR-051: Track task state, progress, worker health, failures and usage.
- FR-052: Support user/workspace/brand separation in the domain model.
- FR-053: Provide audit history for rights, approval, settings and publishing actions.

## 7. Non-functional requirements

- NFR-001: Every long-running operation is asynchronous and restartable.
- NFR-002: PostgreSQL is authoritative for workflow state.
- NFR-003: Job dispatch and external side effects are idempotent/reconcilable.
- NFR-004: API credentials are never exposed to the browser or logs.
- NFR-005: Media is stored outside relational database blobs.
- NFR-006: Every pipeline stage emits structured progress and diagnostics.
- NFR-007: Every generated clip is technically validated before it is publishable.
- NFR-008: Provider failures do not corrupt completed stages.
- NFR-009: Workspace timezone defaults to Asia/Kolkata but is configurable.
- NFR-010: Tests cover services, APIs, workers, adapters, UI and E2E flows.

## 8. MVP scope

MVP includes local upload and direct authorized URLs first, Azure Blob and watched-folder imports as the second priority, transcription, AI candidate discovery for all four profiles, vertical rendering, captions, review/approval, Instagram/Facebook Reels and YouTube Shorts publishing through official APIs after credentials and permissions are approved. Full multi-track timeline editing is desktop-first; tablets support dashboard, preview, clip review, approve/reject, calendar and analytics.

The first release may keep live stream ingestion, automatic trend discovery, multi-tenant billing, AI B-roll and advanced dynamic effects out of scope.

## 9. Explicit non-goals

- Circumvent DRM, login walls, access controls or platform download restrictions.
- Guarantee virality, reach, revenue or platform monetization.
- Publish content without the account owner's explicit authorization.
- Generate misleading edits or remove necessary context.
- Store raw media inside PostgreSQL.
- Let LLM output execute shell commands, Python, FFmpeg arguments or arbitrary code directly.

## 10. Product decisions

Resolved by Product Owner Decision v1:

- OUT-001: self-hosted Docker MVP, initially one owner/workspace, secure authentication, no billing, SaaS-ready boundaries.
- OUT-002: local upload and direct authorized URL first, Azure Blob and watched folders second, authorized platforms third.
- OUT-003: Instagram/Facebook Reels and YouTube Shorts in MVP through official APIs and OAuth.
- RQ-4: desktop-first full timeline editing; tablet supports dashboard, preview, clip review, approve/reject, calendar and analytics.
- FR-050: workspace default, then profile override, then per-job override with local-first/balanced/cloud-first/user-selected modes.

Remaining decisions:

- OUT-004: live-stream monitor remains deferred until a separate product-owner decision.
- OUT-005: AI dubbing and generated B-roll remain deferred until a separate product-owner decision.
