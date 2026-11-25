# Screen Specifications

**Status:** APPROVED v1 - Phase 05 wireframe specification  
**Version:** v1  
**Date:** 2026-11-23  
**Prerequisites:** `APPROVE UX v1`, `APPROVE IA v1`, `APPROVE VISUAL DIRECTION v1`  
**Approval:** `APPROVE WIREFRAMES v1`  
**Primary visual direction:** A - Calm Creator Workstation  

This document defines low-fidelity layout, content hierarchy, actions and states. It intentionally excludes final CSS, high-fidelity component styling and application implementation.

## 1. Design baseline

All wireframes inherit the approved Calm Creator Workstation direction:

- dark graphite application shell;
- preview-first Clip Studio;
- neutral surfaces with restrained indigo for active controls and primary actions;
- teal success, amber attention and red failure semantics;
- labels and icons accompany status color;
- Inter/system UI for controls and JetBrains Mono/SF Mono/Consolas for timecodes;
- management screens use spacious density;
- operational screens use compact density;
- Clip Studio uses dense editing density.

Approved source documents:

- [UX research](./01-UX-RESEARCH.md)
- [Information architecture](./02-INFORMATION-ARCHITECTURE.md)
- [Visual direction](./03-BRAND-VISUAL-DIRECTION.md)
- [Responsive strategy](./08-RESPONSIVE-STRATEGY.md)
- [Accessibility requirements](./07-ACCESSIBILITY.md)
- [Interaction and state specification](./06-INTERACTION-AND-STATES.md)

## 2. Shared application shell

The shell remains stable across authenticated management screens.

```text
+------------------------------------------------------------------------------+
| [ClipYantra]  [Workspace / Brand v]             Search  [Notifications] [User]|
+--------------+----------------------------------------------------------------+
| Overview     |  Breadcrumb / Page Header / Primary action                         |
| Library      |                                                                  |
| Candidates   |  Page content                                                     |
| Studio       |                                                                  |
| Exports      |                                                                  |
| Calendar     |                                                                  |
| Published    |                                                                  |
| Connections  |                                                                  |
| Brand        |                                                                  |
| Settings     |                                                                  |
+--------------+----------------------------------------------------------------+
```

Rules:

- the navigation label must match the IA object names;
- the workspace/brand context remains visible when switching brands;
- search is globally useful and filters may be local to the current route;
- notification and user actions must be real controls, not decorative placeholders;
- route changes preserve relevant section filters and unsaved-draft warnings;
- tablet navigation collapses to icon rail or horizontal section navigation;
- mobile uses a compact menu with the page task as the current heading.

## 3. Required page states

Every page or panel must define the following state behavior:

| State | Required behavior |
|---|---|
| Initial | One clear primary task and no fabricated records or metrics |
| Loading | Skeleton or stage-specific progress tied to a real operation |
| Empty | Explain why empty and provide the valid next action |
| Populated | Real objects, labels, timestamps and available metadata |
| Error | State what failed, whether retry is safe and the recovery action |
| Partial failure | Show successful items plus the failed/unknown subset; do not imply all work completed |
| Disabled or permission | Visible control with a reason or removed until permitted |
| Success | Confirm the completed action and provide the next relevant destination |
| Unsaved/conflict | Preserve the draft and explain save/reload/replace choices |
| Narrow viewport | Reflow or prioritize the primary task without clipping critical actions |

Loading indicators must represent measured progress or an honest indeterminate state. Empty states must not use sample analytics or simulated processing percentages.

## 4. Screen inventory

