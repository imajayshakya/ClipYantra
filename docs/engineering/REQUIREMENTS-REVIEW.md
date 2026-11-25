# Requirements Review Report

**Status:** IN PROGRESS  
**Version:** v1  
**Date:** 2026-11-22  
**Prerequisites:** APPROVE DISCOVERY v1 ✓, APPROVE REQUIREMENTS v1 ✓

## Executive Summary

Review of `docs/01-PRODUCT-REQUIREMENTS.md` (PRD v0.1) against repository discovery findings and the approved requirements baseline (68 requirements, 24 acceptance criteria in session DB). This review identifies confirmed requirements, gaps, conflicts, and open decisions needing product-owner resolution.

---

## 1. Requirements Confirmed (No Changes)

### Business Requirements (7/7 Confirmed)

| ID | Title | Status | Notes |
|---|---|---|---|
| BR-001 | Content Repurposing Platform | CONFIRMED | Core product vision aligns with PRD Section 1 |
| BR-002 | Multi-Profile Content Discovery | CONFIRMED | 4 profiles defined in PRD Section 5 |
| BR-003 | Human-in-the-Loop Editing | CONFIRMED | FR-028 + FR-027 mandate preview/validation/undo |
| BR-004 | Official API Publishing Only | CONFIRMED | FR-033 + CON-003 explicit non-goal |
| BR-005 | Restartable Async Pipeline | CONFIRMED | NFR-001 + NFR-008 mandate restartability |
| BR-006 | Cost-Bounded AI Processing | CONFIRMED | FR-050 + CON-007/008 hardware constraints |
| BR-007 | Multi-Workspace Brand Separation | CONFIRMED | FR-052 domain model requirement |

### Functional Requirements — Ingestion & Library (5/5 Confirmed)

| ID | Title | Status | Notes |
|---|---|---|---|
| FR-001 | Source video record & upload | CONFIRMED | PRD FR-001 |
| FR-002 | File validation before processing | CONFIRMED | PRD FR-002 |
| FR-003 | Rights declaration & provenance | CONFIRMED | PRD FR-003 + CON-001 |
| FR-004 | Storage abstraction (Local/Azure) | CONFIRMED | PRD FR-004 |
| FR-005 | Resumable upload/ingestion | CONFIRMED | PRD FR-005 + NFR-001 |

### Functional Requirements — Processing (9/9 Confirmed)

| ID | Title | Status | Notes |
|---|---|---|---|
| FR-010 | Audio extraction & metadata | CONFIRMED | PRD FR-010 |
| FR-011 | Timestamped transcription | CONFIRMED | PRD FR-011/012 |
| FR-012 | Speaker diarization (optional) | CONFIRMED | PRD FR-012 |
| FR-013 | Scene boundary detection | CONFIRMED | PRD FR-013 |
| FR-014 | Clip candidate generation | CONFIRMED | PRD FR-014 |
| FR-015 | Candidate boundary validation | CONFIRMED | PRD FR-015 |
| FR-016 | Configurable editorial ranking | CONFIRMED | PRD FR-016 + CON-002 |
| FR-017 | Multi-provider evaluation | CONFIRMED | PRD FR-017 |
| FR-018 | Candidate de-duplication & spreading | CONFIRMED | PRD FR-018 |

### Functional Requirements — Rendering & Editing (8/8 Confirmed)

| ID | Title | Status | Notes |
|---|---|---|---|
| FR-020 | Multi-aspect rendering | CONFIRMED | PRD FR-020 |
| FR-021 | Caption system with templates | CONFIRMED | PRD FR-021 |
| FR-022 | Face/speaker-aware cropping | CONFIRMED | PRD FR-022 |
| FR-023 | Audio normalization & effects | CONFIRMED | PRD FR-023 |
| FR-024 | B-roll support (fail-soft) | CONFIRMED | PRD FR-024 + OUT-005 |
| FR-025 | Immutable originals & versioned drafts | CONFIRMED | PRD FR-025 + D-005 |
| FR-026 | Multi-track timeline in Clip Studio | CONFIRMED | PRD FR-026 |
| FR-027 | Core edit operations | CONFIRMED | PRD FR-027 |

### Functional Requirements — Metadata & Publishing (7/7 Confirmed)

| ID | Title | Status | Notes |
|---|---|---|---|
| FR-030 | Platform-specific metadata generation | CONFIRMED | PRD FR-030 |
| FR-031 | Editable metadata before publish | CONFIRMED | PRD FR-031 |
| FR-032 | OAuth account connection | CONFIRMED | PRD FR-032 |
| FR-033 | Official API publishing only | CONFIRMED | PRD FR-033 + CON-003 |
| FR-034 | Configurable publishing policies | CONFIRMED | PRD FR-034 |
| FR-035 | Publish audit trail | CONFIRMED | PRD FR-035 |
| FR-036 | Duplicate prevention & reconciliation | CONFIRMED | PRD FR-036 |

