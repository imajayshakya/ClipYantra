# Information Architecture and Navigation

**Status:** **APPROVED** — **APPROVE IA v1** ✓  
**Version:** v1 (updated with Product Owner Decision v1)  
**Date:** 2026-11-22  
**Prerequisites:** **APPROVE UX v1** ✓, **APPROVE IA v1** ✓  
**Dependencies:** OUT-001, OUT-002, OUT-003, RQ-4, FR-050 **RESOLVED** (Product Owner Decision v1); OUT-004, OUT-005 pending

---

## 1. Core Object Model (User-Facing)

These are the objects users work with, distinct from backend entities. Each has a clear user-visible identity and lifecycle.

| Object | User-Facing Name | Description | Key Attributes |
|--------|------------------|-------------|----------------|
| **Source Video** | Source Video | The original long-form video imported with rights declared | title, duration, resolution, rights_declaration, provenance, storage_path, status, created_at |
| **Processing Job** | Processing Job | An async run that extracts audio, transcribes, detects scenes, generates candidates | profile, stages[], progress, status, error, cost_estimate, provider_routing |
| **Transcript** | Transcript | Timestamped segments with word alignment and optional speaker labels | language, segments[], speakers[], confidence, word_aligned |
| **Clip Candidate** | Clip Candidate | An AI-proposed self-contained segment with evidence and rationale | start, end, transcript_excerpt, category, score, rationale, rank |
| **Draft** | Draft | A user-editable version of a candidate with timeline edits | version, parent_candidate, operations[], timeline_state, autosaved_at |
| **Rendered Asset** | Rendered Clip | A finalized export ready for publishing (immutable) | format, aspect_ratio, resolution, codecs, storage_path, validation_status |
| **Publish Target** | Destination | A connected social account (YouTube channel, Instagram/FB page) | platform, account_id, account_name, oauth_status, policy |
| **Scheduled Post** | Scheduled Post | A render + metadata + destination + time, awaiting publish | render_id, destination_id, title, caption, hashtags, scheduled_at, policy |
| **Published Post** | Published Post | A post that has been sent to platform API with external ID | external_id, platform, published_at, status, reconciliation_state |
| **Analytics Snapshot** | Performance Snapshot | Timestamped platform metrics associated to a post | view_count, like_count, comment_count, share_count, captured_at |

---

## 2. Object Relationships (User Mental Model)

```
Source Video
  └─► Processing Job(s)
        └─► Transcript
        └─► Clip Candidate(s)
              └─► Draft Version(s)
                    └─► Rendered Asset(s) (format variants)
                          └─► Scheduled Post(s) per Destination
                                └─► Published Post
                                      └─► Analytics Snapshot(s)
```

**Key Distinctions for Users:**
- **Candidate** = AI proposal (immutable, ranked, with rationale)
- **Draft** = User's working copy (versioned, editable, autosaved)
- **Rendered Clip** = Finalized export (validated, immutable, publishable)
- **Scheduled Post** = Intent to publish (editable until publish time)
- **Published Post** = Platform-confirmed (external ID recorded, auditable)

---

## 3. Navigation Hierarchy (Validated Against Requirements)

### Primary Navigation (Top-Level)

| Nav Item | Route | Purpose | Key Requirements |
|----------|-------|---------|------------------|
| **Overview** | `/` | Workspace dashboard: active jobs, recent clips, quick actions | FR-051, FR-052, BR-007 |
| **Library** | `/library` | Browse all source videos with status, filters, search | FR-001, FR-002, FR-003, FR-005 |
| **Candidates** | `/candidates` | Review AI-generated clip candidates across all sources | FR-014, FR-015, FR-016, FR-017, FR-018 |
| **Studio** | `/studio/[draftId]` | Clip Studio: multi-track editor for a specific draft | FR-025, FR-026, FR-027, FR-028 |
| **Exports** | `/exports` | Rendered assets ready for publishing, with validation status | FR-020, FR-021, FR-022, FR-023, NFR-007 |
| **Calendar** | `/calendar` | Schedule view: planned, queued, published posts | FR-034, FR-035, FR-036 |
| **Published** | `/published` | Published posts with platform status and analytics | FR-035, FR-040, FR-041, FR-042 |
| **Connections** | `/connections` | OAuth accounts, connection health, publishing policies | FR-032, FR-033, FR-034 |
| **Brand Kit** | `/brand` | Caption templates, brand colors, overlays, CTA presets | FR-021, FR-030 |
| **Settings** | `/settings` | Workspace, AI providers, processing, storage, members | FR-050, FR-051, FR-052, FR-053 |