| Screen family | Route | Primary tablet behavior | Key requirements |
|---|---|---|---|
| Overview | `/` | Compact dashboard; actions and review queue | FR-051, FR-052, BR-007 |
| Library | `/library` | Search/filter cards; no dense table-only workflow | FR-001 to FR-005 |
| Source detail | `/library/[sourceId]` | Tabs + preview; detail tables reflow | FR-001 to FR-005, FR-010 to FR-018 |
| Import | `/library/import` | Step flow with large touch targets | OUT-002, FR-001 to FR-005 |
| Processing monitor | `/library/[sourceId]/jobs/[jobId]` | Stage status and retry actions | FR-051, NFR-001, NFR-006 |
| Candidate discovery | `/candidates`, `/library/[sourceId]/candidates` | Review cards and approve/reject actions | FR-014 to FR-018 |
| Clip Studio | `/studio/[draftId]` | Preview plus one inspector/panel; no desktop multi-track promise | FR-025 to FR-028 |
| Exports | `/exports`, `/exports/[renderId]` | Validation and publish preparation | FR-020 to FR-024, NFR-007 |
| Publishing calendar | `/calendar`, `/calendar/[scheduledPostId]` | Week/list views; keyboard/touch reschedule fallback | FR-034 to FR-036 |
| Social accounts | `/connections`, `/connections/youtube`, `/connections/meta` | Account cards and reconnect actions | FR-032 to FR-034 |
| Published and analytics | `/published`, `/published/[postId]` | Metric cards and linked post detail | FR-040 to FR-043 |
| Brand Kit | `/brand` | Brand/profile list and preview | FR-021, FR-030 |
| AI and processing settings | `/settings/ai-providers`, `/settings/processing`, `/settings/storage` | Sectioned provider/routing settings | FR-050, FR-051 |
| Workspace, policies and audit | `/settings/workspace`, `/settings/audit` | Readable policy and audit lists | FR-052, FR-053, FR-034 |

## 5. Overview dashboard

**Goal:** Surface work requiring attention and enable the next useful action.  
**Primary user:** Solo creator or content operator.  
**Hierarchy:** attention state, active processing, recent sources, clips ready to review, publishing calendar and available metrics.

**Layout zones**

1. Page header with `Import video` as the primary action.
2. Attention strip for failed jobs, provider degradation and items awaiting approval.
3. Active processing queue.
4. Recent sources and generated clips.
5. Upcoming scheduled posts.
6. Real analytics snapshots only where data has been refreshed.

```text
+--------------------------------------------------------------------------+
| Overview                                      [Import video]            |
+----------------------+---------------------------------------------------+
| 2 awaiting review    | Processing: 3 jobs                                   |
| 1 job needs attention| [stage: transcribing] [stage: rendering]             |
| 2 posts due          | [view details]                                      |
| Provider degraded    |                                                   |
+----------------------+---------------------------------------------------+
| Recent sources                                                       |
| [thumb] Title       Status       Candidates  Updated       [Open]      |
| [thumb] Title       Status       Candidates  Updated       [Open]      |
+--------------------------------------------------------------------------+
| Ready to review                         | Upcoming posts                  |
| [candidate cards]                       | [platform + time + clip]         |
+--------------------------------------------------------------------------+
```

**Primary actions:** Import video, resume/retry a job, review candidates.  
**Secondary actions:** Open source, open scheduled post, view all library items.

**States:** first-run, empty, active processing, partial provider failure, failed/retryable work, permission disabled and narrow viewport.

**Tablet:** two-column management cards become one-column sections; the review queue remains above recent activity; full navigation can collapse.

**Requirements:** FR-051, FR-052, BR-007.

## 6. Video Library

**Goal:** Find, filter and resume work across source videos.  
**Primary user:** Creator managing many uploads or imports.

**Layout zones**

1. Header with `Import video`.
2. Search, status, content profile, date and source filters.
3. Grid/list view control and sort.
4. Source records with thumbnail, title, duration, rights status and processing state.
5. Row/card overflow for open, reprocess, archive and delete.

**Wireframe**

```text
+--------------------------------------------------------------------------+
| Library                          [Import video]          [Grid] [List]    |
| [Search sources...] [Status v] [Profile v] [Date v] [Clear]             |
+--------------------------------------------------------------------------+
| [thumb] Source title                                                     |
| 42:18  MP4  Podcast  Completed  6 candidates  Updated 11:10       [...] |
+--------------------------------------------------------------------------+
| [thumb] Source title                                                     |
| 18:03  URL   Gaming    Processing  58% stage  Jobs 2             [...] |
+--------------------------------------------------------------------------+
```

