# ClipYantra Design System Specification

**Status:** APPROVED v1 - Phase 06 design-system baseline  
**Version:** v1  
**Date:** 2026-11-23  
**Prerequisites:** `APPROVE UX v1`, `APPROVE IA v1`, `APPROVE VISUAL DIRECTION v1`, `APPROVE WIREFRAMES v1`  
**Approval:** `APPROVE DESIGN SYSTEM v1`

This document defines semantic tokens and reusable component contracts. It does not implement components, install dependencies or add application styles.

## 1. Design-system principles

1. Semantic meaning overrides raw hex values or one-off component colors.
2. The approved Direction A palette is the baseline dark theme.
3. One token contract serves management, monitoring and editing density tiers.
4. Status is communicated by icon plus text plus color.
5. Every interactive component has keyboard, focus, hover, active, loading, disabled, error and success behavior.
6. Dense editor controls may differ in layout, not in semantic meaning or accessibility.
7. CSS variables are the implementation boundary; components consume tokens, not raw palette values.

## 2. Approved source documents

- [Design overview](./00-DESIGN-OVERVIEW.md)
- [UX research](./01-UX-RESEARCH.md)
- [Information architecture](./02-INFORMATION-ARCHITECTURE.md)
- [Visual direction](./03-BRAND-VISUAL-DIRECTION.md)
- [Screen specifications](./05-SCREEN-SPECIFICATIONS.md)
- [Interaction and state specification](./06-INTERACTION-AND-STATES.md)
- [Accessibility requirements](./07-ACCESSIBILITY.md)
- [Responsive strategy](./08-RESPONSIVE-STRATEGY.md)

Direction B remains a reference for management-screen exploration. It is not a second implementation theme until explicitly approved.

## 3. Token naming convention

Use semantic names with the `--cy-` prefix:

```text
--cy-{category}-{role}-{variant?}-{state?}
```

Examples:

- `--cy-canvas`
- `--cy-surface-panel`
- `--cy-text-primary`
- `--cy-border-control`
- `--cy-accent-hover`
- `--cy-status-success`
- `--cy-space-4`
- `--cy-radius-panel`
- `--cy-motion-panel`
- `--cy-z-modal`

Components must not consume palette aliases directly. For example, a primary button consumes `--cy-accent` and `--cy-accent-foreground`, not `#4F7CFF`.

## 4. Color tokens

| Semantic token | CSS variable | Value | Role |
|---|---|---|---|
| Canvas | `--cy-canvas` | `#0F1113` | App canvas and main dark inset |
| Panel surface | `--cy-surface-panel` | `#181C1F` | Sidebars, cards, panels and drawers |
| Raised surface | `--cy-surface-raised` | `#1E2327` | Hovered panel, floating panel or elevated surface |
| Divider border | `--cy-border-divider` | `#2A2F34` | Non-interactive dividers |
| Control border | `--cy-border-control` | `#6B737C` | Interactive boundaries and control outlines |
| Strong border | `--cy-border-strong` | `#9AA3AC` | Selected, checked or emphasized boundaries |
| Text primary | `--cy-text-primary` | `#E8EAED` | Headings and primary content |
| Text secondary | `--cy-text-secondary` | `#9AA3AC` | Supporting copy and labels |
| Text muted | `--cy-text-muted` | `#6B737C` | Disabled/decorative metadata only; not normal informational text |
| Accent | `--cy-accent` | `#4F7CFF` | Primary action, active state and focus |
| Accent hover | `--cy-accent-hover` | `#3D6BFF` | Primary action hover |
| Accent foreground | `--cy-accent-foreground` | `#0F1113` | Text/icon on accent fill |
| Success | `--cy-status-success` | `#14B8A6` | Complete, valid or published |
| Warning | `--cy-status-warning` | `#F59E0B` | Attention, queued or review |
| Danger | `--cy-status-danger` | `#EF4444` | Error, failed or destructive |
| Focus ring | `--cy-focus-ring` | `#4F7CFF` | Keyboard focus indicator |

### 4.1 Contrast checks

Calculated against the approved palette:

| Pair | Contrast | Use |
|---|---:|---|
| Text primary on canvas | 15.70:1 | Normal text |
| Text secondary on canvas | 7.40:1 | Supporting text |
| Accent foreground on accent | 5.10:1 | Primary button text/icon |
| Success on canvas | 7.60:1 | Status text/icon |
| Warning on canvas | 8.81:1 | Status text/icon |
| Danger on canvas | 5.03:1 | Status text/icon |
| Text muted on canvas | 3.94:1 | Disabled/decorative text only |
| Control border on canvas | 3.94:1 | UI control boundary |