### Secondary Navigation (Contextual)

| Context | Navigation Elements |
|---------|---------------------|
| **Source Video Detail** | Tabs: Overview · Transcript · Candidates · Jobs · Exports · Posts |
| **Processing Job Detail** | Stages: Upload → Audio → Transcript → Scenes → Candidates · Logs · Retry |
| **Clip Studio** | Header: Source → Candidate → Draft v3 · Preview · Timeline · Inspector |
| **Calendar** | Views: Month · Week · Day · List · Filters: Destination · Status · Category |

---

## 4. Page Map and URL Structure

```
ClipYantra (Workspace)
├── /                                    # Overview/Dashboard
├── /library                             # Source Video Library
│   ├── /library/[sourceId]              # Source Video Detail
│   │   ├── /library/[sourceId]/transcript
│   │   ├── /library/[sourceId]/candidates
│   │   ├── /library/[sourceId]/jobs
│   │   ├── /library/[sourceId]/exports
│   │   └── /library/[sourceId]/posts
│   └── /library/import                  # Import flow (modal or page)
├── /candidates                          # All Candidates (cross-source)
│   └── /candidates/[candidateId]        # Candidate Detail → opens Studio
├── /studio                              # Clip Studio entry
│   ├── /studio/new                      # New draft from candidate (redirect)
│   └── /studio/[draftId]                # Editor (persistent route)
├── /exports                             # Rendered Assets
│   ├── /exports/[renderId]              # Render Detail → metadata, validation
│   └── /exports/[renderId]/publish      # Publish flow
├── /calendar                            # Schedule Calendar
│   ├── /calendar/[scheduledPostId]      # Scheduled Post Detail
│   └── /calendar/queue                  # Pending publishes
├── /published                           # Published Posts
│   └── /published/[postId]              # Post Detail + Analytics
├── /connections                         # Social Accounts
│   ├── /connections/youtube             # YouTube OAuth + channels
│   └── /connections/meta                # Meta OAuth + pages
├── /brand                               # Brand Kit
│   ├── /brand/templates                 # Caption templates
│   ├── /brand/overlays                  # Overlay assets
│   └── /brand/presets                   # CTA/hashtag presets
└── /settings                            # Settings
    ├── /settings/workspace              # Workspace, members, brands
    ├── /settings/ai-providers           # Providers, models, routing, costs
    ├── /settings/processing             # Profiles, policies, hardware
    ├── /settings/storage                # Local/Azure config
    └── /settings/audit                  # Audit log (FR-053)
```

---

## 5. Primary User Flows

### Flow 1: Import → Candidates (Core Discovery)
```
User Action                              System Response
─────────────────────────────────────────────────────────────────────
1. Click "Import Video"                  → Import modal/page
2. Select file / cloud URL / watched     → Validate (FR-002)
3. Declare rights (owned/authorized)     → Record rights (FR-003, CON-001)
4. Choose content profile                → Show profile options (FR-014)
5. Set AI routing / cost limit           → Show provider config (FR-050)
6. Start Processing                      → Create job, show progress (NFR-001, NFR-006)
7. View job stages in real-time          → SSE progress (FR-051)
8. Job completes → Navigate to Candidates → Show ranked candidates (FR-014, FR-016)
9. Review candidate cards                → See evidence, rationale, boundaries
10. Click "Edit in Studio"               → Create draft, open Studio (FR-025)
```

**Failure/Recovery Points:**
- Upload interrupted → Resume (FR-005)
- Job fails at stage N → Retry from stage N (NFR-001, AC-NFR-001)
- No candidates → Show "Adjust profile or try different provider" (FR-017)
- Rights unclear → Block processing until resolved (FR-003)

