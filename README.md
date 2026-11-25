# ClipYantra — Complete Product, Design & Copilot Starter Kit

> **Product:** ClipYantra (AI AutoClip Studio)
> **Status:** Contract and design baselines approved. Placeholder scaffold is authorized by `APPROVE SCAFFOLD v1`; implementation slices remain blocked on slice approval.
> **Purpose:** Start a new or existing ClipYantra repository with a complete product/engineering plan, a design-first workflow, reusable Copilot skills, specialist agents and sequential approval-gated prompts.

## What is included

- Product requirements, architecture, data model, APIs, AI-provider routing, media pipeline, publishing, analytics, security, testing, deployment and third-party research.
- A complete design foundation: UX research, information architecture, brand direction, visual system, screen specifications, interaction states, accessibility, responsive behavior and visual QA.
- Workspace Copilot instructions, root `AGENTS.md`, scoped frontend instructions, specialist agents, reusable Agent Skills and sequential prompts.
- Design is a mandatory phase before frontend scaffolding or implementation.
- Existing proposed decisions are clearly labelled as proposals until discovery and human approval.

## Start from the beginning

1. Extract this archive into a new folder or merge the contents into your existing repository after backing it up.
2. Open the repository root in VS Code. Do not copy over an existing file blindly; merge user-owned instructions and documentation.
3. Read `AGENTS.md`, `.github/copilot-instructions.md` and this README.
4. Select the **Architect** agent and run `/00-project-discovery`.
5. Follow prompts in `.github/prompts/` in numeric order. The workflow includes product discovery, UX research, information architecture, visual exploration, wireframes, design system, architecture, risk predictions, design approval, contract freeze, scaffold and one-slice development.
6. Do not implement UI until the design system and screen specifications are approved.
7. After each approved slice, run independent QA and the phase gate before continuing.

## Proposed product baseline

- Inputs: uploads, authorized media URLs, cloud storage imports, watched folders and supported platform imports where terms and rights permit.
- Processing: hybrid local + cloud AI.
- AI providers under consideration: NVIDIA API Catalog, optional self-hosted NVIDIA NIM, Gemini, OpenAI, Anthropic, Groq, Deepgram, Ollama/Qwen and WhisperX.
- Content profiles: Podcasts/Interviews, Educational/Technical, Gaming, Entertainment/Funny.
- Outputs: vertical Reels/Shorts, plus square and original-aspect exports where useful.
- Publishing: manual approval, opt-in automatic policy and hybrid per channel/category.
- Channels: Instagram/Facebook Reels and YouTube Shorts using official APIs and valid account permissions.
- Proposed application stack: Next.js/React/TypeScript, FastAPI, PostgreSQL, Redis/Celery, FFmpeg/FFprobe/OpenCV/PySceneDetect, local/Azure Blob storage and Docker.
- Proposed design direction: premium creator workstation, dark-first editing environment, calm neutral surfaces, clear information hierarchy, restrained accent color, strong editing ergonomics and a responsive management experience. This is a design hypothesis, not an approved visual design.

## Design-first rule

The UI process is intentionally separate from the backend architecture process:

1. User/job research and key workflows.
2. Information architecture and navigation.
3. Brand/visual direction exploration.
4. Low-fidelity wireframes and page composition.
5. Design system and component states.
6. Interaction, motion, responsive and accessibility specification.
7. Human design approval.
8. Only then: frontend scaffold, component implementation and visual verification.

Use `docs/design/` as the design source of truth. Do not invent screens or styling during implementation when approved design specifications exist. If the design proves incomplete, raise a design change request rather than improvising.

## Important workflow gates

- `APPROVE REQUIREMENTS v1`
- `APPROVE UX v1`
- `APPROVE VISUAL DIRECTION v1`
- `APPROVE WIREFRAMES v1`
- `APPROVE DESIGN SYSTEM v1`
- `APPROVE DESIGN v1`
- `APPROVE CONTRACTS v1`
- `APPROVE SCAFFOLD v1`
- `APPROVE SLICE <ID>`

Approval must be explicit in the current conversation. A draft, prompt run, status report or silence is not approval.

## Placeholder scaffold status

The repository currently contains documentation, approved skills and a placeholder-only application structure. Placeholder scaffold rules:

- No provider, social platform or media worker call is implemented.
- No database migration creates or mutates application state.
- No package dependencies are approved or installed.
- Backend modules that are not implemented raise `NotImplementedError` or expose an explicit disabled state.
- Frontend folders contain no unapproved page/component implementation.
- Docker and CI files are skeleton placeholders, not business integrations.
- Vertical-slice implementation begins only after `APPROVE SLICE <ID>`.

## VS Code setup

- Workspace instructions: `.github/copilot-instructions.md`
- Root agent instructions: `AGENTS.md`
- File-scoped instructions: `.github/instructions/`
- Custom agents: `.github/agents/`
- Skills: `.github/skills/<skill-name>/SKILL.md`
- Reusable prompts: `.github/prompts/*.prompt.md`

In VS Code, open the Command Palette and run **Chat: Open Customizations** to inspect the discovered skills, agents and prompts. Start a new Copilot chat after adding or changing customizations. Exact UI labels can vary by VS Code release.

## Design quality bar

