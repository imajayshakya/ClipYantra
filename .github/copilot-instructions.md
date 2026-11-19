# AI AutoClip Studio (ClipYantra) — Always-on Copilot Instructions

## Product context

Build AI AutoClip Studio (ClipYantra): a modular application that turns user-owned or otherwise authorized long-form video into reviewed short-form clips and publishes approved clips to Instagram Reels and YouTube Shorts.

Baseline decisions:
- Mixed source inputs: uploads, authorized media URLs, cloud storage imports, watched folders, and supported platform imports.
- Hybrid AI: local and cloud processing.
- AI providers: NVIDIA (API Catalog and optional self-hosted NIM), Google Gemini, OpenAI, Anthropic, Groq, Deepgram, Ollama/Qwen, WhisperX.
- Content profiles: Podcasts/Interviews, Educational/Technical, Gaming, Entertainment/Funny.
- Publishing modes: manual approval, automatic under user-configured policy, and hybrid per channel/category.
- Core application architecture target: Next.js/React/TypeScript frontend; Python/FastAPI backend; PostgreSQL; Redis/Celery; FFmpeg/OpenCV/PySceneDetect; local and Azure Blob storage adapters; Docker deployment. Treat this as a proposed baseline until discovery confirms existing repository constraints.
- AutoShorts is a research reference only until its source licence is verified. Do not copy code without a compatible licence and explicit review.

## Mandatory gated workflow
1. Discover and inspect before editing.
2. Produce requirements and assumptions.
3. Produce architecture, data flows, API boundaries and ADRs.
4. Produce risk/outcome predictions with assumptions and confidence.
5. Obtain explicit human design approval.
6. Freeze contracts and data model.
7. Scaffold placeholders only after approval.
8. Break work into small vertical slices.
9. Implement one approved slice at a time.
10. Test, independently review and report evidence before asking to proceed.

Never skip a gate. Do not infer approval. An explicit message such as `APPROVE DESIGN v1` or `APPROVE SLICE <ID>` is required.

## Change control
- Before editing, inspect `git status`, recent commits, existing conventions, tests and relevant files. Never overwrite user changes.
- Do not reformat or refactor unrelated code.
- Do not add dependencies without explaining why, alternatives, licence and maintenance impact.
- Do not silently change approved architecture, contracts, acceptance criteria or provider choices. Record a proposed change in an ADR and request approval if material.
- Keep a `docs/engineering/DECISIONS.md`, `RISKS.md`, `PHASE-STATUS.md`, and `CHANGELOG-DEV.md` once the user approves documentation creation.
- Keep `docs/engineering/PHASE-STATUS.md` current after each approved slice.

## Engineering rules
- Type-safe interfaces; Pydantic validation at API boundaries.
- Keep route handlers thin; isolate services, repositories, provider adapters and workers.
- PostgreSQL is the source of truth for workflow state. Redis/Celery is execution infrastructure, not the only durable record.
- Use idempotency, leases/locking, retry limits, outbox/reconciliation patterns where external side effects are involved.
- Store timestamps in UTC; convert for UI using the configured workspace timezone (default Asia/Kolkata).
- Store media in object/file storage, not database blobs.
- All model outputs are untrusted input: validate schemas, timestamps, language, bounds, and content before use.
- Persist provider/model/version, prompt version, input references, usage and execution outcome when available.
- Never claim a mocked provider is a real integration.
- Never claim a test, build, lint, migration or API call passed unless it was actually executed and its output inspected.
- Every behavior change requires tests. Prefer small focused tests plus relevant integration tests.
- No placeholder methods that return success or fake real publishing. Explicit stubs must fail clearly with `NotImplementedError` or a documented disabled status.

## AI provider rules
- Use a provider registry and capability registry. Route tasks only to providers/models whose verified capabilities support the required input/output modalities.
- Treat model IDs, endpoint compatibility, rate limits, context limits, supported languages, modalities, licensing and pricing as volatile. Verify current official provider documentation before implementation and record source URL plus verification date.
- NVIDIA must be a first-class provider with distinct adapters/configurations for hosted API Catalog and self-hosted NIM. Nemotron multimodal/video, vision-language, text and transcription candidates must be individually capability-checked; never assume they all share an API shape or runtime.
- Keep provider credentials server-side, encrypted or held in a secret manager. Never return keys in frontend payloads or logs.
- Support local-first, balanced, cloud-first and user-selected routing policies, but do not make unsupported claims about local GPU compatibility.

## Video and media rules
- Use FFmpeg/FFprobe for deterministic media operations; preserve originals and use temporary workspaces safely.
- Track original source timestamps when chunking audio/video.
- Gaming may require event-triggered or denser frame sampling; sparse uniform sampling alone is not sufficient evidence of complete event detection.
- Rendering, transcription, model analysis and publishing are separate restartable stages.
- Validate codec/container/duration/dimensions/audio/subtitle timing and playable output before a clip becomes publishable.
- Respect content rights, licenses, privacy, platform terms and user authorization. Do not bypass DRM or access controls.

## Publishing rules
- Use official Meta/Instagram and YouTube APIs with OAuth and documented account eligibility/permissions.
- Never use browser automation, password collection or scraping to simulate publishing.
- Require source-rights confirmation and the configured approval policy.
- Automatic mode is opt-in and must honor per-channel/category limits, quality thresholds, schedules, duplicate checks and audit history.
- Reconcile uncertain upload outcomes before retrying to prevent duplicate posts.

## Reporting format after each task
Return:
1. Scope and assumptions.
2. Files inspected/changed.
3. Implementation summary.
4. Tests/commands executed and exact result.
5. Known gaps and risks.
6. Architecture/contract deviations (or explicitly `None`).
7. Gate status: `PASS`, `BLOCKED`, or `NEEDS APPROVAL`.
8. The single next action requiring human input.
