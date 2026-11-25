# Interaction, Feedback and Motion Specification

**Status:** APPROVED v1 - Phase 07 interaction baseline  
**Version:** v1  
**Date:** 2026-11-23  
**Prerequisites:** `APPROVE UX v1`, `APPROVE IA v1`, `APPROVE VISUAL DIRECTION v1`, `APPROVE WIREFRAMES v1`, `APPROVE DESIGN SYSTEM v1`  
**Approval target:** Included in `APPROVE DESIGN v1` after architecture and full design review

This document defines interaction behavior, state transitions, feedback and recovery. It does not implement controls or add application code.

## 1. Interaction contract

Every meaningful action follows a four-part contract:

1. **Trigger:** what the user or system initiates.
2. **Response:** what the system validates, persists or dispatches.
3. **Feedback:** the immediate acknowledgement, progress state or error.
4. **Recovery:** the next safe action, including undo, retry or reconciliation.

An interaction is incomplete if it lacks a truthful loading state, an empty state, a permission/disabled reason or a recovery path.

## 2. Core principles

- Acknowledge every user action immediately.
- Use measured progress; never invent a percentage or ETA.
- Preserve the original source and immutable candidate.
- Make AI suggestions reversible and user-approved.
- Autosave and publish status must be explicit.
- Destructive actions explain consequence and scope.
- Pointer, touch and keyboard interactions expose equivalent outcomes.
- Motion clarifies causality and is disabled under `prefers-reduced-motion`.
- Focus stays inside modal dialogs and returns to a logical trigger after close.

## 3. State transition model

### 3.1 Source video

```text
created -> uploading -> validating -> ready
                                  -> rejected
                                  -> failed
ready -> archived
failed -> uploading or ready after repair/retry
```

### 3.2 Processing job

```text
queued -> running -> waiting_for_input
                  -> retrying
                  -> succeeded
                  -> failed
                  -> cancelled
```

Rules:

- successful stages are not re-executed during stage retry;
- user cancellation is persisted and checked between stages;
- provider fallback is visible as degraded or alternate provider, not hidden;
- final result data is not marked complete until stage output is validated.

### 3.3 Clip candidate

```text
pending_review -> accepted -> draft created
                -> rejected
                -> needs_edit -> accepted or rejected
```

Candidate scores are editorial evidence, not guaranteed virality.

### 3.4 Draft

```text
editing -> saving -> saved
                 -> save_failed -> editing or conflict
saved -> editing
editing -> conflict
```

Rules:

- source and candidate remain immutable;
- every edit creates a new version or a reversible operation;
- save failure preserves local draft state and offers retry;
- conflict resolution is explicit and never silently overwrites another version.

### 3.5 Render

```text
queued -> rendering -> validating -> ready
                                  -> failed
```

An invalid render never becomes publishable. The UI exposes the failed QA gate and a recovery action.

### 3.6 Scheduled post

```text
draft -> awaiting_approval -> scheduled -> uploading -> processing -> published
                                                                    -> failed
                                                                    -> unknown_reconciliation
scheduled -> cancelled
uploading -> unknown_reconciliation
processing -> unknown_reconciliation
```

Unknown reconciliation is a blocking state until the platform and local outbox agree. It does not automatically create duplicate publish attempts.

## 4. Critical workflow interactions

### 4.1 Import source

| Step | Trigger | System response | Feedback | Resulting state | Recovery |
|---|---|---|---|---|---|
| Choose source | Select upload, URL, Azure, watched folder or official platform flow | Validate source type and access | Inline source summary | source selected | Change or remove source |
| Declare rights | Select owned/authorized/public-domain | Persist rights and provenance | Required-field validation | rights complete/incomplete | Correct missing declaration |
| Choose profile | Select content profile | Save profile and show routing implication | Profile summary | profile selected | Change profile |
| Choose routing | Review workspace/profile/job routing | Check provider capabilities and limits | Estimated cost label only if available | routing selected | Override or use default |
| Start | Confirm import and processing | Validate source then create job | Source row plus real stage progress | queued/running or blocked | Retry, cancel or resolve rights |

