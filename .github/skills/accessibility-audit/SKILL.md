---
name: accessibility-audit
description: 'Use when designing, implementing or reviewing ClipYantra accessibility: semantic HTML, keyboard navigation, focus, forms, contrast, zoom/reflow, reduced motion, video captions and editor controls.'
argument-hint: '[route, component or workflow]'
---

# Accessibility Audit

Target WCAG 2.2 AA as an engineering objective; do not claim conformance without evidence.

Review semantic structure, labels, focus order, keyboard operations, visible focus, dialog focus, contrast, errors, live status, zoom/reflow, target size, reduced motion, captions and screen-reader semantics.

Clip Studio-specific: timeline clips and tracks need accessible names/time ranges; playhead and selected clip state must be conveyed; trim and timing must have numeric alternatives to dragging; caption cues must be keyboard editable.

Use automated scans plus manual keyboard walkthroughs and screen-reader spot checks. Report severity, route/component, reproduction, evidence and remediation. Do not silently waive failures.
