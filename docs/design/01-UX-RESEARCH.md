# UX Research and User Needs

**Status:** RESEARCH COMPLETE — **APPROVE UX v1** required  
**Version:** v1  
**Date:** 2026-11-22  
**Prerequisites:** APPROVE DISCOVERY v1 ✓, APPROVE REQUIREMENTS v1 ✓, APPROVE REQUIREMENTS REVIEW v1 ✓

---

## Executive Summary

Research conducted against PRD v0.1, approved requirements baseline (68 requirements), requirements review findings, and hardware discovery (AMD Ryzen 5 3500U, 6GB RAM, Vega 8 2GB VRAM — no NVIDIA GPU). This document distinguishes **observed facts** (from PRD, requirements, discovery), **stated product intent** (from PRD), **assumptions** (not validated with users), and **hypotheses** (require user validation).

---

## 1. Observed Facts (From Approved Artifacts)

| Fact | Source | Confidence |
|---|---|---|
| Target users: solo creators, educators, gamers, entertainment creators, small teams | PRD Section 2 | High |
| 4 content profiles: Podcasts/Interviews, Educational/Technical, Gaming, Entertainment/Funny | PRD Section 5 | High |
| Primary workflow: Import → Transcribe → Discover → Edit → Render → Publish → Analytics | PRD Section 3, Jobs-to-be-done | High |
| MVP scope: upload, one authorized import, transcription, AI discovery for 4 profiles, vertical rendering, captions, review/approval, single-account publishing | PRD Section 8 | High |
| Hardware constraint: No NVIDIA GPU — cloud AI providers required | Discovery (CON-007) | High |
| Hardware constraint: RAM constrained (~686MB free) — limits local processing | Discovery (CON-008) | High |
| Explicit non-goals: No DRM bypass, no virality guarantees, no unauthorized publishing, no misleading edits, no DB blobs, no arbitrary code execution | PRD Section 9 | High |
| Official API publishing only (Meta OAuth, YouTube OAuth) | PRD FR-032/033, CON-003 | High |
| Human-in-the-loop mandatory for AI edits | PRD FR-028, BR-003 | High |
| Restartable async pipeline required | NFR-001, NFR-008 | High |

---

## 2. Personas — Validated as Hypotheses (Require User Validation)

### Persona 1: Solo Creator / Podcaster (Hypothesis P1)
| Attribute | Detail | Source |
|---|---|---|
| **Context** | Records long-form interviews/podcasts (30-120 min); publishes to YouTube Shorts, Reels | PRD Section 2, 5.1 |
| **Trigger** | New episode recorded; needs 3-5 clips for promotion | PRD Section 3 |
| **Desired Outcome** | Self-contained clips with accurate speaker attribution, clean captions, minimal manual edit | PRD FR-011, FR-021, FR-027 |
| **Constraints** | Limited time for editing; no video editing expertise; budget-conscious | Assumption |
| **Failure Cost** | Missed promotion window; poor clip quality damages audience trust | Assumption |
| **Key JTBD** | "Help me find the best moments without watching the full recording" | PRD Section 3, JTBD #2-3 |

**Pain Points (Hypothesized):**
- Transcript errors on proper names/technical terms
- AI cuts off context needed to understand an answer
- Caption timing drifts from speech
- Uncertainty about rights for guest appearances

### Persona 2: Educator / Technical Creator (Hypothesis P2)
| Attribute | Detail | Source |
|---|---|---|
| **Context** | Creates tutorials, code walkthroughs, technical explainers (15-60 min) | PRD Section 2, 5.2 |
| **Trigger** | New lesson recorded; needs clips highlighting key concepts | PRD Section 3 |
| **Desired Outcome** | Clips preserve problem→explanation→demo→conclusion structure; code/screen legible; terminology accurate | PRD Section 5.2 |
| **Constraints** | Technical accuracy non-negotiable; code must be readable in vertical format | Assumption |
| **Failure Cost** | Incorrect technical clip misleads audience; damages credibility | Assumption |
| **Key JTBD** | "Don't cut before the result is demonstrated; keep terminology exact" | PRD Section 5.2 |

