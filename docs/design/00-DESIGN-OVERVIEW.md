# ClipYantra Design Overview

**Status:** IN PROGRESS - UX, IA, Visual Direction, Wireframes and Design System are approved; interaction, responsive and accessibility specifications are in progress.

## Product design objective

ClipYantra should feel like a professional creator workstation that reduces the distance between raw footage and a publishable short-form asset. It must serve both high-level content operations (library, processing, calendar, analytics) and precise editing work (preview, transcript, timeline, track inspector).

## Design outcomes

1. A new user can understand the workflow without reading documentation.
2. A user can identify what the system is doing, what is blocked and what needs approval.
3. The Clip Studio supports accurate edits without requiring external desktop editing software for common jobs.
4. Advanced AI settings remain discoverable but do not overwhelm everyday creators.
5. Publishing controls make the destination, schedule, approval policy and post status explicit.
6. UI remains usable at supported desktop, tablet and mobile breakpoints.
7. Accessibility is designed into components and workflows, not added only at the end.

## Approved visual direction

**Direction:** Calm Creator Workstation (Direction A).

- Dark-first environment for the editor to reduce visual competition with video preview.
- Neutral graphite/slate surfaces with one restrained indigo brand accent and teal/amber/red state semantics.
- High-contrast typography and clear density tiers: spacious management views, denser editor workspace.
- Minimal decoration; visual hierarchy comes from alignment, type, spacing and state.
- Direction B is retained only as a reference for management-screen exploration.

Approval record: `APPROVE VISUAL DIRECTION v1` received 2026-11-22.

## Primary navigation hypothesis

- Overview
- Library
- Create / Clip Studio
- Calendar
- Analytics
- Connections
- Brand Kit
- AI & Processing Settings

Workspace switcher/profile lives in the application shell. Exact navigation is confirmed during information architecture.

## Experience principles

- **Clarity:** current source, job state, active clip and publishing destination are always understandable.
- **Control:** AI suggestions are inspectable, editable and reversible.
- **Trust:** no fake progress, opaque costs, hidden publishing or unlabelled sample data.
- **Focus:** editing surfaces prioritize preview and timeline.
- **Recovery:** drafts autosave, errors explain recovery and destructive operations can be undone where possible.
- **Consistency:** the same terms and states mean the same thing across dashboard, editor and calendar.

## Design approval artifacts

Before implementation, the owner must approve:

1. UX research summary and personas.
2. Information architecture and core user flows.
3. Brand/visual direction.
4. Screen wireframes and responsive behavior.
5. Design tokens and component catalog.
6. Interaction, state and motion specifications.
7. Accessibility and visual QA acceptance criteria.

Record the approval version/date in `10-DESIGN-DECISIONS.md`.
