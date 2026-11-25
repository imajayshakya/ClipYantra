# ClipYantra AI-Assisted Development — Quick Start

## The control loop
**Discover → Elicit → Specify → Design → Architect → Predict Risks → Plan QE → Approve → Freeze Contracts → Scaffold → Plan Slice → Implement → Verify → Validate → Accept → Next Slice → Release.**

## First prompts
1. `/00-project-discovery` — read-only repository inspection.
2. `/24-requirements-elicitation` — stakeholder needs and open questions.
3. `/25-requirements-baseline` — PRD, stable IDs and measurable ACs.
4. `/02-ux-research` and `/03-information-architecture` — user experience.
5. `/04-brand-visual-directions` through `/07-interaction-responsive-accessibility` — visual design.
6. `/08-architecture-design` and `/09-risk-prediction` — technical design and hypotheses.
7. `/27-qe-strategy` and `/28-test-design` — QE plan and tests.
8. `/10-full-design-approval` plus explicit requirements/architecture/QE approvals.
9. `/11-contracts-freeze`, `/12-placeholder-scaffold`.
10. `/29-slice-breakdown`, then `/30-test-first-implementation` for one approved slice.
11. `/31-slice-verification`, `/32-user-validation-uat`, `/34-slice-qe-gate`.
12. Human `ACCEPT SLICE <ID>`, then plan the next slice.

## Approval is not optional
A prompt completing does not approve its output. Only the human owner can approve baselines, slices, phases or releases. Use the approval tokens in `.github/copilot-instructions.md`.

## QE statuses
- `PASS`: required checks executed and evidence inspected.
- `FAIL`: one or more required checks failed.
- `NOT RUN`: not executed; never treat as pass.
- `BLOCKED`: environment/dependency/evidence prevents a reliable conclusion.
- `NEEDS APPROVAL`: evidence ready but human decision required.

## At the end of each slice
Update traceability CSV, defect log, risk register, changelog and phase status. Report exact commands, exit codes and artifacts.
