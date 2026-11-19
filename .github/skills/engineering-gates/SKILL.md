---
name: engineering-gates
description: "Enforce the project's gated engineering workflow from discovery through explicit design approval, scaffold, one-slice implementation, testing and phase approval."
argument-hint: "[phase, feature, or slice ID]"
---

# Engineering Gates

Use this skill whenever starting a new project phase, feature, refactor or implementation request.

## Non-negotiable stage order
1. Discovery: inspect repo, `git status`, relevant files, test commands, existing deployment and dependencies. Read-only.
2. Requirements: write functional/non-functional requirements, user journeys, exclusions, assumptions and acceptance criteria. No application code.
3. Design: write architecture, component boundaries, sequence/data flows, API contracts at a conceptual level, security/privacy, storage and deployment decisions. No application code.
4. Outcomes and risks: state likely outcomes as hypotheses, not promises. Provide assumptions, confidence, unknowns, risks, cost/latency drivers and experiments. No invented benchmark numbers.
5. Design gate: summarize unresolved decisions and ask for explicit `APPROVE DESIGN vN`. Stop.
6. Contracts: after approval, define DB/API/event/provider contracts and ADRs. No implementation code unless the user explicitly approves contracts and scaffold together.
7. Scaffold: create folder/module placeholders, configs, type shells and health checks only. No business logic, fake API behavior or pretend integrations.
8. Slice plan: divide into vertical slices with exact scope, files, dependencies, test plan and rollback.
9. Implementation: implement one slice only after `APPROVE SLICE <ID>`.
10. Verification: run checks and an independent review. Report exact command output/evidence.
11. Phase gate: request approval before the next slice/phase.

## Stop conditions
Stop and ask for approval when requirements conflict, architecture changes materially, external service costs/permissions are unclear, a destructive migration is proposed, production secrets or account scopes are involved, or a test is unavailable.

## Gate report
Include stage, artifact links/paths, decisions, open questions, blockers, tests/evidence, deviations, and exact approval phrase required. Never treat a plan as permission to edit files.
