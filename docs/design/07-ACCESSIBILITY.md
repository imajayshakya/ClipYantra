# Accessibility Requirements

**Status:** APPROVED v1 - Phase 07 accessibility baseline  
**Version:** v1  
**Date:** 2026-11-23  
**Prerequisites:** `APPROVE UX v1`, `APPROVE IA v1`, `APPROVE VISUAL DIRECTION v1`, `APPROVE WIREFRAMES v1`, `APPROVE DESIGN SYSTEM v1`  
**Engineering objective:** WCAG 2.2 AA  
**Conformance claim:** Not permitted until automated, manual and assistive-technology evidence is recorded

Accessibility is a design and implementation requirement, not a final audit-only activity.

## 1. Scope

This baseline applies to:

- application shell and primary navigation;
- import, library, source detail and processing states;
- candidate discovery and approval;
- Clip Studio, transcript and timeline;
- exports and publishing calendar;
- social accounts and OAuth states;
- published post analytics;
- Brand Kit;
- AI/provider and workspace settings;
- dialogs, drawers, menus, toasts and audit views.

The self-hosted MVP is desktop-first for editing, but management review and RQ-4 tablet workflows remain accessible.

## 2. WCAG 2.2 AA baseline

The implementation must satisfy applicable WCAG 2.2 AA success criteria, including:

- programmatic names and roles;
- keyboard operation;
- focus visibility and focus not obscured;
- target size;
- focus order;
- meaningful sequence;
- labels and instructions;
- error identification and suggestion;
- status messages;
- text alternatives;
- contrast and non-text contrast;
- reflow at 400% zoom-equivalent width;
- reduced motion;
- no keyboard traps;
- drag and motion alternatives;
- consistent navigation and identification.

WCAG 2.2 AA conformance is not inferred from a single automated scan.

## 3. Semantic structure

- use landmarks for navigation, main content, search and status regions;
- maintain a logical heading hierarchy within each route;
- use native buttons for actions and native links for navigation;
- use list/table semantics for repeated records;
- use `aria-current="page"` or equivalent for active navigation;
- use field labels, legends and descriptions rather than placeholder-only labels;
- use one main heading for the primary page task;
- avoid using heading elements solely to enlarge visual text.

For tables and complex charts:

- provide a header for each column;
- associate cells with headers;
- offer an accessible summary or text data alternative;
- do not communicate chart meaning by color alone.

## 4. Focus management

### 4.1 Keyboard focus

- visible focus uses `--cy-focus-ring` and remains at least 2 px where possible;
- focus is never hidden beneath sticky headers or overlay surfaces;
- focus order follows visible task hierarchy;
- no positive `tabindex` is used;
- custom widgets implement the required ARIA pattern and native keyboard behavior;
- keyboard focus is not placed on a static element unless it communicates a state or screen-reader context.

### 4.2 Dialogs and drawers

- opening a dialog moves focus to a title or logical first control;
- focus remains inside the modal surface;
- Escape closes only if no unresolved unsaved or destructive action would be lost;
- closing restores focus to the trigger;
- route-change navigation announces new context;
- nested drawers are avoided unless they preserve a clear focus and navigation path.

### 4.3 After state changes

When a state change removes or replaces the triggering control:

- move focus to the next logical control or page heading;
- announce success, validation or recovery in a suitable live region;
- do not reset focus to the top of the page after every autosave;
- preserve focus within inline editing fields after updates.

## 5. Keyboard and input behavior

- every control operates with keyboard and, where applicable, touch;
- Enter/Space activation follows native control semantics;
- arrow-key behavior is context-specific and visible where discoverable;
- shortcut combinations do not fire while text fields are focused unless explicitly intended;
- numeric timecode controls exist as alternatives to drag handles;
- list, table and calendar selection is keyboard reachable;
- menus support arrow keys, Enter/Space and Escape;
- sortable and filterable controls expose state and result count.

## 6. Clip Studio accessibility

### 6.1 Preview and transport

