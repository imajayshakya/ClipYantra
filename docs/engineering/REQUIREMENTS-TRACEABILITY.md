# Requirements Traceability

Maintain `REQUIREMENTS-TRACEABILITY.csv` as the live matrix.

## Traceability chain
Requirement → acceptance criterion → UX/design artifact → architecture/ADR → API/data contract → implementation slice/PR → automated/manual test → execution evidence → release.

## Minimum CSV columns
`requirement_id,acceptance_criteria_id,priority,design_ref,adr_ref,contract_ref,slice_id,code_ref,test_id,test_level,latest_result,evidence_ref,defect_id,status,notes`

## Status meanings
- `UNMAPPED`: no downstream implementation/test mapping yet.
- `PLANNED`: mapped to design/contracts/slice, not implemented.
- `IMPLEMENTED_UNVERIFIED`: code exists but evidence is incomplete.
- `VERIFIED`: applicable technical tests passed with evidence.
- `VALIDATED`: user/business acceptance completed.
- `BLOCKED`: evidence or dependency unavailable.
- `DEFERRED`: explicitly deferred with human approval.

No requirement may be marked complete from code presence alone. No test case may be considered coverage unless linked to an approved AC.