**Pain Points (Hypothesized):**
- AI doesn't understand code context; splits mid-function
- Vertical crop obscures code/terminal output
- Technical terms mistranscribed
- Losing the "setup" that makes the "solution" intelligible

### Persona 3: Gaming Creator / Streamer (Hypothesis P3)
| Attribute | Detail | Source |
|---|---|---|
| **Context** | Long gameplay recordings/streams (2-8 hrs); facecam + gameplay + audio | PRD Section 2, 5.3 |
| **Trigger** | Stream ended; wants highlights for Shorts/Reels | PRD Section 3 |
| **Desired Outcome** | Action events + reactions captured; facecam configurable; gameplay legible; chat spikes detected | PRD Section 5.3 |
| **Constraints** | Dense/event-triggered sampling needed; high visual fidelity for gameplay | Assumption |
| **Failure Cost** | Missed highlight moments; facecam covers critical gameplay | Assumption |
| **Key JTBD** | "Find the clutch plays and genuine reactions; keep gameplay readable" | PRD Section 5.3 |

**Pain Points (Hypothesized):**
- Standard frame sampling misses brief action events
- Facecam positioning blocks minimap/health/HUD
- Audio events (kill sounds, voice spikes) not detected
- Chat/replay data integration complexity

### Persona 4: Entertainment Creator (Hypothesis P4)
| Attribute | Detail | Source |
|---|---|---|
| **Context** | Sketches, commentary, reaction videos (5-30 min); multi-person | PRD Section 2, 5.4 |
| **Trigger** | New video recorded; needs clips preserving comedic timing | PRD Section 3 |
| **Desired Outcome** | Setup→punchline→payoff preserved; multi-person layout; expressive captions | PRD Section 5.4 |
| **Constraints** | Timing is everything; cutting punchline kills joke | Assumption |
| **Failure Cost** | Broken joke structure = unfunny clip = wasted effort | Assumption |
| **Key JTBD** | "Preserve the beat; don't cut the payoff; support multi-speaker layouts" | PRD Section 5.4 |

**Pain Points (Hypothesized):**
- AI doesn't recognize comedic structure
- Multi-speaker caption attribution errors
- Reaction shots separated from triggering moment
- Expressive caption styling limited

### Persona 5: Content Operator / Small Team (Hypothesis P5)
| Attribute | Detail | Source |
|---|---|---|
| **Context** | Manages 3-10 channels across brands; approval workflows needed | PRD Section 2, FR-052, FR-034 |
| **Trigger** | Team produces content; needs review/approval/scheduling | PRD Section 3 |
| **Desired Outcome** | Policy-gated publishing; audit trail; calendar; permissions; cross-channel analytics | PRD FR-034, FR-035, FR-040, FR-052 |
| **Constraints** | Brand separation mandatory; compliance/audit requirements | Assumption |
| **Failure Cost** | Unauthorized publish = brand risk; duplicate publish = platform penalty | Assumption |
| **Key JTBD** | "Enforce approval policies; show me what's scheduled; audit everything" | PRD FR-034, FR-035, FR-053 |

**Pain Points (Hypothesized):**
- No visibility into team's clip pipeline
- Manual approval bottleneck
- Analytics fragmented across platforms
- Rights tracking across multiple creators

---

## 3. End-to-End User Journey (Validated Against Requirements)

### Journey Map: Source Import → Analytics Feedback

