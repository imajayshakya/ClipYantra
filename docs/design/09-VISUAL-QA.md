# Visual Quality Assurance

**Status:** APPROVED plan - Phase 07 visual QA baseline  
**Version:** v1  
**Date:** 2026-11-23  
**Prerequisites:** `APPROVE UX v1`, `APPROVE IA v1`, `APPROVE VISUAL DIRECTION v1`, `APPROVE WIREFRAMES v1`, `APPROVE DESIGN SYSTEM v1`

## Review dimensions

1. **Design fidelity:** matches approved wireframe, tokens, typography, hierarchy and component behavior.
2. **Content hierarchy:** primary task/action is obvious; preview/timeline dominate editor as specified.
3. **Consistency:** spacing, type, color, borders, radii, icons and states are token-driven.
4. **Functionality:** controls do what they say; disabled controls explain why.
5. **State coverage:** loading, empty, error, success, conflict, disabled and partial-failure states are checked.
6. **Responsive:** no clipping/overlap/unusable navigation at required viewports.
7. **Accessibility:** keyboard, focus, contrast, labels, reduced motion and zoom.
8. **Media fidelity:** actual video thumbnails, aspect ratio, caption safe zones and timecode alignment are visible.

## Required evidence per UI slice

- Screenshots at desktop and at least one smaller viewport; use the full viewport list for page-level changes.
- List of routes/components checked.
- Automated test/lint/type-check results.
- Accessibility scanner results and manual keyboard notes.
- Known visual deviations and whether approved.
- Browser/device/viewport used.

## Visual regression

- Use deterministic fixture data and stable media test assets.
- Mask genuinely nondeterministic regions only (timestamps, random IDs); do not mask layout or styling defects.
- Review baseline diffs rather than automatically accepting screenshots.
- Avoid updating snapshot baselines simply to make a test green.

## Tools (proposed; verify existing dependencies first)

- Playwright for browser E2E and screenshot capture.
- Storybook or equivalent for component states if component isolation is useful.
- axe-core or equivalent automated accessibility checks.
- Testing Library for UI behavior.
- Existing screenshot/visual comparison tooling if already present.

Add dependencies only after reviewing project constraints, maintenance and license.

## Required viewport and orientation matrix

| Width | View | Required evidence |
|---|---|---|
| 1440 px | Large desktop | full shell and three-pane Clip Studio |
| 1280 px | Desktop/laptop edge | sidebar and inspector collapse |
| 1024 px | Laptop/tablet edge | panel collapse and no page overflow |
| 768 px | Portrait tablet | RQ-4 dashboard, preview, review, approval, calendar and analytics |
| 390 px | Mobile | review, metadata, schedule and settings reflow |
| 360 px | Small mobile | no clipped primary action or validation state |

Where tooling permits, test 768 px portrait and 1024 px landscape tablet orientations.

## Required evidence

For each visual QA slice, record:

- route and viewport;
- browser/device/zoom level;
- approved design artifact and component/state checked;
- screenshot or recording;
- automated test/lint/type-check result;
- keyboard and focus notes;
- contrast and accessibility scan result;
- media/thumbnail/caption safe-area evidence;
- known visual deviation and approval status;
- defect ID when remediation is required.

Do not mask layout or styling defects. Mask only genuinely nondeterministic regions such as timestamps or random IDs.

## Critical route checklist

| Route | Minimum visual/accessibility check |
|---|---|
| Overview | attention state, queue, cards and primary actions |
| Library/Source | thumbnail, status, table/card reflow and source detail |
| Import | source choice, rights, profile, routing and validation |
| Processing | stage state, progress/indeterminate state, retry and logs |
| Candidates | evidence, score explanation and accept/reject |
| Clip Studio | preview, transcript, inspector, timeline, playhead and numeric controls |
| Exports | validation pass/fail and publish eligibility |
| Calendar | month/week/list, detail drawer and timezone |
| Accounts | OAuth status and permission explanations |
| Analytics | available/unavailable metrics and source links |
| Brand/Settings | provider/routing, policy, audit and disabled explanations |

## Gate status

**Current status:** IN PROGRESS - visual QA evidence plan.  
**Approval target:** Included in `APPROVE DESIGN v1` after responsive and accessibility evidence is complete.