### Functional Requirements — Analytics (4/4 Confirmed)

| ID | Title | Status | Notes |
|---|---|---|---|
| FR-040 | Platform metrics snapshots | CONFIRMED | PRD FR-040 |
| FR-041 | Analytics association | CONFIRMED | PRD FR-041 |
| FR-042 | Performance comparison | CONFIRMED | PRD FR-042 |
| FR-043 | Historical data as signal | CONFIRMED | PRD FR-043 |

### Functional Requirements — Admin & Operations (4/4 Confirmed)

| ID | Title | Status | Notes |
|---|---|---|---|
| FR-050 | Provider/capability configuration | CONFIRMED | PRD FR-050 |
| FR-051 | Task state & health monitoring | CONFIRMED | PRD FR-051 |
| FR-052 | Workspace/brand separation | CONFIRMED | PRD FR-052 |
| FR-053 | Comprehensive audit history | CONFIRMED | PRD FR-053 |

### Non-Functional Requirements (10/10 Confirmed)

| ID | Title | Status | Notes |
|---|---|---|---|
| NFR-001 | Async restartable operations | CONFIRMED | PRD NFR-001 |
| NFR-002 | PostgreSQL authoritative workflow state | CONFIRMED | PRD NFR-002 + D-003 |
| NFR-003 | Idempotent job dispatch | CONFIRMED | PRD NFR-003 |
| NFR-004 | Server-side credentials only | CONFIRMED | PRD NFR-004 |
| NFR-005 | Media outside relational DB | CONFIRMED | PRD NFR-005 + CON-005 |
| NFR-006 | Structured progress & diagnostics | CONFIRMED | PRD NFR-006 |
| NFR-007 | Technical validation before publish | CONFIRMED | PRD NFR-007 |
| NFR-008 | Provider failure isolation | CONFIRMED | PRD NFR-008 |
| NFR-009 | Configurable workspace timezone | CONFIRMED | PRD NFR-009 (default Asia/Kolkata) |
| NFR-010 | Comprehensive test coverage | CONFIRMED | PRD NFR-010 |

### Constraints (8/8 Confirmed)

| ID | Title | Status | Notes |
|---|---|---|---|
| CON-001 | No DRM/access control circumvention | CONFIRMED | PRD Section 9 |
| CON-002 | No virality guarantees | CONFIRMED | PRD Section 9 |
| CON-003 | No unauthorized publishing | CONFIRMED | PRD Section 9 |
| CON-004 | No misleading edits | CONFIRMED | PRD Section 9 |
| CON-005 | No database blobs for media | CONFIRMED | PRD Section 9 + NFR-005 |
| CON-006 | No arbitrary code execution | CONFIRMED | PRD Section 9 |
| CON-007 | Hardware: AMD GPU only (no NVIDIA) | CONFIRMED | **Discovery finding** — AMD Ryzen 5 3500U, Vega 8 2GB VRAM |
| CON-008 | RAM constrained (~686MB free) | CONFIRMED | **Discovery finding** — 6GB total, limited headroom |

---

## 2. Requirements with Changes/Clarifications Needed

### 2.1 FR-028 Natural-Language AI Editing — Clarification Required

**Current PRD wording:** "Natural-language AI editing returns allow-listed typed operations with preview, validation and undo/redo."

**Gap identified:** 
- "Allow-listed typed operations" needs explicit enumeration
- No specification of supported natural language intents (trim, split, crop, caption edit, reorder, etc.)
- No definition of validation rules for each operation type
- No specification of fallback behavior when NL parsing fails

**Proposed clarification:**
- Define explicit operation schema: `{ type: 'trim' | 'split' | 'merge' | 'crop' | 'caption_edit' | 'reorder' | 'broll_insert', params: ... }`
- Require schema validation before execution
- Define confidence threshold for auto-apply vs preview-only

### 2.2 FR-050 Provider/Capability Configuration — Scope Expansion

**Current PRD wording:** "Configure model providers, capabilities, default routing and cost limits."

**Gap identified:**
- Hardware constraint CON-007 (no NVIDIA GPU) means local inference via Ollama/Qwen must be evaluated for feasibility on AMD Vega 8
- NVIDIA API Catalog vs NIM are separate adapters (D-001, provider-integration skill)
- Capability registry must distinguish modalities: transcription, vision, reasoning, multimodal

**Proposed addition:** Explicit capability matrix per provider (API Catalog, NIM, Gemini, OpenAI, Anthropic, Groq, Deepgram, Ollama/Qwen, WhisperX) with supported modalities, rate limits, cost per unit.

### 2.3 NFR-010 Comprehensive Test Coverage — Need Measurable Targets

