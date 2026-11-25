# Full Design Approval Package

**Status:** APPROVED v1 - full design approval  
**Version:** v1  
**Date:** 2026-11-23  
**Prerequisites:** Discovery, Requirements Review, UX, IA, Visual Direction, Wireframes, Design System and Architecture approvals/evidence  
**Approval:** `APPROVE DESIGN v1`

This package audits the design and architecture artifacts for freeze readiness. It does not implement frontend code or infer approval.

## 1. Audit result

**Result:** APPROVED BY PRODUCT OWNER.

The product-owner decisions and core design artifacts are present. The explicit `APPROVE DESIGN v1` token resolves the full-design gate; acceptance coverage and implementation visual-QA evidence remain contract/slice exit criteria, not reasons to retroactively deny the design approval.

## 2. Artifact status

| Artifact | Status | Evidence | Freeze result |
|---|---|---|---|
| Repository discovery | APPROVED | Discovery approval and repository evidence | Ready |
| Product requirements | APPROVED v1 | `APPROVE REQUIREMENTS v1`, `APPROVE REQUIREMENTS REVIEW v1` | Partially ready; AC gaps remain |
| UX research | APPROVED | 01-UX-RESEARCH.md | Ready as approved baseline |
| Information architecture | APPROVED | 02-INFORMATION-ARCHITECTURE.md | Ready |
| Visual direction | APPROVED | 03-BRAND-VISUAL-DIRECTION.md | Direction A frozen as primary |
| Screen specifications | APPROVED | 05-SCREEN-SPECIFICATIONS.md | Ready for design freeze |
| Design system | APPROVED | 04-DESIGN-SYSTEM.md | Ready for design freeze |
| Interaction states | APPROVED v1 | 06-INTERACTION-AND-STATES.md | Freeze in contracts |
| Accessibility | APPROVED v1 | 07-ACCESSIBILITY.md | Freeze acceptance and evidence plan |
| Responsive strategy | APPROVED v1 | 08-RESPONSIVE-STRATEGY.md | Freeze viewport and capability plan |
| Visual QA | APPROVED plan | 09-VISUAL-QA.md | Evidence to be produced during implementation |
| Architecture | APPROVED | 02-ARCHITECTURE.md and APPROVE ARCHITECTURE v1 | Ready for full design review |
| Risks | IN PROGRESS | 15-RISKS-AND-PREDICTIONS.md and engineering/RISKS.md | Residual risks documented |

## 3. Screen inventory coverage

The approved wireframe inventory covers:

| Route family | User task | Approval state |
|---|---|---|
| Overview | Identify attention and next action | Approved wireframe |
| Library and source detail | Find, inspect and resume work | Approved wireframe |
| Import | Add source with rights and profile | Approved wireframe |
| Processing monitor | Recover from stages and providers | Approved wireframe |
| Candidate discovery | Review evidence and accept/reject | Approved wireframe |
| Clip Studio | Preview, transcript, timeline and inspector | Approved wireframe |
| Exports | Validate and prepare publishing | Approved wireframe |
| Publishing calendar | Schedule, approve and reconcile | Approved wireframe |
| Social accounts | OAuth connection and permissions | Approved wireframe |
| Published and analytics | Review real results and metrics | Approved wireframe |
| Brand Kit | Configure reusable brand assets | Approved wireframe |
| AI and processing settings | Configure provider/capability/routing | Approved wireframe |
| Workspace/policies/audit | Workspace, brand and publishing controls | Approved wireframe |

The live route list includes source detail tabs and scheduled-post detail for deeper navigation.

## 4. Primary flow coverage

| Flow | Approved design coverage | Remaining validation |
|---|---|---|
| Import to candidates | Wireframe, states, rights, routing and failure/recovery | Test fixture and real provider evidence |
| Candidate to Studio | Wireframe, draft, transcript, timeline and inspector | Prototype or implementation usability evidence |
| Studio to export | Wireframe, versioning, QA and state | Render fixture, visual and keyboard evidence |
| Export to publish | Calendar, accounts, metadata and reconciliation | OAuth/test-account evidence |
| Workspace/brand | Settings, routing, policies and audit | Permission/role and workspace isolation evidence |

## 5. Token and component completeness

The design system defines:

- semantic canvas, surface, text, border, accent and status tokens;
- 4 px spacing scale;
- management/monitoring/edit density tiers;
- typography and tabular numerals;
- radius/elevation/motion/z-index;
- initial component inventory;
- common component anatomy and states;
- keyboard/focus and responsive contracts;
- CSS-variable mapping proposal.

Remaining implementation decisions:

- no UI primitive library is selected;
- no frontend package manifest exists;
- no final component library screenshot exists;
- final CSS values must preserve semantic tokens;
- topbar and drawer dimensions remain proposals until implementation evidence or a design change.

