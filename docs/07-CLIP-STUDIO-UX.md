# Clip Studio — Product and Interaction Specification

**Status:** PROPOSED. This summary is subordinate to the detailed screen and design specifications in `docs/design/`.

## Objective

Provide a creator-friendly multi-track editor for generated clips. The editor must support human editing even if optional AI services are unavailable.

## Primary composition hypothesis

- Header: source/clip identity, draft version, undo/redo, save state and export.
- Left context panel: transcript, candidate rationale and source context.
- Center: large preview with safe-area/crop overlays.
- Bottom: timeline with video, audio, captions, B-roll and effects/brand lanes.
- Right inspector: framing, captions, audio, B-roll, effects, metadata and export preset.
- Panels are collapsible and resizable where practical.

## Immutable originals and drafts

- Generated source clip is immutable.
- Every edit creates/updates a versioned draft.
- Autosave uses optimistic concurrency/version checks.
- Operations record actor, timestamp, operation type, parameters and parent version.
- Undo/redo is deterministic.

## Allowed edit operations

`TrimRange`, `SplitAt`, `MergeClips`, `SetAspectRatio`, `SetCropMode`, `SetCropKeyframes`, `UpdateCaptionText`, `ShiftCaptionCue`, `SetCaptionStyle`, `AddBrollCue`, `MoveBrollCue`, `RemoveBrollCue`, `AdjustAudioGain`, `AddEffect`, `RemoveEffect`, `SetBrandOverlay`.

AI proposes typed allow-listed operations only. Server validates bounds and permissions before apply. Never execute arbitrary model-generated code or commands.

## Source map

Keep source-to-clip time mapping and overlay cues coherent through trim, split, merge and re-render. Prefer render-from-source to avoid quality loss from repeated encodes.

## Design references

- `docs/design/05-SCREEN-SPECIFICATIONS.md`
- `docs/design/06-INTERACTION-AND-STATES.md`
- `docs/design/07-ACCESSIBILITY.md`
- `docs/design/08-RESPONSIVE-STRATEGY.md`
- `docs/design/09-VISUAL-QA.md`

No Clip Studio frontend implementation before design approval.
