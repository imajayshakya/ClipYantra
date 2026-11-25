# Delivery Slice Playbook

## Slice sizing
Prefer one observable capability across the necessary layers (e.g. register an uploaded file → persist metadata → show it in the library) over a large horizontal batch (all backend first, all UI later). A slice should normally be reviewable in one focused session and should not mix unrelated features.

## Slice template
- Slice ID/name/outcome
- Parent requirement IDs and AC IDs
- User journey and design references
- API/data contract references
- In-scope / out-of-scope
- Dependencies and assumptions
- Files/modules expected to change
- Implementation tasks
- Test IDs and test data
- Risk and failure scenarios
- Observability/logging
- Rollback/recovery
- Definition of Ready checklist
- Definition of Done checklist
- Human approval token

## Execution
One approved slice at a time. Test-first where practical. Keep commits focused. If actual work reveals a requirement/contract mismatch, stop and raise a change request rather than improvising.