## 6. Accessibility and responsive risks

| Risk | Status | Required evidence |
|---|---|---|
| Color contrast | Direction A contrast pair calculations documented | Recheck actual CSS states and overlays |
| Text-muted use | Restricted to disabled/decorative metadata | Component audit |
| Clip Studio keyboard | Numeric/non-drag alternatives specified | Manual keyboard walkthrough |
| Timeline screen-reader semantics | Tracks/clips/playhead requirements specified | Assistive-tech spot check |
| Dialog/drawer focus | Contract specified | Component focus tests |
| Live status | Announcements specified | Screen-reader and noisy-status tests |
| 200% zoom/reflow | Required strategy defined | Browser screenshot/zoom evidence |
| Tablet RQ-4 | Required behaviors specified | Tablet usability walkthrough |
| 360/390/768/1024/1280/1440 | Test matrix specified | Actual screenshots and visual baseline |

No WCAG conformance claim may be made before evidence in 09-VISUAL-QA.md.

## 7. Clip Studio usability risks

The Clip Studio is the largest design/implementation risk:

- preview, transcript and timeline source mappings must remain synchronized;
- source and clip-relative time ranges must be visually and semantically distinct;
- drag-only trim/split/move controls are prohibited as the sole method;
- AI edit operations must be previewed and reversible;
- save/conflict state must remain usable under keyboard and touch;
- timeline accessibility is not a visual-only component;
- B-roll fail-soft behavior must not hide the warning;
- technical validation must block publish eligibility.

Representative validation fixtures:

- simple podcast;
- two-speaker interview;
- screen tutorial;
- fast-motion gaming clip.

## 8. Decisions proposed for freeze

| Decision | Proposed freeze value |
|---|---|
| Visual direction | Direction A - Calm Creator Workstation |
| App shell | Stable left nav/top bar/workspace context |
| Clip Studio | Preview + timeline + left context + right inspector |
| Density | Management spacious, monitoring compact, Studio dense |
| Theme | Dark Direction A only for MVP; no unapproved light theme |
| Tablet | Dashboard/preview/review/approval/calendar/analytics; no full timeline parity |
| Provider routing | Workspace -> profile -> per-job; local/balanced/cloud/user-selected |
| Publishing | Meta and YouTube official OAuth adapters; reconciliation and idempotency |
| State model | Draft/candidate/draft/render/post state vocabulary consistent across UI |
| Deferred scope | OUT-004 live-stream monitor and OUT-005 dubbing/generated B-roll |

These freeze values require the explicit `APPROVE DESIGN v1` token.

## 9. Blockers and unresolved items

### 9.1 Acceptance coverage blocker

The live requirements matrix contains 69 requirement rows, but only 24 acceptance-criteria records in the baseline database. FR-028 and NFR-010 are explicitly unmapped, and many other requirements have no acceptance criterion or test linkage.

Examples of gaps:

- FR-028 operation schema and fallback behavior;
- NFR-010 measurable test coverage targets;
- provider fallback thresholds;
- exact supported input formats and size/duration limits;
- tablet usability thresholds;
- publish platform eligibility test threshold;
- benchmark thresholds for cost, latency and memory.

This does not permit the design package to self-approve acceptance completeness.

### 9.2 Evidence blockers

- no implementation screenshots or visual baselines exist;
- no actual browser accessibility scan exists;
- no actual keyboard-only walkthrough evidence exists;
- no 360/390/768/1024/1280/1440 screenshot set exists;
- no hardware benchmark exists for Vega 8 or Docker resource limits;
- no official provider/platform app review evidence exists;
- no contract freeze exists.

These are planned validation evidence, not claims of completion.

### 9.3 Scope conflicts

- OUT-004 live-stream monitor remains outside MVP.
- OUT-005 dubbing/generated B-roll remains outside MVP.
- Per-brand provider routing remains deferred.
- Square output is optional and not promised.

No implicit extension of scope is approved.

## 10. Required implementation visual QA evidence

The first UI slice must produce:

- desktop screenshot at 1440 and 1280;
- tablet screenshot at 768;
- mobile screenshot at 390 and 360;
- 200% zoom/reflow evidence where applicable;
- keyboard focus and dialog evidence;
- axe or equivalent automated scan report;
- manual keyboard walkthrough notes;
- reduced-motion behavior;
- empty/loading/error/disabled/success state evidence;
- actual representative media, not fabricated analytics or fake progress.

## 11. Approval gate

**Current status:** APPROVED v1 - `APPROVE DESIGN v1` received.

Remaining work:

1. Contract freeze for schemas, state machines, APIs, events and side-effect semantics.
2. Placeholder scaffold only after `APPROVE CONTRACTS v1`.
3. Acceptance criteria and implementation visual-QA evidence remain slice/phase exit evidence.