| Stage | User Action | System Response | Requirements | Pain Points (Hypothesized) |
|---|---|---|---|---|
| **1. Workspace Setup** | Create/select workspace, brand profile | Show workspace dashboard, brand settings | FR-052, BR-007 | — |
| **2. Source Import** | Upload file / import from cloud / watched folder | Validate file, show metadata, estimate cost/time | FR-001, FR-002, FR-004, FR-005 | Rights declaration friction; upload failures on large files |
| **3. Rights Declaration** | Confirm ownership/permission, add provenance | Record rights record, block processing until complete | FR-003, CON-001 | Legal language unclear; guest rights complex |
| **4. Profile Selection** | Choose content profile, language, AI policy | Show profile-specific options, provider routing | FR-014, FR-016, FR-050 | Unclear which profile fits; AI policy options overwhelming |
| **5. Processing** | Start analysis | Show honest progress (stage, %, ETA, cost) | NFR-001, NFR-006, FR-051 | Black-box processing; no stage visibility; cost uncertainty |
| **6. Candidate Review** | Browse ranked candidates with evidence | Show start/end, transcript evidence, category, score, rationale | FR-014, FR-015, FR-016, FR-017, FR-018 | Too many/few candidates; rationale opaque; boundaries wrong |
| **7. Clip Studio (Edit)** | Open candidate → trim, crop, caption, B-roll, effects | Multi-track timeline; preview; undo/redo; versioned drafts | FR-025, FR-026, FR-027, FR-028 | Timeline lag; keyboard inaccessible; caption editing tedious |
| **8. Quality Check** | Run validation | Technical validation (NFR-007), preview export | NFR-007, FR-020, FR-021, FR-022, FR-023 | Validation errors cryptic; export preview slow |
| **9. Metadata Prep** | Edit title, caption, hashtags, CTA per platform | Platform-specific suggestions, character counts | FR-030, FR-031 | Platform limits change; hashtag suggestions irrelevant |
| **10. Publish Decision** | Approve / schedule / set auto-policy | Record decision, enforce policy, show audit trail | FR-032, FR-033, FR-034, FR-035, FR-036 | Policy confusion; fear of accidental auto-publish |
| **11. Publishing** | Trigger publish / wait for schedule | OAuth → Official API → record external ID, status | FR-032, FR-033, NFR-003 | OAuth token expiry; rate limits; duplicate detection |
| **12. Monitoring** | View publish status, reconciliation | Show platform processing state, external ID | FR-035, FR-036 | Uncertain outcomes (processing vs failed) |
| **13. Analytics** | Review performance snapshots | Timestamped metrics associated to source/candidate | FR-040, FR-041, FR-042, FR-043 | Metrics delayed; attribution unclear; no actionable insights |

---

## 4. Moments of Uncertainty (Critical UX Risks)

| Moment | Uncertainty | Mitigation (From Requirements) |
|---|---|---|
| **Rights Declaration** | "Do I have permission for this guest clip?" | FR-003: Explicit rights record required before processing |
| **Processing Start** | "How long? How much? What if it fails?" | NFR-006: Structured progress; FR-050: Cost limits; NFR-001: Restartable |
| **Candidate Selection** | "Why this clip? Is the boundary right?" | FR-014: Evidence + rationale; FR-015: Boundary validation |
| **AI Edit Suggestion** | "Will this edit break context?" | FR-028: Preview + validation + undo/redo; BR-003: Human-in-loop |
| **Crop/Framing** | "Is gameplay/code readable in 9:16?" | FR-022: Face/speaker-aware crop + manual override |
| **Publish Policy** | "Will this auto-publish without my approval?" | FR-034: Explicit opt-in; FR-035: Audit trail |
| **Publish Outcome** | "Did it actually post? Is it processing?" | FR-035: External ID + status; FR-036: Reconciliation |
| **Analytics** | "Is this metric real? What changed?" | FR-041: Association to source/candidate/creative vars |

---

## 5. Jobs-to-be-Done (From PRD Section 3, Validated)