### Flow 2: Clip Studio Editing (Core Creation)
```
User Action                              System Response
─────────────────────────────────────────────────────────────────────
1. Open Candidate in Studio              → Load draft v1 (immutable candidate)
2. Preview video + transcript sync       → Playhead follows transcript (FR-026)
3. Trim boundaries (drag/keyboard)       → New draft v2, autosave (FR-025, FR-027)
4. Edit captions (inline)                → Word-level timing preserved (FR-021, FR-027)
5. Adjust crop (face-aware + manual)     → Preview updates real-time (FR-022)
6. Add B-roll / overlay                  → New track, versioned (FR-024, FR-026)
7. AI suggests edit (natural language)   → Typed ops preview + validate (FR-028)
8. Approve AI suggestion                 → Apply as new version (BR-003)
9. Run validation                        → Check aspect, codecs, loudness (NFR-007)
10. Click "Export"                       → Queue render job (FR-020)
```

**Key States:**
- Dirty draft (unsaved changes) → Warn on navigate
- Validation errors → Inline, blocking export
- Version history → Accessible via sidebar

### Flow 3: Metadata → Schedule → Publish (Core Distribution)
```
User Action                              System Response
─────────────────────────────────────────────────────────────────────
1. Open Render Detail                    → Show validated asset (NFR-007)
2. Click "Prepare Publish"               → Metadata editor per platform
3. Edit title/caption/hashtags/CTA       → Platform char counts (FR-030, FR-031)
4. Select Destination(s)                 → Show connected accounts (FR-032)
5. Choose: Publish Now / Schedule / Auto-policy  → Policy preview (FR-034)
6. Confirm → Creates Scheduled Post      → Visible in Calendar (FR-035)
7. At scheduled time → Worker publishes  → Official API call (FR-033)
8. Record external_id + status           → Reconcile if uncertain (FR-035, FR-036)
9. Post appears in Published             → Link to platform post
10. Analytics snapshots collected        → Associated to source/candidate (FR-040, FR-041)
```

**Policy Variations (FR-034):**
- **Manual**: User clicks "Publish Now" per post
- **Scheduled**: User sets date/time per post
- **Auto (opt-in)**: Per channel/category, posts publish when render completes
- **Hybrid**: Auto for some categories, manual for others

### Flow 4: Workspace & Brand Management (Operations)
```
User Action                              System Response
─────────────────────────────────────────────────────────────────────
1. Open Settings → Workspace             → Show members, roles, brands (FR-052)
2. Invite member → Assign role           → Role: Owner / Editor / Viewer
3. Create Brand Profile                  → Name, default profile, templates
4. Switch Brand (header)                 → Filters library, templates, policies
5. Settings → AI Providers               → Add keys, test, set defaults (FR-050)
6. Settings → Processing                 → Cost limits, hardware, profiles
7. Settings → Storage                    → Local path / Azure config (FR-004)
8. Settings → Audit                      → Filterable history (FR-053)
```

---

## 6. Contextual Navigation Patterns

### Breadcrumbs (Always Visible on Deep Pages)

| Page | Breadcrumb |
|------|------------|
| `/library/[sourceId]` | Home / Library / "Video Title" |
| `/library/[sourceId]/candidates` | Home / Library / "Video Title" / Candidates |
| `/studio/[draftId]` | Home / Studio / "Candidate Title" / Draft v3 |
| `/exports/[renderId]` | Home / Exports / "Clip Title" / Render 9:16 |
| `/calendar/[scheduledPostId]` | Home / Calendar / "Post Title" |
| `/published/[postId]` | Home / Published / "Post Title" |

### Persistent Context Bar (Top of Studio, Library Detail, Calendar)

```
┌─────────────────────────────────────────────────────────────────┐
│ [← Back]  Source: "Podcast Ep 42"  •  Profile: Podcast  •  Job: Completed  │
└─────────────────────────────────────────────────────────────────┘
```
- Shows current source, profile, processing status
- Links back to source detail
- In Studio: shows Candidate → Draft version

### Search and Filter Persistence

| Context | Persisted State |
|---------|-----------------|
| Library list | Search query, status filter, date range, sort |
| Candidates list | Profile filter, min score, date range, sort |
| Calendar | Date range, destination filter, status filter |
| Published | Platform filter, date range, source filter |
| Settings tabs | Active tab per section |

State survives navigation within section; resets on logout or explicit clear.