Rules:

- block processing until rights are complete;
- never imply an authorized-looking link is downloadable;
- platform imports use official or supported access only;
- interrupted upload provides resume or safe retry.

### 4.2 Processing monitor

| Step | Trigger | System response | Feedback | Resulting state | Recovery |
|---|---|---|---|---|---|
| Open job | Navigate to source job detail | Load durable stage state | Stage timeline | queued/running/succeeded/failed | Open source or retry |
| Stage running | Worker emits stage event | Persist progress and diagnostic category | Stage label and measured progress | running/waiting | Open diagnostics |
| Stage failed | Adapter or worker returns failure | Persist stage failure and completed-stage state | Inline stage error | failed/retryable | Retry stage or provider |
| Retry | Choose retry stage/job | Dispatch from last completed stage | Retry acknowledgement | retrying/running | Cancel or return to source |
| Cancel | Choose cancel | Persist cancellation intent and stop between stages | Confirmation and final state | cancelled | Open partial results if available |

Progress bars must not animate as a guarantee. Use a label and measured percentage only when the backend has a measured value.

### 4.3 Candidate discovery

| Step | Trigger | System response | Feedback | Resulting state | Recovery |
|---|---|---|---|---|---|
| Open candidates | Navigate or processing completes | Load evidence-backed candidates | Sort/filter summary | pending_review | Change filters/profile |
| Compare | Select 2-4 candidates | Open side-by-side evidence | Selection count | comparison | Remove candidate or open Studio |
| Accept | Choose accept/edit | Create versioned draft | Saving acknowledgement | accepted/draft created | Open Studio |
| Reject | Choose reject | Persist decision | Undo available when possible | rejected | Undo or choose another |
| Needs edit | Open with context gap | Mark candidate for editing | Explicit reason | needs_edit | Adjust trim/profile |

Use text and visual evidence for ranking. Never present `score` as virality probability.

### 4.4 Clip Studio editing

| Step | Trigger | System response | Feedback | Resulting state | Recovery |
|---|---|---|---|---|---|
| Open draft | Enter Studio route | Load immutable candidate and latest draft | Save state | editing/saving/saved | Reload conflict if changed |
| Scrub | Drag playhead or use keyboard/numeric control | Update preview and transcript context | Current timecode | editing | Clear selection |
| Select clip/cue | Select timeline clip or transcript segment | Update inspector and accessible selection | Name/time range | editing | Escape clears selection |
| Trim/split/crop | Pointer or numeric control | Validate operation and create reversible transaction | Before/after preview or draft state | editing/saving/saved | Undo/redo |
| Caption edit | Edit cue text/timing | Validate timing and update source map | Inline timing state | editing/saving/saved | Revert cue |
| Save | Auto-save or explicit save | Persist operation history and draft version | Saving/saved/save_failed | saved/save_failed/conflict | Retry or resolve conflict |
| Export | Choose export | Queue technical validation/render | Real render stage | queued/rendering/validating/ready/failed | Edit or open QA diagnostics |

The source remains immutable. A generated candidate can be viewed but not silently mutated.

### 4.5 Natural-language AI edit

```text
User intent
  -> parse typed operation proposal
  -> validate allow-list and source bounds
  -> preview before/after diff
  -> user accept, modify or reject
  -> apply as one reversible transaction
```

The UI must:

- display each operation type and parameters;
- reject arbitrary or unsupported operations;
- show source-relative impact;
- require confirmation before applying;
- show undo/redo as a single user-visible transaction;
- preserve any operation outside the allow-list for retry or manual edit.

AI cannot emit shell commands, FFmpeg arguments or executable code.

### 4.6 Export and publish preparation

