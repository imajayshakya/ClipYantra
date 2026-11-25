# ClipYantra — Always-on Copilot Instructions

## Product context

Build **ClipYantra (AI AutoClip Studio)**: a modular AI content-repurposing platform that turns user-owned or otherwise authorized long-form video into editable short-form assets and publishes approved content to Instagram/Facebook Reels and YouTube Shorts.

Baseline decisions are proposals until repository discovery and explicit approval:
- Mixed inputs: uploads, authorized media URLs, cloud storage imports, watched folders and supported platform imports where terms and rights permit.
- Hybrid local + cloud AI.
- Providers under consideration: NVIDIA API Catalog and optional self-hosted NIM; Gemini; OpenAI; Anthropic; Groq; Deepgram; Ollama/Qwen; WhisperX.
- Profiles: Podcasts/Interviews, Educational/Technical, Gaming, Entertainment/Funny.
- Publishing: manual approval, opt-in automatic and hybrid per channel/category.
- Proposed stack: Next.js/React/TypeScript; FastAPI; PostgreSQL; Redis/Celery; FFmpeg/FFprobe/OpenCV/PySceneDetect; local/Azure Blob storage; Docker.

## Non-negotiable development philosophy

Work as a **requirements-led, design-first, test-driven and evidence-based engineering team**. Do not jump from a broad idea directly to code. Treat requirements, design, architecture, contracts, implementation and verification as separate deliverables with explicit gates.

## Mandatory end-to-end workflow

1. **Repository discovery (read-only):** inspect Git status, branches, commits, structure, existing architecture, dependencies, tests, CI, runtime and hardware. Do not edit files.
2. **Requirements elicitation:** ask/record unresolved questions, users, jobs-to-be-done, source constraints, workflows, non-goals and assumptions. Do not silently fill material gaps.
3. **Requirements baseline:** produce functional requirements, non-functional requirements, user stories, measurable acceptance criteria, priorities and constraints. Assign stable IDs (`FR-*`, `NFR-*`, `CON-*`, `AC-*`).
4. **UX and design:** research, user journeys, information architecture, visual directions, wireframes, design system, responsive behavior, accessibility and error/empty/loading states.
5. **Architecture:** produce component boundaries, sequence/data-flow diagrams, deployment view, data model, API/event contracts and ADRs.
6. **Risk and outcome prediction:** assess technical, product, security, privacy, licensing, cost, latency, GPU, operational and platform risks. State assumptions, likelihood, impact, confidence and validation experiment. Predictions are hypotheses, not facts.
7. **Test and QE planning:** create a risk-based test strategy, test levels, test data/environment plan, automation scope, traceability matrix and Definition of Ready/Done.
8. **Human approval:** obtain explicit, versioned approvals for requirements, UX, visual direction, design system, architecture, contracts and QE plan. Never infer approval.
9. **Contract freeze:** freeze approved schemas, APIs, events, state machines, error models and acceptance criteria. Changes require impact analysis and approval.
10. **Placeholder scaffolding:** create only approved folders, modules, interfaces, empty routes/components, migrations skeletons and health checks. No fake business behavior.
11. **Vertical-slice planning:** decompose one milestone into small, end-to-end, independently verifiable slices. Each slice must have a requirement ID, acceptance criteria, dependencies, risks, files, tests and rollback plan.
12. **Chunk implementation loop:** for each approved slice: inspect → plan → implement minimal change → run focused tests → run relevant integration tests → static checks → independent review → fix → rerun → record evidence.
13. **Verification and validation:** verify implementation against technical specifications and validate user/business outcomes against acceptance criteria. Keep these distinct.
14. **QE and phase gate:** assess requirement coverage, test results, unresolved defects, regression results, security/accessibility/visual checks as applicable. Report PASS, BLOCKED or NEEDS APPROVAL.
15. **Release readiness:** confirm release criteria, migration/rollback, observability, support notes, security and operational readiness before release.

## Approval tokens

Require explicit messages in the current conversation, such as:
- `APPROVE DISCOVERY v1`
- `APPROVE REQUIREMENTS v1`
- `APPROVE UX v1`
- `APPROVE VISUAL DIRECTION v1`
- `APPROVE WIREFRAMES v1`
- `APPROVE DESIGN SYSTEM v1`
- `APPROVE DESIGN v1`
- `APPROVE ARCHITECTURE v1`
- `APPROVE QE PLAN v1`
- `APPROVE CONTRACTS v1`
- `APPROVE SCAFFOLD v1`
- `APPROVE SLICE <ID>`
- `ACCEPT SLICE <ID>`
- `APPROVE RELEASE <VERSION>`

A draft, prompt run, status report, silence or a previous approval for another version is not approval.