The visual design does not allow `text-muted` to carry essential labels or error instructions. Status text must include a visible label and icon, not only color.

Non-interactive dividers use `border-divider`; dividers must not substitute for a 3:1 control boundary.

## 5. Typography tokens

Use Inter or a comparable system sans stack for UI text. Use JetBrains Mono, SF Mono or Consolas for timecodes, durations, source offsets and numeric data.

| Role | CSS variable | Size/line height | Weight | Use |
|---|---|---|---|---|
| Display | `--cy-type-display` | 28/36 px | 700 | Rare large workspace title or welcome state |
| H1 | `--cy-type-h1` | 24/32 px | 600 | Page title |
| H2 | `--cy-type-h2` | 20/28 px | 600 | Section title |
| H3 | `--cy-type-h3` | 16/24 px | 600 | Panel title or card title |
| Body | `--cy-type-body` | 14/22 px | 400 | Standard content |
| Small | `--cy-type-small` | 12/18 px | 400/500 | Labels, metadata and table secondary text |
| Micro | `--cy-type-micro` | 11/16 px | 500 | Dense metadata and overlines |
| Numeric | `--cy-type-numeric` | 14/22 px monospace | 500 | Timecodes, durations, counts and costs |

Rules:

- enable tabular numerals for timecodes, durations, metrics and cost values;
- do not use display type inside controls or dense editor tables;
- UI text wraps; timecodes remain single-line;
- Hindi/Devanagari and other multilingual fallbacks are required if multilingual UI enters scope;
- avoid automatic sentence-case changes that alter domain nouns or platform names.

## 6. Spacing and layout tokens

Use a 4 px base grid:

| Token | Value |
|---|---:|
| `--cy-space-0` | 0 px |
| `--cy-space-1` | 4 px |
| `--cy-space-2` | 8 px |
| `--cy-space-3` | 12 px |
| `--cy-space-4` | 16 px |
| `--cy-space-5` | 20 px |
| `--cy-space-6` | 24 px |
| `--cy-space-8` | 32 px |
| `--cy-space-10` | 40 px |
| `--cy-space-12` | 48 px |

Density tiers:

| Tier | Base | Primary surfaces |
|---|---:|---|
| Management | 16 px | dashboard, library, calendar, settings |
| Monitoring | 6 px | processing monitor and operational status |
| Clip Studio | 8 px | preview, timeline and inspector |

Layout values:

- application sidebar: 240 px expanded / 64 px collapsed;
- workspace top bar: 56 px proposed;
- page content gutter: 24 px management / 16 px compact;
- Clip Studio left context: 280 px;
- Clip Studio right inspector: 320 px;
- candidate or detail drawer: 320-400 px depending on content;
- default track height: 48 px;
- compact track height: 32 px.

The top bar and candidate/drawer width values are implementation proposals pending Interaction/Responsive/Accessibility approval. They must not be promoted to approved geometry before that gate.

## 7. Radius, elevation and z-index

| Category | Token | Value |
|---|---|---:|
| Control | `--cy-radius-control` | 4 px |
| Panel | `--cy-radius-panel` | 8 px |
| Modal/drawer | `--cy-radius-overlay` | 12 px |
| Pill | `--cy-radius-pill` | 9999 px |
| Elevation 0 | `--cy-elevation-0` | none |
| Elevation 1 | `--cy-elevation-1` | `0 1px 2px rgba(0,0,0,0.3)` |
| Elevation 2 | `--cy-elevation-2` | `0 4px 8px rgba(0,0,0,0.4)` |
| Elevation 3 | `--cy-elevation-3` | `0 8px 24px rgba(0,0,0,0.5)` |

Z-index proposal:

- base `--cy-z-base`: 0;
- sticky `--cy-z-sticky`: 100;
- dropdown `--cy-z-dropdown`: 1000;
- overlay `--cy-z-overlay`: 1100;
- modal `--cy-z-modal`: 1200;
- toast `--cy-z-toast`: 1500.

Do not use shadows to communicate status. Status remains text/icon/shape plus optional color.

## 8. Motion tokens

| Token | Value | Use |
|---|---|---|
| `--cy-motion-micro` | 120 ms ease-out | buttons, toggles and hover feedback |
| `--cy-motion-panel` | 200 ms ease-out | drawers, panels and short route transitions |
| `--cy-motion-reduced` | 0 ms | required when `prefers-reduced-motion: reduce` |

