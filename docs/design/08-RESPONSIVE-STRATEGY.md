# Responsive Strategy

**Status:** APPROVED v1 - Phase 07 responsive baseline  
**Version:** v1  
**Date:** 2026-11-23  
**Prerequisites:** `APPROVE UX v1`, `APPROVE IA v1`, `APPROVE VISUAL DIRECTION v1`, `APPROVE WIREFRAMES v1`, `APPROVE DESIGN SYSTEM v1`  
**Approval target:** Included in `APPROVE DESIGN v1`

This document defines when ClipYantra layouts reflow or change capability. It is not a promise to reproduce desktop precision on smaller devices.

## 1. Responsive principles

1. Start from the task and content constraint, not a device stereotype.
2. Preserve source, current object and primary action context.
3. Collapse navigation and panels before removing essential task information.
4. Horizontal overflow is allowed only inside a purposeful timeline, table or calendar region.
5. Tablet supports review and approval; it does not promise full desktop multi-track editing.
6. Mobile supports review, metadata correction, scheduling and monitoring.
7. Touch alternatives are first-class controls, not hidden hover actions.
8. 200% zoom and reflow take priority over showing every column.

## 2. Breakpoint policy

These are task/content breakpoints derived from the approved wireframes and design-system proposals:

| Range | Label | Layout policy |
|---|---|---|
| >= 1280 px | Large desktop | Full application navigation and full management layout |
| 1024-1279 px | Small desktop/laptop | Collapse one non-primary panel; preserve preview/timeline |
| 768-1023 px | Tablet | Compact shell, card/list layouts, one contextual panel |
| <= 767 px | Mobile | Compact navigation, task-first stacked layout |
| <= 390 px | Small mobile | Preserve primary action and object identity; avoid dense secondary controls |

Breakpoints may be adjusted at implementation only through a design change request.

## 3. Shared application shell

### Large desktop >=1280

- left navigation: expanded 240 px;
- top bar: workspace/brand, search, notification and user context;
- primary route content: normal max-width or 12-column layout;
- breadcrumbs and contextual bar remain visible where relevant.

### Small desktop 1024-1279

- left navigation: collapsed 64 px icon rail or 240 px if content permits;
- top bar search remains visible or collapses to a named search action;
- management tables may reduce optional columns;
- Clip Studio preserves center preview and timeline and collapses one side panel.

### Tablet 768-1023

- navigation becomes icon rail or compact drawer;
- table rows become cards or labeled stacked rows;
- search and filters move to a top row or filter drawer;
- dashboard uses one or two columns;
- tablet RQ-4 task support remains explicit.

### Mobile <=767

- navigation uses a menu/drawer;
- page header remains visible with a single primary action;
- secondary actions move to named menu items;
- cards and lists become single-column;
- sticky bottom actions are used only for primary, low-risk tasks.

## 4. Route-specific behavior

| Route family | Large desktop | Laptop | Tablet | Mobile |
|---|---|---|---|---|
| Overview | attention + queue + recent + schedule grid | 2-column summaries | compact cards and primary actions | stacked attention/queue/review |
| Library | grid/list with optional columns | list or grid with filters | card grid and filter drawer | card list and import action |
| Source detail | tabs plus source summary and side context | tabs plus compact summary | tabs, preview and stacked detail | tabs become scrollable named tabs |
| Import | step form/modal | step form with compact side summary | full-width steps | full-width wizard and large controls |
| Processing | stage timeline plus diagnostics | vertical stage detail | vertical stage stepper | one active stage and expandable details |
| Candidates | comparison/list and evidence | 2-column cards | 1-2 column cards, visible review actions | one card at a time or stacked cards |
| Clip Studio | 280 px context + preview + 320 px inspector + timeline | collapsed one context panel, preview/timeline priority | preview + one transcript/inspector panel | preview + review/limited edit controls |
| Exports | grid/list and validation detail | grid plus detail drawer | card list plus detail panel | list and explicit open/publish actions |
| Calendar | month/week plus detail drawer | week/list plus drawer | week/list, no hover-only reschedule | queue/list or day view |
| Social accounts | account cards and permission detail | account cards plus drawer | account cards | stacked account and reconnect actions |
| Published/Analytics | table/cards plus detail | reduced columns, detail drawer | metric cards and post list | metric cards, text definitions and post detail |
| Brand Kit | profile list plus preview | profile list plus preview | profile list and preview tabs | profile list and one preview/asset section |
| AI/Processing settings | provider list plus detail and routing | provider list plus detail drawer | sectioned settings and provider cards | stacked configuration sections |
| Workspace/Audit | settings tabs plus table/history | tabs plus compact history | accordion/section list | section list and filter drawer |

## 5. Clip Studio responsive behavior

### Large desktop >=1280

Composition:

- left context: 280 px;
- center preview: flex;
- right inspector: 320 px;
- bottom timeline: multi-track visible;
- preview remains dominant.

Advanced multi-track timeline operations remain available.

### Laptop 1024-1279

- preserve preview and timeline;
- collapse left transcript/context or right inspector into named tabs/drawers;
- do not hide export or save state;
- timeline scrolling is contained within the timeline viewport;
- numeric edit controls remain visible or in a clearly named editing panel.

### Tablet 768-1023

