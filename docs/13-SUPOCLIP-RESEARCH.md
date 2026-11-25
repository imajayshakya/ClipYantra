# SupoClip Research and Adoption Assessment

**Reviewed:** 2026-11-22  
**Repository:** https://github.com/FujiwaraChoki/supoclip  
**Assessment status:** Static documentation/repository review; no local build or runtime test performed.

## 1. Repository summary

SupoClip describes itself as an open-source OpusClip alternative. Its README advertises long-form video ingestion, transcript-driven LLM selection, clip scoring, face-centered vertical cropping, word-synced subtitles, hook titles, optional Pexels B-roll, a built-in clip editor, direct publishing, performance feedback and real-time progress. It documents YouTube/Twitch/Kick/upload inputs and says live streams are not supported by the listed import flow.

The docs describe a multi-service design: Next.js frontend and API routes, FastAPI backend, Redis queue, ARQ worker, PostgreSQL and file storage. The architecture guide describes task creation returning quickly while processing happens out of band, with SSE progress events. It has a layered route/service/repository backend and a pipeline for acquisition, transcription, segment selection, rendering and persistence.

## 2. High-value patterns to adapt

| SupoClip pattern | ClipYantra decision |
|---|---|
| Task creation is fast; workers process asynchronously | ADOPT |
| Explicit source/task/generated-clip persistence | ADOPT; expand with rights, job stages and provenance |
| Live progress via SSE | ADOPT as default; retain REST status refetch fallback |
| Layered route/service/repository design | ADOPT |
| Word-timed transcript and LLM segment selection | ADAPT; capability-based provider router and multi-signal discovery |
| Hook/engagement/value/shareability scoring | ADAPT; editorial scores with evidence, not predicted virality probability |
| Face-aware vertical crop | ADOPT with manual override and speaker tracking |
| Caption templates/custom fonts | ADOPT with font licence tracking |
| Optional B-roll and transitions | ADOPT later; licence-aware and fail-soft |
| Built-in trim/split/merge editor | ADOPT |
| Video/B-roll/Captions/Audio timeline tracks | ADOPT and extend with effects/brand tracks |
| Generated output immutable; edits stored as drafts | ADOPT |
| AI edits translated into operations and undo | ADOPT with strict allow-listed operation schema |
| Source-map sidecar for B-roll timing | ADAPT; persist versioned source-map/edit graph in DB plus sidecar cache where useful |
| Vertical and original-aspect output | ADOPT |
| Platform presets and direct publishing | ADAPT only through current official platform APIs |
| Performance feedback loop | ADOPT; only official available metrics and evidence-aware learning |
| Backend/frontend/E2E test layers | ADOPT |
| ARQ + Redis | DO NOT inherit by default; existing ClipYantra baseline uses Celery unless ADR changes it |
| Prisma plus backend persistence | Avoid duplicate authority; use one approved ORM/schema owner |
| Hosted billing/subscriptions | DEFER until product owner approves SaaS monetization |

## 3. Specific UX/product improvements to include

1. **Clip Studio:** preview, clip picker, multi-track timeline, reversible edits, transcript/caption correction and crop/audio controls.
2. **AI-assisted edit:** user writes a natural-language instruction; the LLM returns typed operations; backend validates; UI shows preview/diff; user applies; one undo action reverses it.
3. **B-roll planning:** timeline-aligned cues, asset provenance/attribution and cache retention. If an optional provider fails, skip B-roll and warn instead of failing the core render.
4. **Task progress:** stage-level progress events and durable status endpoint so the UI can reconnect after reload.
5. **Creative workflows:** highlights first; later topic clips, recap, trailer, series and creator instructions as separate workflow templates.
6. **Feedback loop:** post-level analytics snapshots linked back to candidate/editorial variables.

## 4. Patterns to improve rather than copy verbatim

- Use a durable relational job record and outbox rather than relying on queue state alone.
- Use current official APIs for publishing and supported platform import flows; no scraping to mimic authenticated publishing.
- Validate account eligibility, app permissions and API metric availability at runtime.
- Treat external model scores as subjective editorial signals, not virality guarantees.
- Use a platform capability matrix so changes in API constraints are versioned and tested.
- Preserve original media and source timestamps through all versions.

## 5. Licensing warning

The repository README and root licence identify AGPL-3.0. The app-guide self-host section contains the phrase “SupoClip Noncommercial Source License”, which is inconsistent with those root-level references. Do not copy, fork, port or substantially adapt SupoClip implementation code until the exact licence applicable to the chosen commit is verified and a qualified reviewer approves the planned distribution/hosting model. This document recommends adopting product/architecture ideas only, not copying source code. See `14-LICENSING-AND-THIRD-PARTY.md`.

## 6. Sources reviewed

- README: https://github.com/FujiwaraChoki/supoclip/blob/main/README.md
- Architecture: https://github.com/FujiwaraChoki/supoclip/blob/main/docs/architecture.md
- App guide: https://github.com/FujiwaraChoki/supoclip/blob/main/docs/app-guide.md
- Configuration: https://github.com/FujiwaraChoki/supoclip/blob/main/docs/configuration.md
- Development/testing: https://github.com/FujiwaraChoki/supoclip/blob/main/docs/development.md
- API reference: https://github.com/FujiwaraChoki/supoclip/blob/main/docs/api-reference.md
- Root licence: https://github.com/FujiwaraChoki/supoclip/blob/main/LICENSE

Repository content changes. Recheck commit SHA, files and licence before any future use.