Motion explains cause/effect; it never delays input or hides a loading state. No animated gradients or attention pulses are part of the design baseline.

## 9. Initial component inventory

| Component family | Core anatomy | Variants or states |
|---|---|---|
| AppShell | sidebar, topbar, brand/workspace context, content region | expanded/collapsed, tablet, mobile |
| Sidebar / Topbar | navigation, workspace switcher, search, notifications, user menu | active, hover, disabled, permission-denied |
| PageHeader | title, context, breadcrumb, primary/secondary actions | loading, empty, error, success |
| Button | label, icon optional, loading indicator | primary, secondary, destructive, ghost, loading, disabled |
| IconButton | icon, accessible name, tooltip optional | default, hover, focus, selected, disabled |
| TextField / TextArea | label, value, help, prefix/suffix, error | default, focus, invalid, disabled, read-only |
| Select / Combobox | label, trigger, option list, selected value | open, selected, invalid, empty, loading |
| Tabs / SegmentedControl | tab list, panel, indicator | active, hover, focus, disabled |
| Dialog / Drawer / Popover | surface, title, close action, content, actions | open, nested, confirm, error, focus-contained |
| Toast / Alert | icon, title, message, action/dismiss | success, warning, error, info, persistent |
| StatusIndicator / Progress | icon, label, measured or indeterminate bar | queued, running, succeeded, failed, cancelled |
| EmptyState / Skeleton | message, icon/visual, primary recovery action | initial, loading, no-data, partial-data |
| DataTable / FilterBar | header, rows, selected state, filter controls | sorted, filtered, loading, empty, permission |
| CandidateCard / ListRow | thumbnail, source range, score, evidence, actions | pending, accepted, rejected, needs-edit |
| ScoreBreakdown | score label, category weights, uncertainty | complete, partial, unavailable |
| ProcessingStepper / JobLog | stage list, current stage, diagnostics disclosure | queued, running, retrying, failed, succeeded |
| VideoPlayer / Transport | preview, playhead, timecode, controls | loading, ready, paused, playing, error |
| TimelineRuler / TrackLane | ruler, track label, clips, playhead | collapsed, expanded, zoomed, keyboard-selected |
| ClipBlock / CaptionCue | time range, label, handles, selected state | default, selected, drag, trim, invalid |
| Playhead / CropOverlay | position, safe zone, transform handles | dragging, keyboard-moving, invalid, hidden |
| CaptionCue / TranscriptSegment | text, source timing, speaker/label | editable, selected, out-of-sync, invalid |
| CalendarGrid / ScheduledPostCard | date, event, platform, status, actions | month/week/day/list, drag, approval, reconciliation |
| ChannelBadge | platform icon, account name, status | connected, degraded, expired, disconnected |
| AnalyticsMetric / ChartPanel | label, value, definition, refresh time | available, unavailable, loading, partial |

The component foundation must be chosen in the implementation-gated phase. No package or primitive library is selected by this design-system document.

## 10. Component documentation contract

Every component added during implementation must document:

1. purpose and supported screen contexts;
2. anatomy and required/optional parts;
3. variants and size/density behavior;
4. default, hover, active, selected, focus, loading, disabled, error and success states;
5. keyboard behavior and accessible name;
6. content rules and overflow behavior;
7. responsive and touch behavior;
8. related tokens and component dependencies;
9. test and visual-QA evidence.

## 11. State vocabulary

Use existing state names consistently:

- source: created, uploading, validating, ready, rejected, failed, archived;
- job: queued, running, waiting_for_input, retrying, succeeded, failed, cancelled;
- candidate: pending_review, accepted, rejected, needs_edit;
- draft: editing, saving, saved, save_failed, conflict;
- render: queued, rendering, validating, ready, failed;
- post: draft, awaiting_approval, scheduled, uploading, processing, published, failed, unknown_reconciliation, cancelled.

State components must use labels and icons. Color is only a supporting cue.

## 12. Existing dependency assessment

Repository discovery found no package manifest or frontend source in the current workspace. The proposed application stack is Next.js, React, TypeScript and Tailwind, but no implementation dependencies are currently established.

At implementation design freeze, evaluate:

- Radix Primitives for accessible primitive behavior;
- shadcn/ui only as a generated copy/customization approach, not as a package assumption;
- Headless UI only if it better matches the selected framework;
- Lucide or Phosphor for icons, subject to bundle, license and maintenance review.

