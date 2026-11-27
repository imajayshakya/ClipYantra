# Development Change Log

## 2026-11-28 — ING-004 Scene Detection model/repository/config/migration

- **APPROVE SLICE ING-004** and **APPROVE SLICE PROC-001** received from product owner.
- Created detailed slice plans: `docs/slices/ING-004.md` (16KB) and `docs/slices/PROC-001.md` (24KB)
- Created branch `feature/ING-004-scene-detection` from main
- Implemented Scene SQLAlchemy model with full schema:
  - Fields: id, media_asset_id, start_ms, end_ms, keyframe_asset_id, labels (JSONB), detection_job_id, created_at, updated_at
  - Indexes: media_asset_id, (media_asset_id, start_ms, end_ms), detection_job_id
  - Foreign keys: media_asset_id → media_assets.id (CASCADE), keyframe_asset_id → media_assets.id (SET NULL)
  - Relationships: MediaAsset.scenes (one-to-many), Scene.keyframe_asset (many-to-one)
- Added SceneRepository methods: create_scene, get_scene, list_scenes, update_scene_keyframe, delete_scenes_for_media_asset, get_scenes_by_detection_job
- Added Scene Detection configuration to settings: scene_default_threshold, scene_min_duration_ms, keyframe_default_format, keyframe_default_quality
- **Fixed critical Alembic migration bug**: Migration 84845e49c21c was auto-generated to drop all existing tables. Manually corrected to only CREATE scenes table with indexes.
- Recreated test database by running all migrations in order (20261123_001 → 20261123_002 → 20261126_003 → 84845e49c21c)
- Fixed pre-existing test infrastructure issue in test_source_repository.py (import conflict causing metadata collision)
- All 239 backend tests pass
- Updated PHASE-STATUS.md to reflect ING-004 IN PROGRESS
- Pushed branch to origin

## 2026-11-22 — Documentation baseline created

- Added draft product requirements, architecture, data model, API contracts, AI strategy, media pipeline, editor, publishing, analytics, security, testing, operations, SupoClip research, licensing, risks, roadmap and acceptance criteria.
- Added agent instructions and sequential Copilot prompts.
- No application code or dependencies were changed by this documentation pack.
- No design/contract/scaffold approval has been granted.

## 2026-11-22 — Requirements baseline created (post-discovery)

- **APPROVE DISCOVERY v1** received from product owner.
- Repository discovery completed: git status, branch (main), 1 commit (85e7aad), hardware inventory (AMD Ryzen 5 3500U, 6GB RAM, Vega 8 2GB VRAM — no NVIDIA GPU).
- Requirements baseline created in session database:
  - 68 requirements: 7 BR, 38 FR, 10 NFR, 8 CON, 5 OUT
  - 24 acceptance criteria (Given/When/Then format) with full traceability
- Engineering docs updated: PHASE-STATUS.md (Phase 00 COMPLETE, Phase 01 BASELINE DRAFT), DECISIONS.md (D-006 added)
- Next gate: **APPROVE REQUIREMENTS v1** required before proceeding to requirements review

## 2026-11-22 — Requirements review completed (APPROVE REQUIREMENTS v1 received)

- **APPROVE REQUIREMENTS v1** received from product owner.
- Requirements review conducted against PRD v0.1, discovery findings, and approved baseline:
  - All 68 requirements confirmed (38 FR, 10 NFR, 7 BR, 8 CON, 5 OUT)
  - 3 clarifications needed: FR-028 operation schema, FR-050 capability matrix, NFR-010 measurable test targets
  - 5 open decisions (OUT-001 to OUT-005) identified for product-owner resolution
  - 5 user personas and 5 critical user journeys documented
  - 3 conflicts identified and resolved (B-roll rights, PostgreSQL vs object storage, NVIDIA cloud vs local)
  - Traceability matrix started for requirement → AC → test level mapping
