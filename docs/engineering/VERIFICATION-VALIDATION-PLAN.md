# Verification and Validation Plan

## Verification vs validation
**Verification:** Does the implementation conform to approved requirements, design, contracts and technical specifications?

**Validation:** Does the increment meet user needs and produce the intended outcome in realistic use?

## Evidence record
For each AC record: AC ID; verification/validation method; test ID or inspection; commit/build; environment; test data; exact command/action; expected result; actual result; artifact/log/screenshot; result (PASS/FAIL/NOT RUN/BLOCKED); defect ID; reviewer; date.

## Required checks by feature family
- Ingestion: permitted source, format/size validation, upload interruption, SSRF, duplicates, cleanup.
- Transcription: language, alignment, chunk boundary continuity, speaker attribution and fallback.
- AI selection: schema, timestamp bounds, segment context, duplicate windows, unsupported outputs and provider outage.
- Rendering: codecs, duration, dimensions, audio sync, subtitle timing, crop/speaker visibility, corrupted/black frames.
- Publishing: OAuth permissions, approval policy, idempotency, unknown outcome reconciliation, retry and rate limits.
- Analytics: source attribution, time windows, missing metrics and no fabricated values.
- UI: design match, responsive states, keyboard, focus, errors, empty/loading/disabled states and visual regression.

## Reporting
Not-run is never pass. A mocked integration is not proof of live provider/platform behavior. Record residual risks and require explicit human acceptance for validation and release.