**Primary actions:** Open source, continue processing, import.  
**Secondary actions:** Filter, sort, reprocess with profile, archive/delete after confirmation.

**States:** no sources, import in progress, source ready, processing, partial candidates, processing failed, rights blocked, permission restricted.

**Responsive:** tablet uses cards; list columns collapse progressively; mobile exposes filters in a drawer and preserves title/status/open action.

**Requirements:** FR-001 to FR-005, FR-051.

## 7. Source detail and import

### 7.1 Source detail

**Goal:** Understand one source and move to its transcript, jobs, candidates, exports or posts.  
**Primary user:** Creator reviewing or recovering processing work.

**Tabs:** Overview, Transcript, Candidates, Jobs, Exports, Posts.

```text
+--------------------------------------------------------------------------+
| <- Library / Source title                                                |
| [Preview]  Duration  Profile  Rights  Storage  Last activity              |
+--------------------------------------------------------------------------+
| Overview | Transcript | Candidates | Jobs | Exports | Posts              |
+--------------------------------------------------------------------------+
| Source summary                    | Processing summary                   |
| [thumbnail/preview]               | Completed jobs / active job          |
| [rights] [provenance]             | [retry/stop]                         |
+--------------------------------------------------------------------------+
| Recent candidates / jobs / exports                                       |
+--------------------------------------------------------------------------+
```

**States:** ready, processing, failed, rights missing, no candidates, partial stage failure and archived source.

### 7.2 Import flow

**Goal:** Safely add a source with rights and processing intent.  
**Primary user:** Solo creator or operator.

**Step order**

1. Choose source type: Local upload, Direct authorized URL, Azure Blob, Watched folder or Authorized platform.
2. Validate the selected source and show supported limits.
3. Declare ownership/authorization and provenance.
4. Select content profile.
5. Review provider routing and cost/usage boundary.
6. Start processing.

```text
+--------------------------------------------------------------------------+
| Import video                                                     [Close] |
+--------------------------------------------------------------------------+
| 1 Source | 2 Rights | 3 Profile | 4 Routing | 5 Review                  |
+--------------------------------------------------------------------------+
| [Local upload]  [Authorized URL]  [Azure Blob]                            |
| [Watched folder] [Authorized platform]                                    |
|                                                                           |
| Source preview / file information                                         |
| Rights declaration: owned / authorized / public-domain                    |
| [Continue]                                                                |
+--------------------------------------------------------------------------+
```

The import screen must:

- support direct authorized media URLs first;
- place Azure and watched-folder sources behind configuration or connectivity checks;
- identify platform imports as official/authorized flows only;
- never present public platform links as blanket download permission;
- show a clear block when rights, source access or platform terms prevent import.

**States:** idle, validating, upload paused, upload resumed, source access denied, unsupported format, rights missing, route unavailable, duplicate detected and queued.

**Requirements:** OUT-001, OUT-002, FR-001 to FR-005, FR-003, FR-050.

## 8. Processing monitor

**Goal:** Explain where a source is in processing and enable safe recovery.  
**Primary user:** Creator or operator troubleshooting a job.

**Hierarchy:** stage timeline, current event, elapsed/remaining time if measured, provider/model metadata, logs and recovery controls.

```text
+--------------------------------------------------------------------------+
| Processing: Source title                                  [Cancel]      |
+--------------------------------------------------------------------------+
| Validate | Audio | Transcript | Scenes | Candidates | Render | QA        |
| Complete | Complete | Running | Queued | Queued | Queued | Queued        |
+--------------------------------------------------------------------------+
| Current stage                                                        |
| Transcribing with Deepgram                                              |
| Real progress: 58%  Elapsed: 08:42                                     |
| [Retry stage] [Open diagnostics]                                        |
+--------------------------------------------------------------------------+
| Diagnostics disclosure                                                   |
+--------------------------------------------------------------------------+
```