### Deep Links (Shareable, Bookmarkable)

| Deep Link | Opens |
|-----------|-------|
| `/library/[sourceId]` | Source detail with last active tab |
| `/studio/[draftId]` | Studio with that draft loaded |
| `/exports/[renderId]` | Render detail with metadata |
| `/calendar/[scheduledPostId]` | Scheduled post in calendar context |
| `/published/[postId]` | Published post with analytics |

---

## 7. Naming Conventions (Validated for Clarity)

| Internal Term | User-Facing Label | Rationale |
|---------------|-------------------|-----------|
| `source_video` | **Source Video** | Clear, matches "video file" mental model |
| `processing_job` | **Processing Job** | "Job" implies async, trackable work |
| `clip_candidate` | **Clip Candidate** | "Candidate" = proposal, not final |
| `draft` | **Draft** | Standard term for work-in-progress |
| `rendered_asset` | **Rendered Clip** | "Clip" = short-form output; "Rendered" = processed |
| `publish_target` | **Destination** | Where it goes (YouTube channel, IG account) |
| `scheduled_post` | **Scheduled Post** | Intent + time, not yet live |
| `published_post` | **Published Post** | Confirmed on platform |
| `analytics_snapshot` | **Performance Snapshot** | Point-in-time metrics |

**Test:** Can a creator predict what happens next?
- "Edit Candidate" → Opens Studio with new Draft ✓
- "Export Draft" → Creates Rendered Clip ✓
- "Schedule Rendered Clip" → Creates Scheduled Post ✓
- "Publish Scheduled Post" → Becomes Published Post ✓

---

## 8. Application Shell Layout

```
┌────────────────────────────────────────────────────────────────────┐
│ [Logo]  ClipYantra          [Workspace ▼]  [Brand ▼]  [User ▼]     │
├──────────────────┬────────────────────────────────────────────────┤
│                  │                                                │
│  PRIMARY NAV     │  MAIN CONTENT                                  │
│                  │                                                │
│  ▸ Overview      │  [Page Title]        [Contextual Actions]      │
│  ▸ Library       │  [Breadcrumbs]                                 │
│  ▸ Candidates    │  ────────────────────────────────────────────  │
│  ▸ Studio        │  Page Content                                  │
│  ▸ Exports       │                                                │
│  ▸ Calendar      │                                                │
│  ▸ Published     │                                                │
│  ▸ Connections   │                                                │
│  ▸ Brand Kit     │                                                │
│  ▸ Settings      │                                                │
│                  │                                                │
│  [Notifications] │                                                │
│  [Activity]      │                                                │
│                  │                                                │
└──────────────────┴────────────────────────────────────────────────┘
```

**Responsive Behavior:**
- Desktop (≥1024px): Persistent sidebar
- Tablet (768-1023px): Collapsible sidebar (hamburger)
- Mobile (<768px): Bottom nav bar (Overview, Library, Studio, Calendar, Menu)

---

## 9. Notifications and Activity Center

| Trigger | Channel | Action |
|---------|---------|--------|
| Job completed | In-app + optional email | "Processing complete — 8 candidates ready" |
| Job failed | In-app + toast | "Transcription failed — click to retry" |
| Render ready | In-app | "Export complete — review and publish" |
| Publish succeeded | In-app | "Posted to YouTube Shorts" |
| Publish failed | In-app + toast | "Publish failed — view details to reconcile" |
| Policy violation | In-app | "Auto-publish blocked: rights not declared" |
| Cost limit approached | In-app | "80% of daily AI budget used" |

**Activity Feed** (sidebar panel): Chronological, filterable by type, links to relevant object.

---

## 10. Open Questions Requiring Product Owner Decisions