**Current PRD wording:** "Tests cover services, APIs, workers, adapters, UI and E2E flows."

**Gap identified:** No measurable coverage thresholds or test pyramid distribution.

**Proposed clarification:**
- Unit: ≥80% coverage for services, repositories, adapters
- Integration: ≥70% coverage for API routes, worker flows
- Contract: 100% for frozen API schemas
- E2E: Critical user journeys (upload → clip → publish)
- Visual: Clip Studio timeline, caption rendering, crop modes
- Accessibility: WCAG 2.1 AA for all user-facing screens

---

## 3. Deferred Requirements (Post-MVP)

Per PRD Section 8 MVP scope and Section 10 open decisions, the following are explicitly deferred:

| Requirement | Deferral Reason | Target |
|---|---|---|
| Live stream ingestion | OUT-004 | Post-MVP module |
| Automatic trend discovery | PRD Section 8 | Post-MVP |
| Multi-tenant billing | PRD Section 8 | Post-MVP |
| AI B-roll generation | OUT-005 | Post-MVP |
| Advanced dynamic effects | PRD Section 8 | Post-MVP |
| Square (1:1) output | FR-020 optional | Post-MVP |
| Twitch/Kick import adapters | PRD Section 4 | Post-MVP |
| YouTube import (authorized only) | PRD Section 4 | Post-MVP |

---

## 4. Rejected Requirements (None)

No requirements from PRD v0.1 are rejected. All 38 FR, 10 NFR, 7 BR are confirmed.

---

## 5. User Personas & Workflows (From PRD Section 2-3)

### Primary Personas

| Persona | Primary Workflow | Key Requirements |
|---|---|---|
| Solo creator / podcaster | Upload → Transcribe → Discover → Edit → Publish | FR-001, FR-011, FR-014, FR-026, FR-033 |
| Educator / technical creator | Upload → Transcribe → Preserve technical context → Edit → Publish | FR-011, FR-012, Profile 5.2, FR-021 |
| Gaming creator | Upload → Event-triggered sampling → Facecam + gameplay → Edit → Publish | FR-013, Profile 5.3, FR-022 |
| Entertainment creator | Upload → Preserve punchline structure → Expressive captions → Publish | Profile 5.4, FR-021 |
| Small creator team | Multi-brand workspace → Shared library → Approval policies → Analytics | FR-052, FR-034, FR-040 |

### Critical User Journeys (Must Have Acceptance Criteria)

1. **J-001: Upload to First Clip** — File upload → processing → candidate review → edit → render → publish
2. **J-002: Profile-Specific Discovery** — Select profile → get candidates → verify profile-appropriate boundaries
3. **J-003: Human-in-the-Loop Edit** — AI suggests edit → preview → approve/modify/reject → versioned draft
4. **J-004: Policy-Gated Publishing** — Configure policy → candidate approved → auto-publish or manual approval
5. **J-005: Failure Recovery** — Worker fails → job resumes from last completed stage → no data loss

---

## 6. Open Decisions Requiring Product-Owner Resolution

### OUT-001: Deployment Model
- **Options:** Single-user self-hosted MVP vs Multi-user SaaS from day one
- **Impact:** Architecture (D-003 single persistence layer), auth, multi-tenancy, billing
- **Decision needed before:** Contract freeze, scaffold, slice planning

### OUT-002: Import Connectors for MVP
- **Options:** Local file upload only vs Local + Azure Blob vs Local + Azure + Watched folders
- **Impact:** FR-004 scope, storage abstraction complexity, MVP timeline
- **Decision needed before:** Ingestion slice implementation

### OUT-003: First Release Publishing Channels
- **Options:** YouTube only vs Meta (Instagram/Facebook) only vs Both
- **Impact:** OAuth implementation, API contracts, publishing slice scope
- **Decision needed before:** Publishing slice implementation

### OUT-004: Live-Stream Monitor in v1
- **Options:** Include in v1 vs Post-MVP
- **Impact:** Real-time ingestion architecture, scheduling, resource allocation
- **Decision needed before:** Architecture finalization

### OUT-005: Audio Dubbing & B-Roll in v1
- **Options:** Include in v1 vs Post-MVP
- **Impact:** FR-024 scope, rendering pipeline complexity, rights metadata
- **Decision needed before:** Rendering slice implementation

---

## 7. Assumptions Documented

| Assumption | Source | Validation Needed |
|---|---|---|
| AMD Vega 8 (2GB VRAM) cannot run local LLMs for candidate generation | Discovery hardware | Test Ollama/Qwen on target hardware |
| Cloud providers (NVIDIA API, Gemini, OpenAI, Anthropic, Groq) meet latency/cost targets | PRD FR-050 | Benchmark representative workloads |
| PostgreSQL + Redis + Celery on 6GB RAM is viable | Architecture PRD | Load test with concurrent jobs |
| FFmpeg/FFprobe/OpenCV/PySceneDetect available in container | Architecture PRD | Verify Docker image size/startup |
| Official Meta/YouTube APIs provide needed permissions | PRD FR-032/033 | Verify OAuth scopes and rate limits |