**Rules:** show a percentage only when measured; otherwise use running/queued/waiting labels. Stage failures preserve completed stages. Detailed logs are secondary.

**States:** queued, running, waiting for input, retrying, succeeded, failed, cancelled and provider degraded.

**Responsive:** stage names collapse into a vertical stepper on tablet/mobile.

**Requirements:** FR-051, NFR-001, NFR-006, NFR-008.

## 9. Candidate discovery

**Goal:** Compare evidence-backed clip proposals and decide what to edit.  
**Primary user:** Creator making editorial decisions.

**Layout zones**

1. Source/profile filters and sort.
2. Ranked candidate list or grid.
3. Candidate preview and transcript excerpt.
4. Evidence: source times, category, score breakdown and rationale.
5. Actions: open Studio, accept for editing, reject and batch render.

```text
+--------------------------------------------------------------------------+
| Candidates   [Source v] [Profile v] [Score v] [Status v] [Sort v]        |
+--------------------------------------------------------------------------+
| [thumb] 00:42-01:18  Category: Hook                                   |
| Rationale: complete answer with clear payoff                            |
| Score breakdown: 82  |  Provider disagreement: none       [Open Studio] |
+--------------------------------------------------------------------------+
| [thumb] 12:10-12:48  Category: Story                                   |
| Rationale: setup and reaction remain in context                         |
| [Accept] [Reject] [Compare]                                              |
+--------------------------------------------------------------------------+
```

**Rules:** editorial score is not virality certainty; candidate boundaries must remain source-relative; compare view uses evidence not a model-only promise.

**States:** no candidates, low-confidence candidates, provider disagreement, processing, stale transcript, rejected, accepted and narrow viewport.

**Tablet:** cards use a two-column or one-column layout; accept/reject controls remain outside overflow menus.

**Requirements:** FR-014 to FR-018, NFR-007.

## 10. Clip Studio

**Goal:** Create a precise, reversible publishable edit.  
**Primary user:** Creator or editor.

**Desktop composition**

- top bar: source/candidate/draft identity, save state, undo/redo and export;
- left context 280 px: candidate notes, transcript, source and asset tabs;
- center flex: dominant 16:9 preview, safe-area/crop overlay and transport;
- right inspector 320 px: framing, captions, audio, B-roll, effects and metadata;
- bottom timeline: video, audio, captions, B-roll and effects tracks.

```text
+--------------------------------------------------------------------------+
| [<-] Podcast Ep.42 / Candidate 3 / Draft v2  [Saved] Undo Redo [Export] |
+--------------+------------------------------------------------------------+
| Transcript   |                         Preview                            |
| Candidate    |                   [16:9 / 9:16 frame]                    |
| Assets       |                     [transport controls]                  |
| Context      |  00:42.00 / 00:75.00                                    |
|              +------------------------------------------------------------+
| [Transcript segments...]       | Inspector                              |
|                                | Crop  Caption  Audio  Brand  Effects   |
|                                | [numeric controls] [platform preset]   |
+--------------+------------------------------------------------------------+
| Video  [========= clip =========][clip]                                  |
| Audio  [=============================]                                    |
| Captions [cue] [cue] [cue]                                               |
| B-roll    [optional]                                                     |
| Playhead | Zoom | Fit                                                   |
+--------------------------------------------------------------------------+
```

**Primary actions:** edit, preview, restore version and export.  
**Secondary actions:** add B-roll, apply caption preset, crop, adjust audio and request AI edit.

**Required behavior**

- source and immutable candidate remain unchanged;
- every edit creates a new versioned draft;
- trim, split, merge, crop and caption timing have numeric alternatives;
- undo/redo, save state and conflicts are explicit;
- AI edit requests show typed operation, before/after preview and confirmation;
- B-roll failure remains non-blocking only when the fallback policy allows it;
- export is disabled until technical validation can be run.