| Question | Blocked IA Element | Options | **Decision (Product Owner Decision v1)** |
|----------|-------------------|---------|------------------------------------------|
| **OUT-001**: Deployment model (self-hosted vs SaaS) | Auth flow, workspace switching, onboarding, Settings structure | Self-hosted: local auth, no billing; SaaS: OAuth providers, subscription, multi-tenant | **RESOLVED** — Self-hosted MVP. Docker-based deployment, initially single owner/workspace, secure app authentication, no billing/subscription module. Keep architecture SaaS-ready for future multi-tenant support. Support local GPU processing and remote/cloud AI providers. |
| **OUT-002**: Import connectors | Library → Import flow, source types, progress UX | Local upload only / + Azure Blob / + Watched folders / + Platform imports | **RESOLVED** — All four source types: 1) Local video uploads, 2) Azure Blob Storage imports, 3) Watched-folder ingestion, 4) Authorized platform imports. Priority: Local uploads + direct authorized URLs first; Azure Blob + watched folders second; platform integrations third. Never bypass platform restrictions. |
| **OUT-003**: Publishing channels | Connections, Destinations, Metadata fields, Calendar | YouTube only / Meta only / Both (MVP) | **RESOLVED** — Both platform families in MVP: Instagram Reels, Facebook Reels (via Meta integration), YouTube Shorts. Official APIs, separate publishing adapters, OAuth + capability validation. |
| **OUT-004**: Live-stream monitor | Separate nav item, real-time ingest, clipping UX | Separate "Live" section / Integrated in Library / Post-MVP | **UNRESOLVED** — Still pending product owner decision. |
| **OUT-005**: AI dubbing & B-roll | Clip Studio tracks, provider capabilities | Separate "Enhance" tab / Integrated in Effects / Post-MVP | **UNRESOLVED** — Still pending product owner decision. |
| **RQ-4**: Tablet editing for MVP | Studio layout, responsive strategy | Desktop-only MVP / Tablet-supported MVP | **RESOLVED** — Desktop-first MVP. Tablet supports: Dashboard, Video preview, Clip review, Approve/Reject, Calendar, Analytics. Full multi-track timeline editing is desktop-first; may be introduced on tablets in future phase. |
| **FR-050**: Provider routing granularity | Settings → AI Providers page complexity | Per-workspace / Per-brand / Per-profile / Per-job | **RESOLVED** — Hierarchical routing: 1) Workspace default, 2) Content-profile overrides, 3) Per-job manual overrides. Modes: Local-first, Balanced, Cloud-first, User-selected provider. Per-brand routing deferred. Providers: NVIDIA Nemotron, NVIDIA NIM, Gemini, OpenAI, Claude, Groq, Deepgram, Ollama in capability architecture. |

---

## 11. Approval Checklist

Before `APPROVE IA v1`, confirm:

- [x] Object names (Candidate/Draft/Render/Post) are clearly differentiated
- [x] Navigation labels match creator mental models
- [x] Primary flows cover all MVP jobs-to-be-done (JTBD-1 through JTBD-8)
- [x] Failure/recovery paths are visible in IA (retry, reconcile, rights block)
- [x] Contextual navigation (breadcrumbs, context bar) supports deep work
- [x] Search/filter persistence reduces repetitive work
- [x] Deep links enable sharing and bookmarking
- [x] Responsive strategy defined for all breakpoints
- [x] OUT-001, OUT-002, OUT-003 resolved (Product Owner Decision v1)
- [ ] OUT-004, OUT-005 deferred (still pending product owner decision)

---

## 12. Next Steps After Approval

1. **Visual Direction** (prompt 04-brand-visual-directions) — Define 2+ visual directions for approval
2. **Wireframes** (prompt 05-screen-wireframes) — Low-fidelity screens for each page in page map
3. **Design System** (prompt 06-design-system) — Tokens, components, variants from approved direction
4. **Interaction/Responsive/Accessibility** (prompt 07-interaction-responsive-accessibility) — States, keyboard, motion, a11y
5. **Architecture & Risks** (prompts 08, 09) — Technical architecture, risk predictions
6. **Full Design Approval** (prompt 10) — Package all design artifacts for owner approval
7. **Contracts Freeze** (prompt 11) — Freeze API, data model, events
8. **Placeholder Scaffold** (prompt 12) — Approved folder structure, interfaces, empty routes

---

**Gate Status:** `APPROVED` — **APPROVE IA v1** ✓ received. OUT-001, OUT-002, OUT-003, RQ-4, FR-050 resolved via Product Owner Decision v1. OUT-004, OUT-005 deferred (still pending). Next phases: **Wireframes** (prompt 05-screen-wireframes) and **Design System** (prompt 06-design-system) with approved Visual Direction tokens.
