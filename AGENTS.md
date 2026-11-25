# ClipYantra — Agent Operating Contract

The human product owner controls product scope, design approval, architecture decisions and release authorization.

## Order of authority

1. Explicit current user instruction.
2. Approved requirements, design artifacts and architecture decisions.
3. `.github/copilot-instructions.md`.
4. This file and the relevant task-specific skill/prompt.
5. Existing repository conventions.

If approved sources conflict, stop and report the conflict. Never silently choose.

## Mandatory phase sequence

1. Read-only repository discovery.
2. Requirements and assumptions.
3. UX research and user journeys.
4. Information architecture and navigation.
5. Brand/visual direction alternatives.
6. Low-fidelity screen wireframes and responsive behavior.
7. Design system, components and interaction states.
8. Accessibility and visual QA plan.
9. Technical architecture, data flows and ADRs.
10. Risk/outcome predictions with assumptions and confidence.
11. Explicit human design approval.
12. Contract/data-model freeze.
13. Placeholder scaffolding only.
14. Small vertical slices.
15. Implementation of one approved slice.
16. Automated tests and independent review.
17. Human phase gate before proceeding.

Never skip a phase. No front-end application code before the relevant design artifacts have been approved. Do not infer approval from silence, an earlier approval, a prompt being run or a generated document.

## Design authority

- `docs/design/` is the design source of truth once approved.
- The PRD is the source of truth for user needs and product scope.
- `docs/02-ARCHITECTURE.md` and ADRs are the technical source of truth once approved.
- If UI implementation conflicts with the approved design, stop and raise a design deviation.
- A designer/architect proposes; the human product owner approves.
- Do not invent brand assets, colors, typography, page structure or interaction behavior that is absent from approved design specs.
- Do not use generic AI-generated dashboard patterns, decorative gradients, gratuitous glassmorphism or repetitive cards as substitutes for product-specific design.

## Change control

- Before editing, inspect `git status --short`, branch, recent commits, conventions, relevant files and tests.
- Preserve user changes and avoid unrelated reformatting/refactors.
- Explain dependency additions, alternatives, licensing, maintenance and operational impact.
- Material changes to approved requirements, visual design, architecture, API contracts or data model require a change proposal/ADR and explicit approval.
- Maintain `docs/engineering/DECISIONS.md`, `RISKS.md`, `PHASE-STATUS.md` and `CHANGELOG-DEV.md` after documentation editing is approved.

## Engineering constraints

- Typed interfaces; Pydantic validation at API boundaries.
- Thin route handlers; isolate services, repositories, adapters and workers.
- PostgreSQL is the durable workflow source of truth; Redis/Celery is execution infrastructure.
- Use idempotency, locks/leases, bounded retries, outbox/reconciliation for external side effects.
- Store timestamps in UTC; present them in the workspace timezone (default `Asia/Kolkata`).
- Store media in object/file storage, not relational database blobs.
- Treat all model outputs as untrusted; validate schema, time ranges, language and content.
- Persist model/provider/prompt versions and usage data where available.
- Never claim mocks are real integrations or unrun commands/tests passed.
- Stubs must fail clearly or report an explicit disabled state.

## UI implementation constraints

- Use approved design tokens and semantic component variants.
- Prefer composition and reusable components over monolithic page components.
- Keep visual hierarchy clear; use typography, spacing and grouping before adding borders or color.
- Every screen must implement loading, empty, error, success and disabled/permission states where applicable.
- Every control must have an actual action, a disabled explanation, or be removed.
- Keyboard navigation, visible focus, semantic labels, contrast and reduced motion are required.
- Never use color alone to communicate status.
- Make editor interactions precise and keyboard-accessible; do not make drag-only controls the sole way to edit.
- Verify desktop, tablet and mobile behavior according to `docs/design/08-RESPONSIVE-STRATEGY.md`.
- Use real representative content or honest placeholders labelled as sample data; never fabricate analytics.
- Run visual checks with screenshots at agreed viewports after UI changes.

## AI provider rules

- Use a provider registry plus capability registry.
- Verify current official model IDs, API shape, modalities, language support, limits, costs and licensing at implementation time.
- NVIDIA API Catalog and NIM are separate adapters; model capabilities are not interchangeable.
- Do not assume local GPU compatibility.
- Keep credentials server-side and out of logs/client payloads.

## Media and rights rules

- FFmpeg/FFprobe for deterministic operations; preserve source media.
- Preserve source timestamps across chunks and edits.
- Gaming may require event-triggered/denser sampling.
- Transcription, analysis, rendering and publishing are restartable stages.
- Validate output media before publishing.
- Process only content the user owns or is authorized to use. Do not bypass DRM/access controls.

## Publishing rules

- Official Meta and YouTube APIs with OAuth and documented permissions only.
- Never simulate publishing using browser automation or password collection.
- Require rights declaration and applicable approval policy.
- Automatic publishing is opt-in and policy-bound.
- Reconcile uncertain upload outcomes before retrying.

## Required report after each task

1. Scope and assumptions.
2. Files inspected/changed.
3. Implementation or design summary.
4. Commands/tests executed and exact results.
5. Known gaps and risks.
6. Deviations from approved design/contracts (`None` if none).
7. Gate status: `PASS`, `BLOCKED` or `NEEDS APPROVAL`.
8. One next action requiring human input.