| Step | Trigger | System response | Feedback | Resulting state | Recovery |
|---|---|---|---|---|---|
| Create export | Confirm format/aspect | Validate and queue render | Render stage state | queued/rendering/validating | Cancel/retry |
| QA fail | Validator finds issue | Block publish eligibility | Inline failure and evidence | failed/blocked | Return to Studio |
| Prepare metadata | Open publish flow | Load platform presets | Character limits and unavailable fields | editing | Correct metadata |
| Select destination | Choose account | Validate OAuth scope and capability | Account health and permission gaps | selected/blocked | Reconnect account |
| Schedule/publish | Confirm policy | Persist scheduled post or outbox action | Confirmation and external status | awaiting/scheduled/uploading/processing | Reconcile, cancel or retry safely |

Publish actions must never be presented as complete until the platform confirms or reconciliation resolves the outcome.

### 4.7 Unknown publish outcome

On timeout or partial platform response:

1. record the attempt and uncertainty;
2. set post state to `unknown_reconciliation`;
3. stop automatic duplicate retry;
4. reconcile through official platform state;
5. show confirmed published, confirmed absent or still uncertain;
6. only retry after reconciliation with the same idempotency key.

### 4.8 Provider settings

| Step | Trigger | System response | Feedback | Resulting state | Recovery |
|---|---|---|---|---|---|
| Test provider | Choose test connection | Check capability and credentials | Provider result | healthy/degraded/error/disabled | Reconnect or change provider |
| Change workspace default | Select provider/routing mode | Validate capability | Routing preview | saved/conflict | Revert |
| Add profile override | Map content profile | Store lower-precedence override | Profile summary | saved | Remove override |
| Per-job override | Open import/job routing | Store job-specific choice | Job summary | selected/default | Restore default |
| Cost limit reached | Job attempts provider request | Block or fall back by policy | Explicit budget message | blocked/degraded | Change limit or provider |

The UI distinguishes NVIDIA API Catalog from NVIDIA NIM and does not assume unverified local GPU compatibility.

### 4.9 Workspace and publishing policies

| Step | Trigger | System response | Feedback | Resulting state | Recovery |
|---|---|---|---|---|---|
| Change brand/workspace | Switch context | Load scoped library/settings | Active context | changed | Return/clear filter |
| Change policy | Edit approval or schedule rule | Preview effect and validate | Unsaved/confirmation state | editing/saved/save_failed | Cancel or confirm |
| Confirm policy | Accept consequence | Persist audit event | Success with scope summary | saved | Undo or view audit |
| Audit filter | Filter actor/action/resource | Query scoped audit history | Result count | populated/empty/error | Clear or change filter |

Publishing policy changes require confirmation and are recorded in audit history.

## 5. Global feedback and recovery

| Situation | Inline behavior | Global behavior | Recovery |
|---|---|---|---|
| Validation error | Field-level message with correction | Submission summary if needed | Fix field and retry |
| Single resource failure | Error state in context | Optional toast | Retry or open details |
| Partial failure | Show successful and failed subsets | Warning banner | Resolve one item at a time |
| Permission denied | Disabled control with reason or hidden control | Explanation after navigation | Request owner action |
| Unsaved change | Saving/saved/save_failed indicator | Route-change warning | Save, retry or discard |
| External uncertainty | Reconciliation state | Persistent warning | Reconcile official state |

Inline messages must not disappear without the underlying state changing. Toasts must not be the only record of destructive or publish outcomes.

## 6. Autosave and conflict behavior

- autosave begins after an edit settles, not on every high-frequency pointer move;
- show `saving`, `saved`, `save_failed` and `conflict`;
- retain unsaved local operations across save failure;
- prevent navigate-away data loss with a warning;
- conflicts identify draft version, source and affected operation;
- user chooses retry, reload or replace only after consequence is clear.

## 7. Keyboard interaction

### 7.1 Global shortcuts