- Engineering docs updated: PHASE-STATUS.md (Phase 01 APPROVED, Phase 01a IN PROGRESS), REQUIREMENTS-REVIEW.md created
- Next gate: **Product-owner resolution of OUT-001 to OUT-005** + **APPROVE REQUIREMENTS REVIEW v1** before UX/Design phases

## 2026-11-22 — UX research completed (APPROVE REQUIREMENTS REVIEW v1 received)

- **APPROVE REQUIREMENTS REVIEW v1** received from product owner.
- UX research conducted against approved requirements, PRD v0.1, and discovery:
  - 5 personas documented as hypotheses (Solo creator, Educator, Gaming creator, Entertainment creator, Content operator)
  - 8 Jobs-to-be-Done mapped to requirements with measurable success signals
  - 13-stage end-to-end journey from workspace setup to analytics feedback
  - 8 moments of uncertainty identified with requirement mitigations
  - 10 research questions prioritized (5 high, 3 medium, 2 low)
  - 9 proposed success measures with baseline targets (require validation)
  - 3 open decisions blocking UX design: OUT-001 (deployment), OUT-002 (import connectors), OUT-003 (publishing channels)
  - Research plan: 3 phases (usability, contextual inquiry, benchmark) over 4 weeks
- Engineering docs updated: PHASE-STATUS.md (Phase 02 COMPLETE), 01-UX-RESEARCH.md updated
- Next gate: **Product-owner resolution of OUT-001, OUT-002, OUT-003** + **APPROVE UX v1** before Information Architecture and Visual Direction

## 2026-11-22 — Information Architecture completed

- Information Architecture document created (`docs/design/02-INFORMATION-ARCHITECTURE.md` v1):
  - 9 core user-facing objects with clear distinctions (Source Video, Processing Job, Transcript, Clip Candidate, Draft, Rendered Clip, Destination, Scheduled Post, Published Post, Performance Snapshot)
  - Object relationship diagram showing user mental model
  - 10 primary navigation items with route mapping (23 total routes)
  - 4 primary user flows with failure/recovery points: Import→Candidates, Studio Editing, Metadata→Schedule→Publish, Workspace/Brand Management
  - Contextual navigation patterns: breadcrumbs, persistent context bar, search/filter persistence, deep links
  - Naming conventions validated for clarity (Candidate vs Draft vs Rendered Clip vs Post)
  - Application shell layout with responsive breakpoints
  - Notifications and activity center design
  - 5 open questions requiring product owner decisions (OUT-001, OUT-002, OUT-003, RQ-4, FR-050)
  - Approval checklist and next steps defined
- Engineering docs updated: PHASE-STATUS.md (Phase 03 DRAFT), DECISIONS.md (D-009 added)
- Next gate: **Product-owner resolution of OUT-001, OUT-002, OUT-003** + **APPROVE UX v1** + **APPROVE IA v1** before Visual Direction phase

## 2026-11-22 — UX Research and Information Architecture APPROVED

- **APPROVE UX v1** received from product owner.
- **APPROVE IA v1** received from product owner.
- UX Research phase (Phase 02) and Information Architecture phase (Phase 03) are now **APPROVED**.
- Engineering docs updated: PHASE-STATUS.md (Phase 02 APPROVED, Phase 03 APPROVED, Phase 04 IN PROGRESS), DECISIONS.md (D-008, D-009 updated to APPROVED)
- Next phase: **Visual Direction** (prompt 04-brand-visual-directions) — creating 2+ differentiated brand visual directions for product owner approval
- Remaining open decisions to resolve during/after Visual Direction: OUT-001 (deployment model), OUT-002 (import connectors), OUT-003 (publishing channels), RQ-4 (tablet editing for MVP), FR-050 (provider routing granularity)

## 2026-11-22 — Visual Direction completed (awaiting approval)

