# ClipYantra Development Workflow

## Purpose
This document defines the required end-to-end flow for AI-assisted development. Copilot and other coding agents are contributors, not product owners or approval authorities. The human owner approves baselines and gates.

## Lifecycle

| Stage | Inputs | Required outputs | Gate |
|---|---|---|---|
| 0. Discovery | Existing repository/context | Repository assessment, constraints, baseline | APPROVE DISCOVERY |
| 1. Elicitation | Goals, stakeholders | Elicitation log, personas/JTBD, workflows, open questions | Validate elicitation |
| 2. Requirements | Validated needs | PRD, FR/NFR/CON/OUT IDs, ACs, priorities | APPROVE REQUIREMENTS |
| 3. UX/design | Requirements | Journeys, IA, visual options, wireframes, tokens, interaction states, accessibility | UX/design approvals |
| 4. Architecture | Requirements + design | C4 views, data flows, ADRs, data model, APIs/events | APPROVE ARCHITECTURE |
| 5. Risk + prediction | Baselines and technical evidence | Risk register, cost/latency/GPU hypotheses, experiments | Accept risks/assumptions |
| 6. QE planning | Requirements + architecture | Test strategy, test plan, traceability, environments/data | APPROVE QE PLAN |
| 7. Contract freeze | Approved architecture | API/schema/state/event contracts | APPROVE CONTRACTS |
| 8. Scaffold | Frozen contracts | Empty modules, interfaces, build/health checks | APPROVE SCAFFOLD |
| 9. Slice planning | Approved backlog | Small vertical slices and test designs | APPROVE SLICE |
| 10. Implementation | One approved slice | Minimal code + tests | Review required |
| 11. Verification | Built slice | AC evidence, test results, defect report | Slice QE gate |
| 12. Validation | Working increment | UAT/user outcome evidence | ACCEPT SLICE |
| 13. Phase/release | Accepted slices | Phase report, release checklist, rollback | APPROVE PHASE/RELEASE |

## Standard slice loop
1. Confirm requirement IDs and acceptance criteria.
2. Check Git state and current approved documents.
3. Prepare implementation plan and test cases.
4. Get slice approval.
5. Implement one small vertical slice.
6. Run focused tests and static checks.
7. Run integration/contract/E2E tests relevant to the slice.
8. Have an independent reviewer verify the diff and evidence.
9. Fix defects and rerun impacted tests.
10. Update traceability, defect log, changelog and phase status.
11. Present evidence and ask for human acceptance.
12. Start next slice only after acceptance.

## Rules
- One slice in progress at a time unless explicitly approved otherwise.
- No phase skipping.
- No silent requirement/design/contract changes.
- Not-run is not pass.
- Mocked external calls do not prove live integration.
- AI-generated code must be reviewed and tested like human-written code.
- Keep an audit trail of approvals in `docs/engineering/APPROVAL-LOG.md`.