- preview controls have accessible names;
- play/pause state is exposed;
- current and total time is available in accessible text;
- left/right frame controls and five-second controls are available;
- keyboard playback shortcuts do not conflict with text editing;
- the preview may expose a descriptive transcript or caption context.

### 6.2 Timeline

- tracks have accessible names and states;
- clips/cues have accessible names including track, label and source time range;
- selected clip/cue state is programmatically exposed;
- playhead position and movement are announced meaningfully;
- timeline changes are focusable and undoable;
- tracks and clips do not depend on pointer hover;
- zoom controls are keyboard operable;
- horizontal timeline overflow occurs only inside the timeline region.

### 6.3 Trim, split and move

The following alternatives are required:

- numeric in/out timecode fields;
- trim start/end controls;
- split at playhead action;
- caption cue timing fields;
- source-relative caption/trim validation;
- move and reorder controls with keyboard or numeric options;
- before/after preview and operation summary;
- undo/redo after apply.

Dragging may accelerate editing but is not the only operation method.

### 6.4 Captions and transcript

- transcript segments expose source time and speaker labels when available;
- caption text can be edited with a keyboard;
- timing can be adjusted numerically;
- out-of-sync and invalid caption cues show text/icon errors;
- safe-area/crop preview has a non-color text description;
- screen reader users receive cue selection and timing context.

### 6.5 AI edit flow

- operation proposal is announced or placed in a readable focus context;
- operation type and parameters are in plain text;
- before/after impact is programmatically and visually identifiable;
- accept, modify and reject actions are named;
- applying a proposal moves focus to a result or undoable edit state;
- unsupported operations show an accessible error and manual alternatives.

## 7. Status and live announcements

Use live regions only when a state change is useful to an assistive-technology user.

- page-level route changes: polite page/title announcement;
- save state: concise polite announcement for saving/saved/save_failed/conflict;
- processing stages: announce stage completion and failure, not every frame or percentage;
- validation errors: assertive or prompt when submission fails;
- reconciliation: persistent visible status plus polite status-region update;
- publish success: confirmed external result plus visible status.

Avoid repeated announcements for playhead movement, scrub position or hover state. The current timecode can be available on focus or through a dedicated control.

## 8. Labels and validation

- every form field has a visible label and programmatic name;
- placeholder text is not the label;
- required fields are identified in text and semantics;
- error text explains what failed and how to correct it;
- invalid fields use `aria-invalid` or the component framework equivalent;
- the error summary identifies affected fields and can move focus;
- success and warning text is not color-only;
- account permissions and provider capabilities use plain-language labels.

## 9. Contrast and non-text contrast

The approved Direction A design-system contrast target is WCAG 2.2 AA:

| Pair | Contrast | Requirement |
|---|---:|---|
| Text primary on canvas | 15.70:1 | Pass normal text |
| Text secondary on canvas | 7.40:1 | Pass normal text |
| Accent foreground on accent | 5.10:1 | Pass normal text |
| Success on canvas | 7.60:1 | Pass status text/icon |
| Warning on canvas | 8.81:1 | Pass status text/icon |
| Danger on canvas | 5.03:1 | Pass status text/icon |
| Control border on canvas | 3.94:1 | Pass UI boundary target |

Rules:

- do not use text-muted for essential labels or instructions;
- text-muted is only disabled/decorative metadata;
- status meaning always includes icon plus text;
- control boundaries and focus indicators meet 3:1 against adjacent surfaces;
- hover and selected states have both visual and semantic/state cues;
- contrast must be rechecked after actual CSS, blur, transparency and state combinations are implemented.

## 10. Target size and touch

For tablet and mobile:

- primary actions use at least a 44 x 44 px touch target;
- dense desktop controls may use a minimum 24 x 24 px target where spacing prevents overlap;
- 8 px or more separation is preferred between adjacent touch targets;
- timeline handles have a larger touch area or numeric alternative;
- drag-only resize handles are not the sole mode of operation;
- safe-area insets are respected for bottom and sticky controls.

