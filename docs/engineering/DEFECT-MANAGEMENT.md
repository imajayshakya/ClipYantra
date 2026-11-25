# Defect Management

## Severity
- `S0 Critical`: security compromise, major data loss, unauthorized publishing or system-wide outage.
- `S1 High`: core workflow blocked, widespread incorrect output, duplicate posts or corrupted media.
- `S2 Medium`: important feature degraded with workaround.
- `S3 Low`: minor defect, cosmetic issue or low-impact edge case.

Priority is decided separately using user impact, frequency, exposure, deadline and release risk.

## Required defect fields
ID, title, severity, priority, affected requirement/AC, build/commit, environment, preconditions, reproduction steps, expected/actual results, evidence, frequency, impact, workaround, suspected root cause, owner, fix version, regression TEST ID, retest evidence and status.

## Closure
A defect closes only after the fix is tested on the target build, its regression test passes and relevant adjacent workflows are re-run. Do not close due to code review alone.