**States:** no draft, preview loading, timeline loading, saving, saved, save conflict, autosave failed, invalid edit, render queued, render running, QA failed and export ready.

**Tablet:** show preview, candidate transcript and one contextual inspector; timeline is review-oriented and does not promise full multi-track precision. Numeric edit controls remain available.

**Desktop-only:** full multi-track timeline drag precision, simultaneous left/context + right/inspector panels and advanced track operations.

**Requirements:** FR-025 to FR-028, FR-021 to FR-024, NFR-007.

## 11. Exports and publish preparation

**Goal:** Review validated render variants and prepare a publish action.  
**Primary user:** Creator approving final content.

```text
+--------------------------------------------------------------------------+
| Exports                                       [Create export]            |
| [Status v] [Aspect v] [Source v] [Date v]                                |
+--------------------------------------------------------------------------+
| [render preview]  Vertical 9:16  00:36  Valid                          |
| Captions  AAC  H.264  1080x1920  [Open] [Publish] [Download]             |
+--------------------------------------------------------------------------+
| [render preview]  Original 16:9  QA failed: caption out of safe area     |
| [Edit in Studio] [Open diagnostics]                                       |
+--------------------------------------------------------------------------+
```

**Primary actions:** Open render, edit in Studio, prepare publish.  
**Secondary actions:** Download or duplicate export variant after validation.

**States:** queued, rendering, validating, ready, QA failed, provider unavailable and publish prohibited.

**Requirements:** FR-020 to FR-024, NFR-007.

## 12. Publishing calendar

**Goal:** Review schedule, destination, approval and publish status.  
**Primary user:** Creator or operator planning channel output.

**Views:** Month, Week, Day and Queue/List.

```text
+--------------------------------------------------------------------------+
| Calendar  [Month v] [Today]  [Schedule post]                              |
+--------------------------------------+-----------------------------------+
| Sun Mon Tue Wed Thu Fri Sat          | Scheduled post detail             |
|                                      | 9:16 preview                      |
| 1  [YT 18:30]                        | Instagram @channel                 |
| 5  [IG 10:00] [FB 10:00]             | Awaiting approval                  |
| 12 [YT 09:15] [+2]                   | [Approve] [Reschedule] [Cancel]   |
+--------------------------------------+-----------------------------------+
```

**Rules:** timezone must be explicit (default Asia/Kolkata); each event identifies platform and account; drag rescheduling is supplement to keyboard/date controls.

**States:** draft, awaiting approval, scheduled, uploading, processing, published, failed, cancelled and unknown reconciliation.

**Tablet:** month becomes week/list by default; approval and reschedule remain primary; drag/drop is optional.

**Requirements:** FR-034 to FR-036, NFR-009.

## 13. Social accounts

**Goal:** Connect only authorized publishing destinations and explain account health.  
**Primary user:** Workspace owner.

```text
+--------------------------------------------------------------------------+
| Connections                                                               |
+--------------------------------------------------------------------------+
| YouTube                                  | Instagram / Facebook            |
| Channel name  Connected  Healthy         | Page name  Permissions partial   |
| [Reconnect] [View permissions]           | [Reconnect] [Review permissions] |
+--------------------------------------------------------------------------+
```

**Rules:** use official OAuth; show scopes and permission gaps in plain language; never reveal token values; separate YouTube, Instagram and Facebook adapter status.

**States:** no account, consent pending, connected, permissions incomplete, token refresh failed, expired, disconnected and unknown API health.

**Requirements:** OUT-003, FR-032 to FR-034, NFR-004.

## 14. Published posts and analytics

**Goal:** Show confirmed publishing results and only available platform metrics.  
**Primary user:** Creator or operator measuring output.