- Brand Visual Direction document created/updated (`docs/design/03-BRAND-VISUAL-DIRECTION.md`):
  - **Direction A — Calm Creator Workstation** (recommended): Dark graphite editor surfaces, neutral text hierarchy, restrained indigo accent, teal/amber/red status semantics, dense editing controls, spacious management pages. Full semantic token specification (colors, typography, spacing, radius, elevation, motion, density tiers).
  - **Direction B — Editorial Light Studio**: Warm off-white canvas, deep ink typography, deep violet/blue accent, generous whitespace, editorial typography. Dual-surface challenge for Clip Studio (light UI + dark preview zone). Full token specification.
  - **Direction C — Broadcast Control Room** (conditional): High-density dark interface for live monitoring; only if OUT-004 validates live-operations mode.
  - All 5 required screens specified for A & B: Overview Dashboard, Video Library/List, Clip Studio (Preview+Timeline+Inspector), Publishing Calendar, AI Provider Settings.
  - Side-by-side comparison table, accessibility requirements, trade-offs analysis, logo concept prompts.
  - Recommendation: Direction A primary with Direction B parallel for management screens.
- Engineering docs updated: PHASE-STATUS.md (Phase 04 IN PROGRESS with detailed evidence), DECISIONS.md (no new decisions — visual direction exploration phase)
- Next gate: **Side-by-side compositions + accessibility audit** → **Product owner review** → **`APPROVE VISUAL DIRECTION v1`**
- Blockers: OUT-001, OUT-002, OUT-003 remain open but do not block visual direction exploration

## 2026-11-22 — Product Owner Decision v1 + Visual Direction APPROVED

- **Product Owner Decision v1** received — resolves 5 open decisions:
  - **OUT-001 (Deployment)**: Self-hosted MVP, Docker-based, single owner/workspace, secure app auth, no billing, SaaS-ready architecture, local GPU + cloud AI providers supported.
  - **OUT-002 (Import Connectors)**: All four source types — Local uploads, Azure Blob, Watched folders, Authorized platform imports. Priority: Local + URLs first; Azure + watched folders second; platform integrations third. No DRM bypass.
  - **OUT-003 (Publishing Channels)**: Both platform families in MVP — Instagram Reels, Facebook Reels (Meta), YouTube Shorts. Official APIs, separate adapters, OAuth + capability validation.
  - **RQ-4 (Tablet Editing)**: Desktop-first MVP. Tablet supports Dashboard, Video preview, Clip review, Approve/Reject, Calendar, Analytics. Full timeline editing desktop-only for now.
  - **FR-050 (Provider Routing)**: Hierarchical — Workspace default → Content-profile overrides → Per-job manual overrides. Modes: Local-first, Balanced, Cloud-first, User-selected. Per-brand deferred. 8 providers in capability architecture (NVIDIA Nemotron, NVIDIA NIM, Gemini, OpenAI, Claude, Groq, Deepgram, Ollama).
- **APPROVE VISUAL DIRECTION v1** received from product owner.
- Information Architecture updated: OUT-001, OUT-002, OUT-003, RQ-4, FR-050 marked RESOLVED with decisions documented; OUT-004, OUT-005 remain unresolved.
- Requirements baseline updated: OUT-001, OUT-002, OUT-003 status changed to 'resolved'; FR-050 description expanded with hierarchical routing details.
- Engineering docs updated: PHASE-STATUS.md (Phase 04 APPROVED, Product Owner Decisions RESOLVED), DECISIONS.md (D-010 added), CHANGELOG-DEV.md (this entry).
- **Next gate**: **Wireframes** (prompt 05-screen-wireframes) and **Design System** (prompt 06-design-system) with approved tokens. Remaining open: OUT-004 (live-stream monitor), OUT-005 (AI dubbing/B-roll).

## 2026-11-23 — Phase 05 wireframe baseline created

