# Requirements Engineering Standard

## Requirement types and IDs
`BR-*` business requirements; `FR-*` functional; `NFR-*` non-functional/quality attributes; `CON-*` constraints; `AC-*` acceptance criteria; `OUT-*` out of scope; `ASM-*` assumptions; `Q-*` unresolved questions. IDs remain stable across revisions.

## Required fields
Each requirement records ID, statement, rationale/source, priority (MoSCoW or approved scheme), status (confirmed/assumed/proposed/unresolved/approved/deprecated), owner/decision-maker, dependencies, acceptance criteria and verification method.

## Elicitation
Capture stakeholders, personas, jobs-to-be-done, current workflow, desired outcome, primary/alternate/error journeys, roles/permissions, data/media constraints, platform dependencies, operational expectations and non-goals. Ask focused questions for material ambiguity.

## Quality criteria
Requirements should be necessary, singular, unambiguous, consistent, feasible, traceable and verifiable. Quantify performance and reliability. Define supported languages, media formats, clip duration limits and platform requirements only after current technical verification.

## ClipYantra requirement domains
Source ingestion and rights; media validation; transcription/alignment/diarization; multimodal highlight discovery; provider routing; local GPU detection; editor/timeline/drafts; render pipeline; captions/branding; quality checks; OAuth/social connections; approval/scheduling; analytics/learning; billing/usage if later in scope; security/privacy/retention; operations/observability; accessibility and responsive UX.

## Baseline control
The PRD is a draft until explicit approval. Changes require change-impact analysis and traceability updates. Never treat a proposed model, platform integration or stack choice as confirmed solely because it appears in this document.
