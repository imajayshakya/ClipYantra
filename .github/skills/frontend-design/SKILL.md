---
name: frontend-design
description: 'Use when designing ClipYantra web application interfaces, high-quality SaaS screens, layouts, dashboards, editor workspaces, component composition or frontend visual implementation.'
argument-hint: '[screen or component to design]'
---

# Frontend Design for ClipYantra

Build product-specific interfaces, not generic admin templates.

Before implementation:
- Read approved screen spec, design tokens, component catalog, interaction states, responsive strategy and accessibility rules.
- Verify the relevant design gate and implementation slice are approved.
- Inspect existing components and installed dependencies.

Design and implementation rules:
- Establish one clear primary task per screen.
- Use typography, alignment, whitespace and grouping to create hierarchy.
- Avoid repetitive cards, decorative gradients, excessive glassmorphism, oversized hero areas and gratuitous badges.
- Keep Clip Studio preview prominent and timeline readable; use collapsible side panels and a contextual inspector.
- Use data tables for comparison/management when they are clearer than cards.
- Show real system state and clear recovery actions.
- Use reusable semantic components and tokens.
- Include keyboard, hover, focus, active, disabled, loading, empty, error and success states.
- Ensure all controls work or clearly explain why they are disabled.
- Test at approved desktop/tablet/mobile viewports.

Do not make unapproved visual-direction or navigation changes. Report when requirements conflict with the approved design.