## Requirements engineering rules

- Every requirement must have a stable ID, source/rationale, priority, owner or decision-maker, acceptance criteria, dependencies and verification method.
- Separate functional requirements, quality attributes/non-functional requirements, business rules, constraints, assumptions and out-of-scope items.
- Write acceptance criteria as observable outcomes; prefer Given/When/Then where useful.
- Avoid ambiguous terms such as fast, secure, intuitive, seamless or scalable unless quantified or tied to a measurable test.
- Maintain bidirectional traceability: requirement → design element → API/data component → implementation slice → test case → evidence.
- Mark each statement as confirmed, assumed, proposed or unresolved.
- Do not invent user answers. Ask focused questions when an unresolved decision materially changes architecture, UX, cost, safety or scope.

## Design-first rules

For product/UI work, complete research, journeys, IA, visual direction, wireframes, design tokens, component states, responsive rules, accessibility and visual QA plan before frontend implementation. The Clip Studio must privilege preview, timeline, transcript and contextual inspector. Avoid generic dashboards, decorative gradients, excess cards and fake metrics. Every control must work or be explicitly disabled with a reason. Design changes require an approved change request.

## Quality Engineering rules

- QE is continuous, not a final QA phase. Plan quality before implementation and build verification into every slice.
- Use a risk-based test pyramid: unit/component tests, API/service integration tests, contract tests, workflow/E2E tests, visual/accessibility tests, performance/reliability/security tests as appropriate.
- For each slice, define test cases before or alongside implementation. Include positive, negative, boundary, failure/retry and permission cases.
- Tests must assert meaningful outcomes, not merely execute code. Do not weaken assertions to make tests pass.
- Never replace a failing test with a skip, mock or loose assertion without explaining and obtaining approval where behavior changes.
- Use deterministic fixtures and synthetic/sample media where possible. Do not place real credentials or private user media in tests.
- Report exact commands, environment, test counts, failures and skipped tests. Distinguish not-run from passed.
- Maintain a defect log with severity, reproducibility, impact, root cause, fix and regression test.
- A slice is not done while acceptance criteria lack evidence, critical/high defects remain, or required tests have not run.

## Change control

Before every edit inspect `git status`, branch, recent commits, relevant files and tests. Preserve user changes. Do not reformat unrelated files. Explain dependency purpose, alternatives, licence and maintenance impact. Material deviations from approved requirements, UX, architecture, contracts, test strategy or acceptance criteria require impact analysis, ADR/change request and explicit approval.

Maintain:
- `docs/engineering/DECISIONS.md`
- `docs/engineering/RISKS.md`
- `docs/engineering/PHASE-STATUS.md`
- `docs/engineering/CHANGELOG-DEV.md`
- `docs/engineering/REQUIREMENTS-TRACEABILITY.csv`
- `docs/engineering/DEFECT-LOG.md`

## Engineering rules

- Typed interfaces; Pydantic validation at API boundaries.
- Thin API routes; isolate services, repositories, providers and workers.
- PostgreSQL is durable workflow state; Redis/Celery is execution infrastructure.
- Use idempotency, leases/locks, bounded retries, outbox/reconciliation for side effects.
- UTC in storage, configured workspace timezone in UI (default Asia/Kolkata).
- Object storage for media; no relational DB blobs.
- Validate model output and timestamps before use.
- Record provider/model/prompt versions and usage where available.
- Never claim mocks are real integrations or tests passed unless executed.
- Stubs must fail clearly or show explicit disabled status.

## AI provider rules

Use provider and capability registries. Verify official model IDs, modalities, languages, API shapes, limits, pricing, data handling, licensing and GPU requirements when implementing. NVIDIA API Catalog and NIM are distinct. Keep secrets server-side. Model outputs are untrusted data and must be validated.

## Media rules

Use FFmpeg/FFprobe for deterministic operations; preserve originals and source timestamps. Gaming may require dense/event-triggered sampling. Keep transcription, analysis, rendering and publishing restartable. Validate final output before publishing. Respect rights, consent and platform terms.

## Publishing rules

Official Meta/Instagram and YouTube APIs with OAuth only. Automatic publishing is opt-in, policy-bound, auditable and idempotent. Reconcile uncertain outcomes before retrying.

## Required report after every task

1. Scope and requirement/slice IDs.
2. Assumptions and unresolved decisions.
3. Files inspected and changed.
4. Implementation summary.
5. Exact commands/tests and actual results.
6. Requirement-to-test traceability evidence.
7. Defects, gaps and risks.
8. Architecture/design/contract deviations (or `None`).
9. Gate status: `PASS`, `BLOCKED` or `NEEDS APPROVAL`.
10. One next human action.