```text
+--------------------------------------------------------------------------+
| Published                                             [Date range v]     |
+--------------------------------------+-----------------------------------+
| Post / platform / published time     | Post detail                       |
| [Post] YouTube  External ID          | 16:9/9:16 preview                |
| [Post] Instagram                    | Source / Draft / Render links     |
| [Post] Facebook                     | Metric refresh: 11:20             |
+--------------------------------------+-----------------------------------+
| Views  Watch time  Likes  Shares  Comments  (only if API returns them) |
+--------------------------------------------------------------------------+
```

**Rules:** metric definitions and refresh time are visible; unavailable metrics are labelled unavailable; no fabricated zeroes or trend forecasts.

**Tablet:** metrics reflow into labeled cards and accessible tables; post detail remains readable.

**Requirements:** FR-035, FR-040 to FR-043.

## 15. Brand Kit

**Goal:** Configure reusable brand assets and previews.  
**Primary user:** Solo creator or brand operator.

**Sections:** brand profile, logo/wordmark, colors, typography, captions, overlays, intros/outros and CTA presets.

```text
+--------------------------------------------------------------------------+
| Brand Kit                                                                |
+----------------------+---------------------------------------------------+
| Brand profiles       | Brand preview                                      |
| [Podcast]            | [representative clip frame]                        |
| [Education]          | [caption] [logo] [CTA]                             |
| [Add brand]          |                                                   |
+----------------------+---------------------------------------------------+
| Caption presets      | Logo and overlay assets                            |
+--------------------------------------------------------------------------+
```

**Rules:** preview where an asset applies; validate format/license/ownership; do not silently replace a source asset.

**States:** no brand, default brand, asset upload invalid, license missing, preview failed and save conflict.

**Requirements:** FR-021, FR-030, FR-052.

## 16. AI and processing settings

**Goal:** Configure provider capability, routing, cost limits and processing behavior.  
**Primary user:** Workspace owner or operator.

**Sections:** AI providers, routing, processing profiles, storage and hardware.

```text
+--------------------------------------------------------------------------+
| AI and processing                                         [Test config] |
+----------------------+---------------------------------------------------+
| Providers             | Provider detail                                   |
| NVIDIA Nemotron       | Status  Healthy / Degraded / Error / Disabled     |
| NVIDIA NIM            | Capabilities: modality / language / latency        |
| Gemini                | Cost/usage and model ID                          |
| OpenAI / Claude       | [Test connection] [Disable]                      |
| Groq / Deepgram       |                                                   |
| Ollama / WhisperX     |                                                   |
+----------------------+---------------------------------------------------+
| Hierarchical routing                                                     |
| 1 Workspace default > 2 Content profile override > 3 Per-job override    |
| Mode: Local-first / Balanced / Cloud-first / User-selected               |
+--------------------------------------------------------------------------+
```

**Rules:** distinguish NVIDIA API Catalog from NVIDIA NIM; show provider/model IDs and capability evidence; a provider with no verified capability is unavailable.

**Routing precedence**

1. Workspace default.
2. Content-profile override.
3. Per-job manual override.
4. Per-brand routing remains deferred.

**States:** provider healthy, degraded, auth failed, disabled, capability unknown, cost limit reached, local inference unsupported and routing fallback.

**Requirements:** FR-050, FR-051, CON-007, CON-008.

## 17. Workspace, automation policies and audit

**Goal:** Control workspace/brand separation, publishing approval and auditable operations.  
**Primary user:** Workspace owner or operator.

**Workspace section**

- workspace identity and timezone;
- initial MVP is one owner/workspace;
- brand profiles and future SaaS-ready membership boundaries;
- no billing/subscription controls in MVP.

**Automation policy section**

- account/category;
- manual, scheduled, opt-in automatic or hybrid mode;
- frequency cap and quiet hours;
- minimum QA threshold;
- rights and approval requirements.

**Audit section**

- rights changes;
- provider/routing changes;
- approval/rejection;
- policy changes;
- publishing attempts and reconciliation.

**States:** policy valid, unsaved policy, policy conflict, permission denied, policy change confirmed, audit unavailable.

