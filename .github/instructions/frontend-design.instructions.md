---
name: frontend-design
description: 'Apply approved ClipYantra design-system, UX, accessibility and responsive rules when editing frontend components and styles.'
applyTo: 'frontend/**/*.{ts,tsx,js,jsx,css,scss}'
---

# Frontend design instructions

- Read `docs/design/00-DESIGN-OVERVIEW.md`, `04-DESIGN-SYSTEM.md`, the relevant screen specification and interaction-state spec before editing UI.
- Check design approval status in `docs/design/10-DESIGN-DECISIONS.md` and `docs/engineering/PHASE-STATUS.md`.
- Do not implement an unapproved design direction or create new page structure ad hoc.
- Use semantic CSS variables/design tokens and approved reusable components. Avoid raw hex colors and arbitrary one-off spacing values in page components.
- Match the approved information hierarchy and screen layout. Do not add decorative cards or charts without user value.
- Implement all applicable loading, empty, error, success, disabled and permission states.
- Provide keyboard-accessible controls, visible focus, semantic HTML, accessible names and non-color status cues.
- Support reduced motion and responsive layouts defined by the approved responsive strategy.
- Use realistic fixture data clearly labelled as fixture/sample; never present it as live analytics.
- Run unit/component tests and the visual QA procedure. Capture screenshots at the agreed desktop/tablet/mobile viewports when tooling is available.
- Report deviations and do not silently alter design tokens or reusable component contracts.