Do not add multiple overlapping primitive or icon libraries. No package is approved or installed by this design-system baseline.

## 13. CSS variable plan

Tokens should be declared centrally at theme root and consumed through semantic variables:

```css
:root {
  --cy-canvas: #0F1113;
  --cy-surface-panel: #181C1F;
  --cy-surface-raised: #1E2327;
  --cy-border-divider: #2A2F34;
  --cy-border-control: #6B737C;
  --cy-text-primary: #E8EAED;
  --cy-text-secondary: #9AA3AC;
  --cy-text-muted: #6B737C;
  --cy-accent: #4F7CFF;
  --cy-accent-hover: #3D6BFF;
  --cy-accent-foreground: #0F1113;
  --cy-status-success: #14B8A6;
  --cy-status-warning: #F59E0B;
  --cy-status-danger: #EF4444;
  --cy-focus-ring: #4F7CFF;
}
```

Implementation conventions:

- theme selection sets semantic token variables, not raw component overrides;
- density attributes set spacing/timeline values rather than duplicating page-specific CSS;
- status components consume status tokens plus text/icon;
- Tailwind or CSS modules may map to variables but must not duplicate raw hex values;
- future light theme work requires explicit theme parity and contrast verification.

## 14. Icon, media and status rules

- icon size defaults: 16 px compact, 20 px standard, 24 px prominent;
- icon stroke or fill must remain legible at 16 px;
- do not use emoji as interface status icons;
- status icon plus text is required for success, warning and error;
- thumbnails and informative charts require text alternatives;
- decorative imagery uses empty alternative text;
- platform icons remain official or licensed marks and must not imply account connection before OAuth success;
- generated logos and exports must preserve contrast and safe clear space.

## 15. Accessibility contract

- target WCAG 2.2 AA as an engineering objective;
- maintain visible 2 px focus indication using `--cy-focus-ring`;
- do not rely on focus color alone;
- preserve 200% zoom and supported viewport reflow;
- provide 44 px touch targets for primary tablet actions where appropriate;
- provide numeric alternatives to drag-only timeline controls;
- use live regions for progress without excessive repeated announcements;
- respect `prefers-reduced-motion`;
- verify automated and manual keyboard behavior in the next interaction/accessibility and visual-QA gates.

## 16. Responsive density plan

The proposed visual QA widths remain 1440, 1280, 1024, 768, 390 and 360 px. Exact breakpoints require Interaction/Responsive/Accessibility approval.

- desktop >=1280: full management and Clip Studio layouts;
- laptop 1024-1279: collapse one Clip Studio side panel and preserve preview/timeline;
- tablet 768-1023: management cards, clip review, approval and calendar; no full desktop multi-track promise;
- mobile <=767: status, review, metadata, approval and calendar; advanced editor controls require progressive disclosure.

## 17. Traceability

| Requirement | Design-system evidence |
|---|---|
| FR-021, FR-026, FR-027 | Timeline, caption, transport and versioned-state component contracts |
| FR-028 | AI edit proposal components use typed preview and approval states |
| FR-032 to FR-036 | Channel badges, OAuth, calendar and reconciliation component states |
| FR-050 | Provider capability and routing component content/selection states |
| FR-051, NFR-006 | Processing stepper, status indicator and progress semantics |
| FR-052, FR-053 | Workspace context, brand, policy and audit component contracts |
| NFR-004, NFR-007 | No credential rendering and explicit validation states |
| RQ-4 | Tablet density and touch behavior |
| NFR-010 | Component, keyboard, responsive and visual test hooks |

## 18. Design-system approval checklist

- [ ] Semantic tokens cover canvas, surface, text, border, accent and status roles.
- [ ] Density tiers are explicit for management, monitoring and editing.
- [ ] Typography and numeric/tabular rules are defined.
- [ ] Radius, elevation, motion and z-index are bounded.
- [ ] Component inventory has anatomy, variants and state coverage.
- [ ] No component or package implementation is included.
- [ ] Dependency options are evaluated without adding overlapping libraries.
- [ ] Contrast limitations and required verification are explicit.
- [ ] RQ-4 tablet boundaries remain consistent with approved wireframes.
- [ ] Requirement/design traceability is included.

## 19. Gate status

**Current status:** APPROVED v1 - `APPROVE DESIGN SYSTEM v1` received.  
**Next phase:** Interaction, Responsive and Accessibility baseline.