**Requirements:** OUT-001, FR-034, FR-052, FR-053.

## 18. RQ-4 tablet acceptance matrix

| Experience | Tablet minimum behavior | Desktop-only behavior |
|---|---|---|
| Dashboard | Summary, active work, attention queue and primary actions | Same data with denser management layout |
| Video preview | Open/stop playback and select inspectable preview state | Full Clip Studio track editing |
| Clip review | Candidate cards, transcript excerpt, evidence and accept/reject | Multi-panel comparison and advanced timeline |
| Approve/reject | Prominent decision controls on candidate, export and scheduled post | Additional editor or policy context |
| Publishing calendar | Week/list/month navigation and reschedule using date/time controls | Drag/drop and denser event operations |
| Analytics | Available metric cards and post-source links | Wider comparison tables and charts |
| Clip Studio | Preview, transcript and one inspector; numeric edit controls | Full three/four-pane editing and multi-track timeline |

Tablet behavior must not hide an approve/reject decision inside a desktop-only menu. Full precision multi-track timeline editing is not an MVP promise on tablet.

## 19. Global interaction requirements

- `Cmd/Ctrl+K` opens global search.
- `Escape` closes dismissible overlays and restores focus.
- `Enter` activates a selected list item.
- `Space` toggles preview playback outside text fields.
- arrow keys move focus/time by documented increments.
- timecode edits accept valid numeric values and show the source-relative range.
- destructive actions require confirmation and include scope/consequence.
- autosave and export states remain visible without blocking keyboard navigation.
- status is communicated with icon plus text plus color.
- every open drawer/dialog has focus containment and focus restoration.

## 20. Traceability summary

| Requirement group | Screen coverage | Acceptance/evidence |
|---|---|---|
| FR-001 to FR-005, OUT-002 | Library, source detail, import | Integration, upload and rights evidence |
| FR-010 to FR-018 | Source detail, processing, candidate discovery | Contract, integration and manual/visual evidence |
| FR-020 to FR-028 | Clip Studio, exports | Component, E2E, visual and accessibility evidence |
| FR-030 to FR-036, OUT-003 | Metadata, calendar, exports, social accounts | OAuth, contract and reconciliation evidence |
| FR-040 to FR-043 | Published posts and analytics | Platform adapter and manual data-definition evidence |
| FR-050 to FR-053 | AI settings, workspace, audit | Unit, component, integration and security evidence |
| RQ-4 | RQ-4 tablet matrix, all review and management screens | Responsive and manual tablet walkthrough evidence |
| NFR-001, NFR-006 | Processing, overview, jobs | Reliability and observability evidence |
| NFR-007 | Clip Studio, exports | Technical render validation evidence |

## 21. Wireframe approval checklist

- [ ] All main IA route families are represented.
- [ ] Primary, secondary and recovery actions are explicit.
- [ ] Loading, empty, error, partial failure, disabled and success states are covered.
- [ ] No wireframe shows fake progress or fake analytics.
- [ ] Local upload, direct URL, Azure Blob, watched folder and authorized platform import are distinguishable.
- [ ] YouTube, Instagram Reels and Facebook Reels publishing destinations are represented.
- [ ] Hierarchical provider routing is visible in settings.
- [ ] RQ-4 tablet behavior is explicit for Dashboard, preview, clip review, approve/reject, calendar and analytics.
- [ ] Clip Studio gives preview and timeline sufficient prominence.
- [ ] Desktop-only and tablet-limited editing boundaries are explicit.
- [ ] Accessibility and responsive rules are linked for the next design phases.
- [ ] OUT-004 and OUT-005 remain visibly deferred and do not create MVP wireframe coupling.

## 22. Gate status

**Current status:** APPROVED v1 - `APPROVE WIREFRAMES v1` received.  
**Next gate:** `APPROVE DESIGN SYSTEM v1`.

Do not mark this document approved or advance to Design System until the product owner provides the explicit wireframe approval token.