| JTBD | Requirements | Success Signal (Measurable) |
|---|---|---|
| **JTBD-1**: Import long video from permitted source | FR-001, FR-002, FR-003, FR-004, FR-005 | Upload success rate; resume success rate |
| **JTBD-2**: Understand what was said/shown with timestamps | FR-010, FR-011, FR-012, FR-013 | Transcript WER; scene boundary F1; diarization accuracy |
| **JTBD-3**: Discover self-contained clip candidates | FR-014, FR-015, FR-016, FR-017, FR-018 | Candidate precision/recall vs human labels; boundary accuracy |
| **JTBD-4**: Review why each candidate selected; edit boundaries | FR-014 (rationale), FR-027 (edit ops) | Edit rate per candidate; boundary adjustment magnitude |
| **JTBD-5**: Render professional short-form variants | FR-020, FR-021, FR-022, FR-023, FR-024 | Render success rate; caption sync error; crop correctness |
| **JTBD-6**: Prepare platform-specific metadata | FR-030, FR-031 | Metadata edit rate; character limit compliance |
| **JTBD-7**: Approve/schedule/auto-publish under explicit policy | FR-032, FR-033, FR-034, FR-035, FR-036 | Policy compliance rate; duplicate rate; reconciliation success |
| **JTBD-8**: Measure performance; inform future choices | FR-040, FR-041, FR-042, FR-043 | Metric freshness; attribution completeness; recommendation click-through |

---

## 6. Research Questions Requiring User Input

### High Priority (Block Design Decisions)

| Question | Related Design Decision | Method |
|---|---|---|
| **RQ-1**: Which import workflow is primary: single upload, batch, watched folder, or live capture? | Information architecture: home/dashboard layout; ingestion slice scope | Survey + analytics on existing workflows (if any) |
| **RQ-2**: How many candidates should appear initially (5, 10, 20, infinite scroll)? | Clip Studio candidate list density; pagination vs virtual scroll | Usability test with 5-8 users per persona |
| **RQ-3**: Which edit operations are must-haves in browser vs can defer to desktop? | Clip Studio MVP scope (FR-027); responsive strategy | Card sort + task completion timing |
| **RQ-4**: Is tablet editing required for MVP or desktop-only? | Responsive strategy (08-RESPONSIVE-STRATEGY.md); FR-026 | Contextual inquiry: where do users edit? |
| **RQ-5**: How granular should AI model control be (provider, model, temperature, per-profile)? | Provider capability routing UI; FR-050 | Wizard-of-Oz prototype with config options |

### Medium Priority (Inform UX Polish)

| Question | Related Design Decision | Method |
|---|---|---|
| **RQ-6**: Automatic publishing: per workspace, channel, category, or clip? | Policy UI; FR-034 | Preference ranking exercise |
| **RQ-7**: Acceptable processing time/cost per source hour? | Progress UX; cost display; NFR-001, FR-050 | Willingness-to-pay survey + benchmark data |
| **RQ-8**: How do users want to see "AI reasoning" for candidates? | Candidate card design; FR-014 rationale display | A/B test: summary vs detailed evidence |

### Low Priority (Post-MVP)

| Question | Related Design Decision | Method |
|---|---|---|
| **RQ-9**: Live-stream monitor workflow (if OUT-004 = v1) | Real-time ingestion UI | Deferred |
| **RQ-10**: Audio dubbing/B-roll workflow (if OUT-005 = v1) | Rendering pipeline UI | Deferred |

---

## 7. Success Measures (Proposed Baselines — Require Measurement)

| Measure | Definition | Target (To Be Validated) |
|---|---|---|
| **Time to First Candidate** | Source import complete → first candidate visible | < 5 min for 30-min video (cloud processing) |
| **Candidate Acceptance Rate** | Candidates accepted (published or saved) / total shown | > 30% (baseline from human-labeled fixtures) |
| **Edit Time per Clip** | Open Clip Studio → approve export | < 10 min for simple trim/caption; < 20 min for multi-track |
| **Caption Correction Time** | Auto-caption → user-approved caption | < 2 min per minute of clip |
| **Render Success Rate** | Successful renders / render attempts | > 98% |
| **Publish Success Rate** | Published posts / publish attempts | > 99% (excl. platform outages) |
| **Duplicate Publish Rate** | Duplicate incidents / publish attempts | < 0.1% |
| **Recovery Success Rate** | Jobs recovered from failure / failed jobs | > 95% (NFR-001) |
| **Trust Score (Self-Reported)** | "I trust the candidate selection" / "I trust publish status" | > 4.0/5.0 (quarterly survey) |