- Expanded `docs/design/05-SCREEN-SPECIFICATIONS.md` from a screen checklist into route-level low-fidelity specifications for the shared shell and core screen families.
- Covered Overview, Library, Source Detail, Import, Processing, Candidates, Clip Studio, Exports, Calendar, Accounts, Published/Analytics, Brand Kit, AI/Processing Settings, and Workspace/Audit/Policies.
- Added RQ-4 tablet behavior for Dashboard, preview, clip review, approve/reject, calendar and analytics.
- Made the desktop-only boundary explicit for full multi-track timeline editing.
- Added state, navigation, action, responsive, accessibility and requirements traceability sections.
- Corrected design overview and design decision register status consistency for the existing `APPROVE VISUAL DIRECTION v1` approval.
- No application implementation code, contracts or frontend files were changed.
- Gate remains pending: `APPROVE WIREFRAMES v1`.

## 2026-11-23 — Wireframes approved; Design System phase started

- **APPROVE WIREFRAMES v1** received.
- Wireframe document status changed to APPROVED v1 and engineering phase status updated.
- D-011 recorded the approved low-fidelity screen baseline.
- Phase 06 Design System initiated with existing dependencies and repository structure reviewed.
- No frontend, application, package or dependency files were changed.

## 2026-11-23 — Design System approved; Interaction/Responsive/Accessibility phase started

- **APPROVE DESIGN SYSTEM v1** received.
- Design-system document status changed to APPROVED v1 and D-012 recorded.
- Phase 07 initiated for interaction/state, accessibility and responsive behavior specifications.
- No frontend, application, package or dependency files were changed.

## 2026-11-23 — Architecture and risk baseline updated

- Phase 08 started with a proposed architecture update for Product Owner Decision v1:
  - self-hosted Docker MVP and SaaS-ready boundaries;
  - local uploads/direct URLs, Azure Blob, watched folders and authorized platforms;
  - Instagram/Facebook Reels and YouTube Shorts through separate official adapters;
  - hierarchical workspace/profile/job provider routing;
  - desktop-first Clip Studio and RQ-4 tablet boundaries.
- Updated provider, deployment, API and data-model proposals for the resolved decisions.
- Consolidated the engineering risk register and expanded measured-fact/assumption/prediction evidence in the risk report.
- Added proposed ADR-001 through ADR-010 entries to the architecture draft.
- No architecture or risk decision is marked approved until explicit owner action.
- No application implementation, package or dependency files were changed.

## 2026-11-23 — Architecture approved; full design approval audit started

- **APPROVE ARCHITECTURE v1** received.
- `docs/02-ARCHITECTURE.md` changed to APPROVED v1 and D-013 through D-020 recorded as approved architecture decisions.
- Phase 08 architecture status changed to APPROVED; operational risk baselines remain unapproved evidence artifacts.
- Phase 09 full-design approval audit initiated.
- PRD status aligned to requirements approval and resolved/deferred Product Owner decisions.
- No application implementation, package or dependency files were changed.

## 2026-11-23 — Full Design approved; Contract Freeze started

- **APPROVE DESIGN v1** received.
- Full design package status changed to APPROVED v1.
- D-005, D-006 and D-007 recorded as approved by the explicit full-design token.
- Phase 09 completed and Phase 10 Contract Freeze initiated.
- No application implementation, migration or dependency files are changed during contract freeze.

## 2026-11-23 — Contract freeze baseline drafted

- Cross-layer contract freeze draft added at `docs/contracts/CONTRACT-FREEZE.md`.
- Data-model and API-contract documents moved to CONTRACT FREEZE DRAFT status.
- Defined migration order, Pydantic example shapes, API/error/SSE contracts, state machines, edit operations, source maps and storage keys.
- Defined idempotency, outbox, lease and reconciliation semantics.
- Linked key requirements to architecture and contract sections in the live traceability matrix.
- Contract test plan added for schema, migration, API, SSE, state, side effects and source maps.
- No migrations, Pydantic implementation, API routes, workers or application code were changed.

## 2026-11-23 — Contracts approved; Placeholder Scaffold gate blocked