| Key | Action | Guard |
|---|---|---|
| `Cmd/Ctrl+K` | Open global search | Always outside modal when available |
| `/` | Focus list/search field | Disabled while text input or editor text field is focused |
| `Escape` | Close dismissible surface; clear one selection | Never close unsaved destructive form without warning |
| `Enter` | Activate focused action or selected item | Standard native behavior |
| `Tab` / `Shift+Tab` | Move focus | Follow document and panel order |
| Arrow keys | Navigate lists/tabs/day/elements | Context-specific and documented |

### 7.2 Clip Studio shortcuts

| Key | Action | Guard |
|---|---|---|
| `Space` | Play/pause preview | Disabled while text input or modal is active |
| `Left/Right` | Move playhead one frame | Disabled while text input is active |
| `Shift+Left/Right` | Move playhead five seconds | Disabled while text input is active |
| `Ctrl/Cmd+=/-` | Zoom timeline | Disabled while text input is active |
| `Ctrl/Cmd+Z` | Undo | Draft/editor scoped |
| `Ctrl/Cmd+Shift+Z` or `Ctrl/Cmd+Y` | Redo | Draft/editor scoped |
| `Delete` | Remove selected clip/cue only after confirmation policy | Never active in text field |

All critical shortcuts appear in a visible shortcut reference. Numeric trim and timing fields provide a non-keyboard-shortcut alternative.

### 7.3 Dialog and menu behavior

- dialog/drawer traps focus while open;
- focus returns to the trigger after close;
- Escape closes only when no destructive unsaved state would be lost;
- menus support arrow keys, Enter/Space and Escape;
- route navigation announces the new page title or context.

## 8. Pointer and touch interaction

- no action is pointer-hover-only;
- drag is an optional accelerator for timeline and calendar;
- trim, split, move, reorder and caption timing have numeric controls;
- approval/rejection controls remain visible at tablet widths;
- touch targets are at least 44 px for primary tablet/mobile actions;
- no drag-only list reorder or platform reschedule;
- swipe is never the sole way to approve or reject.

## 9. Motion and reduced motion

From the design-system tokens:

- micro interaction: 120 ms ease-out;
- panel transition: 200 ms ease-out;
- reduced motion: no animation and no transition delay.

Motion must not communicate progress by itself. Status text and non-animated icons remain visible.

## 10. Destructive and irreversible actions

Require confirmation for:

- deleting source assets;
- disconnecting social accounts;
- deleting brand assets or published-post references;
- replacing a conflicting draft;
- changing automation policies.

Confirmation content states:

- scope;
- affected objects;
- irreversible consequence;
- undo availability;
- primary cancel action.

Use undo/restore for source-safe operations where feasible.

## 11. Traceability

| Requirement | Interaction evidence |
|---|---|
| FR-025 to FR-028 | Versioned draft, typed AI edit, undo/redo and state recovery |
| FR-034 to FR-036 | Publishing policy, reconciliation and duplicate prevention |
| FR-050 | Provider test, routing precedence and fallback feedback |
| FR-051, NFR-006 | Truthful stage progress and diagnostics |
| NFR-001 | Retry from last completed stage |
| NFR-007 | Export QA state blocks publish |
| RQ-4 | Visible tablet review/approval and limited editing |
| NFR-010 | Deterministic interaction and state test hooks |

## 12. Interaction acceptance checklist

- [ ] Every primary action has immediate feedback.
- [ ] Progress values are measured or explicitly indeterminate.
- [ ] Draft, render and post states have recovery paths.
- [ ] AI operations are typed, previewed and confirmed.
- [ ] Timeline operations have numeric alternatives.
- [ ] Autosave exposes saving/saved/failure/conflict.
- [ ] Unknown publish outcomes reconcile before retry.
- [ ] Destructive actions confirm scope and consequence.
- [ ] Keyboard shortcuts do not conflict with text fields.
- [ ] Tablet approval and review actions are never hover-only.
- [ ] Reduced-motion behavior is explicit.

## 13. Gate status

**Current status:** IN PROGRESS - proposed interaction and state baseline.  
**Approval target:** Included in `APPROVE DESIGN v1` after this artifact, accessibility/responsive baselines and architecture review are complete.
