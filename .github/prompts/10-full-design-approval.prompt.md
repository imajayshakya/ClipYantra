---
name: full-design-approval
description: 'Audit all ClipYantra product design artifacts and prepare an explicit human visual-design approval package.'
agent: design-system-architect
---

Use `design-handoff`, `visual-design-system`, `accessibility-audit` and `video-editor-ux`.

Audit PRD, UX research, information architecture, brand directions, screen specifications, tokens, component catalog, interaction states, responsive strategy and accessibility requirements.

Return:
1. Approved/proposed artifact status.
2. Unresolved contradictions and assumptions.
3. Screen inventory and user-flow coverage.
4. Design token/component completeness.
5. Accessibility and responsive risks.
6. Clip Studio usability risks.
7. Exact visual direction and design decisions to freeze.
8. Required design QA evidence during implementation.

Do not self-approve. Do not implement frontend code. Mark `PASS TO REQUEST APPROVAL` only if complete. The final status remains `NEEDS APPROVAL` until the product owner explicitly replies `APPROVE DESIGN v1`.