- **APPROVE CONTRACTS v1** received.
- Contract freeze baseline changed to APPROVED v1.
- Data model and API contract documents changed to FROZEN v1.
- D-021 recorded the approved contract baseline.
- Phase 10 changed to APPROVED.
- Placeholder scaffold remains NOT STARTED because **APPROVE SCAFFOLD v1** was not provided.
- No scaffold folders, migrations, dependencies or application files were created.

## 2026-11-23 — Placeholder Scaffold authorized

- **APPROVE SCAFFOLD v1** received.
- Placeholder-only backend, frontend folder and infrastructure skeleton work initiated.
- No package dependencies, migrations, provider calls, social API calls, media processing or business logic may be added in this phase.

## 2026-11-23 — Placeholder Scaffold completed

- Backend placeholder folders, typed settings, disabled health/domain/port/adapter/worker interfaces and migration/test READMEs created.
- Frontend placeholder folders and scope READMEs created; no package manifest or UI implementation added.
- Placeholder Docker Compose, environment and disabled CI skeleton added.
- Python placeholder package passed `python -m compileall -q backend/app`.
- No package manifests, migrations, external service calls or business behavior were detected.
- Phase 11 is complete; vertical-slice implementation remains blocked until an explicit `APPROVE SLICE <ID>` token.

## 2026-11-23 — FOUND-001 implementation completed for independent review

- **APPROVE SLICE FOUND-001** received.
- Added FOUND-001 slice specification and acceptance/test IDs.
- Added a backend dependency manifest for FastAPI, Pydantic settings, SQLAlchemy, psycopg and pytest.
- Replaced placeholder config, health and database probe modules.
- Implemented liveness and readiness endpoints and explicit not-configured component states.
- Focused red run: 3 collection errors before implementation.
- Focused green run: 16 tests passed.
- Independent review found URL normalization, timeout, `.env` ignore and traceability gaps; review fixes were applied and verified.
- DEF-FOUND-001 was extended to cover non-numeric, out-of-range, whitespace and extremely long ports; red/green regression coverage was added.
- Final independent verification resolved DEF-FOUND-001 and kept AC-FND-002 BLOCKED because no live PostgreSQL runtime was available.
- Independent review also found scheme-valid malformed PostgreSQL URL handling; DEF-FOUND-001 was fixed and a red/green regression test was added.
- Live app check: liveness HTTP 200, readiness HTTP 503 with database/Redis/storage/worker `not_configured`.
- Live PostgreSQL `SELECT 1` was not run because PostgreSQL/Docker runtime is unavailable.
- At that pre-acceptance checkpoint, independent verification and `ACCEPT SLICE FOUND-001` were still pending.

## 2026-11-23 — FOUND-001 ACCEPTED

- **ACCEPT SLICE FOUND-001** received.
- FOUND-001 status changed to ACCEPTED v1.
- 16 focused tests, compile check and HTTP liveness/readiness smoke evidence are recorded.
- DEF-FOUND-001 is resolved.
- The owner explicitly waived live PostgreSQL runtime evidence for AC-FND-002.
- No next slice is authorized until a separate `APPROVE SLICE <ID>` token is provided.

## 2026-11-23 — ING-001 implementation completed for independent review

- **APPROVE SLICE ING-001** is recorded.
- Added SQLAlchemy source, source-rights and upload-session entities.
- Added `POST /api/v1/sources/uploads`, `GET /api/v1/sources` and `GET /api/v1/sources/{source_id}` routes.
- Added idempotency conflict and unknown-blocked rights behavior.
- Added Alembic ING-001 migration and synthetic SQLite upgrade/downgrade test.
- Repository/API/migration suite: 13 ING-001 tests passed.
- Complete backend suite: 29 tests passed.
- Live PostgreSQL migration and live HTTP integration remain not run.
- Independent review and `ACCEPT SLICE ING-001` remain pending.
