---
name: implement-approved-slice
description: Implement one explicitly approved ClipYantra vertical slice.
agent: implementer
---

Implement only the slice whose exact ID has been explicitly approved in this conversation.

Before editing: inspect git status, recent commits, files and tests. Verify slice requirements and contract version. Make the smallest coherent change. Add tests for success, failure, validation and idempotency where relevant. Do not touch unrelated modules. Do not silently add providers/dependencies or change contracts. Do not claim unrun tests passed.

After implementation: run formatter/linter/type checker and focused tests; report exact commands, exit codes and summary. Update changelog and phase status with evidence. Do not start the next slice. Request independent review.