## 11. Zoom and reflow

- support 200% browser zoom and 400% reflow-equivalent width;
- no loss of the primary action or selected object context;
- no page-wide horizontal scrolling;
- horizontal overflow is allowed only inside purposeful regions such as timeline or table;
- modal and drawer content scrolls internally and keeps close/primary actions available;
- sticky headers must not consume excessive height at small widths;
- at 768 px and below, navigation and contextual controls reflow rather than overlap.

## 12. Motion and seizure safety

- respect `prefers-reduced-motion`;
- no flashing, pulsing or rapid repeated status animation;
- progress pulses are not the only evidence of running state;
- panel and toast transitions are short and non-blocking;
- playhead movement is functional feedback, not decorative motion.

## 13. Audit strategy

### 13.1 Automated checks

- run axe or an equivalent WCAG 2.2 AA-compatible scanner;
- run component tests for labels, roles, keyboard and focus;
- run DOM contrast checks where computed styles are available;
- run route-level checks for missing headings, duplicate IDs and unnamed controls;
- run lint and static accessibility checks as part of CI.

### 13.2 Manual keyboard walkthrough

- navigate every primary route with keyboard only;
- open and close each dialog/drawer;
- complete import, candidate review, Studio edit, publish and settings flows;
- test all shortcuts and text-field guard behavior;
- verify focus order and focus restoration;
- verify undo and save/conflict recovery.

### 13.3 Screen-reader spot checks

At least one major desktop browser workflow and one secondary browser/assistive-tech pairing should be validated:

- import and rights;
- processing stage failure/retry;
- candidate selection;
- Clip Studio timeline and transcript;
- export validation;
- publish reconciliation;
- responsive/tablet reflow if supported in the test environment.

### 13.4 Responsive and visual checks

- test 1440, 1280, 1024, 768, 390 and 360 CSS px;
- test portrait and landscape tablet;
- test zoom/reflow;
- test visible focus, selected and disabled states;
- test media preview, caption safe area and platform overlays.

## 14. Route and component acceptance

| Area | Acceptance evidence |
|---|---|
| App shell/navigation | heading/landmark structure, active route, keyboard and focus restoration |
| Import and rights | labels, validation, upload state and source restrictions |
| Processing | stage announcement, retry focus and diagnostic expansion |
| Candidates | card name, evidence text, keyboard accept/reject/compare |
| Clip Studio | track/clip names, time ranges, keyboard controls, numeric edit |
| Export | QA failure name, status and publish-block reason |
| Calendar | date/time semantics, keyboard reschedule and approval controls |
| Social accounts | OAuth status, permissions and reconnect explanation |
| Analytics | metric definitions and text alternatives |
| Settings | provider capability, routing order and permission reasons |

## 15. Defect reporting

Each accessibility defect includes:

- route/component and browser/viewport;
- assistive technology or keyboard method;
- WCAG criterion or design requirement;
- reproduction steps;
- severity and affected task;
- screenshot/recording or DOM evidence;
- remediation and re-test result.

Severity rules:

- Critical: primary task blocked or published/rights decision inaccessible;
- High: core control unusable or focus lost;
- Medium: workaround possible but inefficient or confusing;
- Low: minor polish with no task or conformance impact.

## 16. Conformance gate

No UI phase may claim WCAG conformance until:

- automated route scans pass the agreed threshold;
- critical keyboard flows pass manual walkthrough;
- target sizes and zoom/reflow pass the test matrix;
- Clip Studio assistive-tech spot checks pass;
- all Critical/High defects are fixed or explicitly accepted by the product owner;
- evidence is linked to [09-VISUAL-QA.md](./09-VISUAL-QA.md).

## 17. Gate status

**Current status:** IN PROGRESS - proposed WCAG 2.2 AA engineering baseline.  
**Approval target:** Included in `APPROVE DESIGN v1` after full design review and independent visual/accessibility validation evidence.