---

## 8. Acceptance Criteria Gaps

### From PRD Acceptance Criteria (docs/17-ACCEPTANCE-CRITERIA.md) vs Session DB (24 ACs)

**Missing ACs that need definition:**

| Area | Missing Criteria |
|---|---|
| Ingestion | Rights declaration UI flow, upload progress/resume UI |
| Processing | Scene detection accuracy threshold, diarization quality bar |
| Rendering | Caption safe-margin compliance, crop mode correctness |
| Editor | Keyboard accessibility for all timeline operations |
| Publishing | OAuth token refresh handling, rate limit behavior |
| Analytics | Metric freshness SLA, attribution window definition |
| Operations | Cost alert thresholds, worker autoscaling triggers |

---

## 9. Conflicts Identified

### Conflict 1: FR-024 (B-roll fail-soft) vs FR-003 (Rights declaration)
- **Issue:** B-roll requires separate source/rights metadata; fail-soft means core render succeeds without B-roll
- **Resolution:** B-roll metadata optional in candidate; render pipeline validates if present, proceeds without if absent
- **Status:** Resolved in design — B-roll track is optional in Clip Studio (FR-026)

### Conflict 2: NFR-002 (PostgreSQL authoritative) vs NFR-005 (Media outside DB)
- **Issue:** Workflow state in PostgreSQL, media in object storage — need consistent references
- **Resolution:** Media records in PostgreSQL store storage keys/URLs, not blobs; foreign keys to source_video table
- **Status:** Confirmed — data model (docs/03-DATA-MODEL.md) supports this

### Conflict 3: CON-007 (No NVIDIA GPU) vs FR-050 (Provider configuration includes NVIDIA)
- **Issue:** NVIDIA API Catalog and NIM are cloud services, not local GPU — no conflict
- **Resolution:** Clarified in provider-capability-routing skill — NVIDIA adapters are cloud HTTP clients
- **Status:** Resolved — CON-007 only constrains local inference

---

## 10. Traceability Matrix (Partial)

| Requirement | PRD Source | Acceptance Criteria | Test Level | Design Ref | Status |
|---|---|---|---|---|---|
| FR-001 | FR-001 | AC-FR-001 | integration | — | confirmed |
| FR-011 | FR-011 | AC-FR-011 | integration | — | confirmed |
| FR-014 | FR-014 | AC-FR-014 | integration | — | confirmed |
| FR-025 | FR-025 | AC-FR-025 | e2e | D-005 | confirmed |
| FR-026 | FR-026 | AC-FR-026 | visual | — | confirmed |
| FR-027 | FR-027 | AC-FR-027 | e2e | — | confirmed |
| FR-033 | FR-033 | AC-FR-033 | integration | — | confirmed |
| NFR-001 | NFR-001 | AC-NFR-001 | integration | — | confirmed |
| NFR-002 | NFR-002 | AC-NFR-002 | integration | D-003 | confirmed |
| NFR-003 | NFR-003 | AC-NFR-003 | integration | — | confirmed |
| CON-007 | Discovery | AC-CON-007 | unit | — | confirmed |

---

## 11. Recommendations

### Immediate (Before Next Phase)
1. **Resolve OUT-001 to OUT-003** — deployment model, import connectors, publishing channels directly impact architecture and slice planning
2. **Define FR-028 operation schema** — needed for Clip Studio editor design
3. **Add measurable test targets to NFR-010** — needed for QE strategy

### During UX/Design Phases
4. **Profile-specific UI flows** — each content profile (5.1-5.4) needs tailored candidate review UI
5. **Keyboard-accessible timeline** — Clip Studio must support full keyboard editing (FR-027)
6. **Caption editor accessibility** — word-level timing editing must be screen-reader accessible

### During Architecture Phase
7. **Capability registry design** — define provider capability matrix with fallbacks
8. **Cost tracking schema** — per-job, per-provider, per-model cost accumulation
9. **Idempotency keys** — for all external side effects (upload, publish, webhook)

---

## 12. Next Steps

1. **Product owner resolves OUT-001 to OUT-005** (5 open decisions)
2. **Requirements review completion** — this document finalized
3. **Request `APPROVE REQUIREMENTS REVIEW v1`** (or specific changes)
4. **Proceed to UX Research** (prompt 02-ux-research skill) and **Information Architecture** (prompt 03-information-architecture skill)

---

**Gate Status:** `NEEDS APPROVAL` — Requires product-owner resolution of 5 open decisions (OUT-001 to OUT-005) and approval of this review before proceeding to UX/Design phases.