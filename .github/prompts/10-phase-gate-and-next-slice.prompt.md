# Phase 10 — Phase Gate and Next Slice Decision

Use `phase-release-readiness`.

Review the completed slice or milestone against approved acceptance criteria. Confirm test evidence and any independent review findings. Check architecture drift, security, migrations, docs, unresolved risks and skipped tests.

Set status:
- PASS: required criteria met with evidence.
- BLOCKED: required capability/test/permission is missing.
- NEEDS APPROVAL: owner decision required.

If PASS, propose the next smallest slice and its acceptance criteria. Do not start it. Require explicit `APPROVE SLICE <ID>`. If blocked, list the precise remediation. Update phase status only with evidence.


Global rules: Follow `.github/copilot-instructions.md` and the relevant skills. Inspect existing repository state before edits. Do not invent API/model facts. Keep the scope of this prompt only. Do not advance to the next phase automatically. End with a gate report and explicit status.