- No generic dashboard template with decorative gradients and repetitive cards.
- No arbitrary pixel-level styling without tokens or layout rules.
- No icon-only actions without accessible names/tooltips where needed.
- No fake metrics or fake processing states.
- Every screen must specify loading, empty, error, success and permission/disabled states where applicable.
- Every interactive control must have a working behavior or be explicitly marked as disabled/unavailable.
- Use semantic tokens, consistent spacing/type scales, keyboard focus and reduced-motion support.
- The Clip Studio is a productivity tool: optimize timeline readability, preview focus, editing precision and recoverability.

## Third-party and licensing boundaries

SupoClip, AutoShorts and GTA VI Clip Desk are research references. Do not copy code, prompts, assets or substantial expressive text until exact applicable licenses and dependencies are reviewed. See `docs/14-LICENSING-AND-THIRD-PARTY.md`.

## Documentation map

### Product and engineering

- `docs/01-PRODUCT-REQUIREMENTS.md`
- `docs/02-ARCHITECTURE.md`
- `docs/03-DATA-MODEL.md`
- `docs/04-API-CONTRACTS.md`
- `docs/05-AI-PROVIDER-STRATEGY.md`
- `docs/06-MEDIA-PIPELINE.md`
- `docs/07-CLIP-STUDIO-UX.md`
- `docs/08-PUBLISHING-AND-SCHEDULING.md`
- `docs/09-ANALYTICS-AND-LEARNING.md`
- `docs/10-SECURITY-PRIVACY-RIGHTS.md`
- `docs/11-TESTING-STRATEGY.md`
- `docs/12-DEPLOYMENT-OPERATIONS.md`
- `docs/13-SUPOCLIP-RESEARCH.md`
- `docs/14-LICENSING-AND-THIRD-PARTY.md`
- `docs/15-RISKS-AND-PREDICTIONS.md`
- `docs/16-IMPLEMENTATION-ROADMAP.md`
- `docs/17-ACCEPTANCE-CRITERIA.md`

### Design source of truth

- `docs/design/00-DESIGN-OVERVIEW.md`
- `docs/design/01-UX-RESEARCH.md`
- `docs/design/02-INFORMATION-ARCHITECTURE.md`
- `docs/design/03-BRAND-VISUAL-DIRECTION.md`
- `docs/design/04-DESIGN-SYSTEM.md`
- `docs/design/05-SCREEN-SPECIFICATIONS.md`
- `docs/design/06-INTERACTION-AND-STATES.md`
- `docs/design/07-ACCESSIBILITY.md`
- `docs/design/08-RESPONSIVE-STRATEGY.md`
- `docs/design/09-VISUAL-QA.md`
- `docs/design/10-DESIGN-DECISIONS.md`

### Engineering state

- `docs/engineering/DECISIONS.md`
- `docs/engineering/RISKS.md`
- `docs/engineering/PHASE-STATUS.md`
- `docs/engineering/CHANGELOG-DEV.md`
- `docs/engineering/adr/`

## Disclaimer

This pack is a planning and customization starter. It does not prove that the repository has been discovered, the proposed stack is compatible, the APIs are approved, the visual design is approved, or any feature is implemented. Verify all current model IDs, API permissions, platform rules, dependencies and licenses during the relevant phase.


## Expanded Flow AI + Quality Engineering system (v3)

The v3 pack adds explicit requirements engineering, verification/validation and Quality Engineering controls. It is not only a list of development prompts. The intended loop is:

`Discover → Elicit requirements → Baseline PRD/ACs → UX/design → Architecture → Risks/predictions → QE strategy → Approve → Freeze contracts → Scaffold → Slice plan → Implement one slice → Verify → Validate → QE gate → Human acceptance → Next slice`.

### New workflow skills
- `requirements-elicitation`, `requirements-engineering`, `acceptance-criteria`, `requirements-traceability`
- `risk-based-testing`, `test-strategy`, `test-case-design`, `test-automation`
- `verification-validation`, `defect-management`, `chunked-implementation`, `implementation-loop`
- `qe-orchestration`, `release-readiness`, `change-impact-analysis`

### New specialist agents
- Requirements Engineer
- QE Architect
- Test Automation Engineer
- Verification Engineer
- Defect Triage
- Delivery Orchestrator

### New sequential prompts
Prompts `24`–`40` cover requirements elicitation and baselining, traceability, QE strategy, test design, slice planning, test-first implementation, independent verification, user validation, defect triage, slice/phase gates, regression impact, release readiness and workflow status.

### Evidence and templates
See `docs/engineering/DEVELOPMENT-WORKFLOW.md`, `REQUIREMENTS-ENGINEERING.md`, `REQUIREMENTS-TRACEABILITY.md`, `QUALITY-ENGINEERING-STRATEGY.md`, `VERIFICATION-VALIDATION-PLAN.md`, `TEST-PLAN-TEMPLATE.md`, `DEFINITION-OF-READY-DONE.md`, `DELIVERY-SLICE-PLAYBOOK.md`, `DEFECT-MANAGEMENT.md`, `APPROVAL-LOG.md`, `DEFECT-LOG.md` and `REQUIREMENTS-TRACEABILITY.csv`.

Use `WORKFLOW-QUICKSTART.md` as the single flow guide. Start from discovery and do not jump directly to implementation.