---

## 8. Assumptions vs Facts Summary

| Category | Assumptions (Not User-Validated) | Facts (From Approved Artifacts) |
|---|---|---|
| **Personas** | All 5 personas exist with stated behaviors | PRD defines 5 user types (Section 2) |
| **Workflows** | Single upload is primary; batch is secondary | PRD MVP: upload + one authorized import |
| **Pain Points** | Rights friction, transcript errors, crop issues | CON-001, NFR-007, FR-022 documented |
| **Edit Operations** | Trim/split/crop/caption are core; merge/B-roll advanced | FR-027 lists core ops; FR-024 B-roll fail-soft |
| **Device** | Desktop primary; tablet secondary for MVP | Not specified in PRD — needs RQ-4 |
| **AI Control** | Users want per-profile provider selection | FR-050: configure providers, routing, cost limits |
| **Publishing** | Manual approval default; auto opt-in per channel | FR-034: manual, opt-in auto, hybrid per account/category |
| **Processing Time** | Users tolerate 5-10 min for 30-min video | Not specified — needs RQ-7 |

---

## 9. Research Plan (Minimum Viable)

### Phase 1: Remote Usability (Week 1-2)
- **Participants:** 5-8 users across 3+ personas (recruit from creator communities)
- **Tasks:** 
  1. Upload 30-min video → select profile → review candidates
  2. Edit candidate in Clip Studio (trim, caption, crop)
  3. Prepare metadata → publish to test account
- **Metrics:** Task success, time, error rate, SUS score

### Phase 2: Contextual Inquiry (Week 2-3)
- **Participants:** 3-5 content operators (Persona 5)
- **Focus:** Approval policies, multi-brand management, analytics review
- **Method:** Screen share + think-aloud on current workflow

### Phase 3: Benchmark Validation (Week 3-4)
- **Sample:** 20 representative videos across 4 profiles
- **Metrics:** Processing time, cost, candidate quality vs human labels
- **Purpose:** Validate success measure baselines

---

## 10. Open Decisions Blocking UX Design

| Decision | Required For | Status |
|---|---|---|
| **OUT-001**: Deployment model (self-hosted vs SaaS) | Auth flow, workspace switching, onboarding | **BLOCKING** — needs product owner |
| **OUT-002**: Import connectors (local/Azure/watched) | Ingestion screen, source types, progress UX | **BLOCKING** — needs product owner |
| **OUT-003**: Publishing channels (YouTube/Meta/both) | OAuth flow, destination picker, metadata fields | **BLOCKING** — needs product owner |
| **RQ-4**: Tablet editing for MVP | Responsive strategy, Clip Studio layout | **NEEDS RESEARCH** — Phase 1 |
| **RQ-3**: Browser vs desktop edit ops | Clip Studio MVP scope | **NEEDS RESEARCH** — Phase 1 |

---

## 11. Confidence Assessment

| Area | Confidence | Basis |
|---|---|---|
| Persona definitions | **Medium** | PRD-defined, not user-validated |
| Core journey | **High** | Directly from PRD jobs-to-be-done + requirements |
| Pain points | **Low-Medium** | Hypothesized from requirements + analogous products |
| Success measures | **Low** | No baseline data; proposed targets only |
| Research questions | **High** | Derived from design decision dependencies |

---

## 12. Next Steps

1. **Product owner resolves OUT-001, OUT-002, OUT-003** (blocking IA and ingestion/publishing design)
2. **Conduct Phase 1 usability research** (5-8 users, 3+ personas)
3. **Update this document with validated findings** (replace hypotheses with evidence)
4. **Request `APPROVE UX v1`** with research evidence
5. **Proceed to Information Architecture** (prompt 03-information-architecture) and **Visual Direction** (prompt 04-brand-visual-directions)

---

**Gate Status:** `NEEDS APPROVAL` — Requires **product-owner resolution of OUT-001, OUT-002, OUT-003** AND **`APPROVE UX v1`** before proceeding to Information Architecture and Visual Direction phases.
