---
name: placeholder-scaffold
description: Create only the approved project skeleton after contracts are frozen.
agent: implementer
---

Proceed only when explicit `APPROVE CONTRACTS v1` and `APPROVE SCAFFOLD v1` are present.

Before changes inspect git status, branch, conventions and current files. Create only approved folders, empty modules/interfaces, validated settings skeleton, health checks, migration skeleton, Docker/CI skeleton and README updates.

No real business logic, external API calls, provider calls, video rendering, fake data or success-returning placeholders. Stubs must raise `NotImplementedError` or be explicitly disabled. Do not add dependencies unless approved. Run only relevant scaffold checks. Report exact diff and request next slice approval.