- show preview and one active context/inspector panel;
- transcript and properties switch by explicit tabs;
- timeline remains accessible for review and simple trims if usability evidence supports it;
- full precision track movement, overlap and B-roll/effects arrangement are not guaranteed;
- approval/rejection and export actions remain primary.

### Mobile <=767

- prioritize preview and simple clip review;
- advanced track editing is limited or explicitly unavailable;
- one panel is visible at a time;
- numeric trim/caption controls may replace timeline dragging;
- export remains available only after validation and with clear platform constraints.

Tablet and mobile UI must explain when full editing is only available on desktop. It must not show disabled controls without a reason.

## 6. RQ-4 tablet behavior

The following experiences are required on tablets:

| Experience | Tablet behavior |
|---|---|
| Dashboard | Card-based attention/queue/recent work with primary actions |
| Video preview | Play/pause, timecode and accessible preview controls |
| Clip review | Evidence, transcript excerpt, source range and accept/reject |
| Approve/reject | Visible decision controls on candidate, export and scheduled-post surfaces |
| Publishing calendar | Week/list/month navigation, open post detail and date/time reschedule fallback |
| Analytics | Available metric cards, metric definitions, refresh time and post/source links |
| Clip Studio | Preview plus one inspector/transcript panel; no full desktop multi-track promise |

Approval/rejection must not be trapped in hover menus or desktop-only shortcuts.

## 7. Overflow behavior

- page-wide horizontal overflow is prohibited;
- timeline overflow is contained to the timeline region;
- data tables use responsive cards or deliberate internal horizontal scrolling;
- calendar events use list/day/weekly collapse rather than squeezing month cells below usability;
- provider capability matrices reflow into labeled rows or accordions;
- inspector fields wrap and use full-width controls in narrow layouts;
- modal/dialog content scrolls without losing close or primary action.

## 8. Panels, navigation and disclosure

- one source of truth controls active panel selection;
- tabs are not visually duplicated with hidden state;
- collapsed panels expose a named open action;
- drawers and dialogs restore focus after close;
- sticky headers include route identity and primary action;
- sticky headers must not consume more than roughly 25% of the viewport on small screens.

## 9. Tables and charts

At narrow widths:

- hide optional columns before hiding core identity/status/action;
- preserve title, platform, state and open action;
- render analytics metrics as labeled cards or vertical rows;
- charts provide a text summary or tabular alternative;
- unavailable platform metrics remain unavailable, not zero or estimated.

## 10. Touch and safe-area behavior

- primary controls use at least 44 x 44 px touch targets;
- timeline and crop handles have an enlarged touch area or numeric alternative;
- bottom sheet/drawer actions respect device safe-area insets;
- drag/drop is never the only reschedule or reorder mechanism;
- press feedback is immediate and non-color-only;
- selected or dragging objects have label/text state.

## 11. Zoom and reflow

- support 200% browser zoom;
- test reflow at 400% zoom-equivalent width;
- preserve visible focus and selected context;
- avoid fixed-height text containers that clip labels;
- wrap long source titles and account names;
- keep primary action and object title visible after reflow.

At any viewport:

- no text is cut off only because of a fixed card height;
- truncation includes an accessible full title or open detail action;
- dialogs and drawers keep internal scrolling and primary actions reachable.

## 12. Required test widths

Test the following CSS pixel widths and representative orientations:

| Width | View | Required checks |
|---|---|---|
| 1440 | Large desktop | full app shell, three-pane Studio, dense timeline |
| 1280 | Large desktop/laptop edge | sidebar and inspector collapse behavior |
| 1024 | Laptop/tablet edge | panel collapse, table overflow and no page overflow |
| 768 | Portrait tablet | RQ-4 flows and management layout |
| 390 | Modern mobile | stacked review, schedule and settings |
| 360 | Small mobile | no clipped primary action or field |

Where tooling permits, test 768 portrait and 1024 landscape tablet orientations.

## 13. Route acceptance matrix

| Route | Acceptance |
|---|---|
| Overview | attention/queue/review remains usable on tablet/mobile |
| Library/Source | object identity, status and open action are preserved |
| Import | source type, rights and profile fields do not clip or hide validation |
| Processing | stages and retry/diagnostic actions remain readable |
| Candidates | evidence and accept/reject remain available |
| Clip Studio | preview/timeline priority and no drag-only edit promise |
| Exports | validation and publish state remain visible |
| Calendar | month/week/list alternatives and explicit date/time control |
| Accounts | OAuth scopes and reconnect status remain understandable |
| Analytics | metric definition and unavailable state remain visible |
| Brand/Settings | provider/brand/policy controls remain labeled and reachable |

## 14. Feature boundary summary

The MVP must state the following boundaries explicitly:

- full multi-track timeline editing is desktop-first;
- tablet supports preview, review, approve/reject, calendar and analytics;
- mobile prioritizes status, review, correction and schedule actions;
- live-stream monitoring remains deferred unless OUT-004 is approved;
- AI dubbing and generated B-roll remain deferred unless OUT-005 is approved.

## 15. Gate status

**Current status:** IN PROGRESS - proposed responsive strategy.  
**Approval target:** Included in `APPROVE DESIGN v1` after interaction, accessibility and visual QA review.
