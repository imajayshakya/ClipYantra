# Phase 02 — Architecture and Design Proposal

Use `architecture-design`. READ-ONLY with respect to application code; you may propose documentation artifacts but do not create app implementation.

Using the discovered repository and approved requirements, prepare:
1. System context/container/component architecture.
2. Ingestion→transcription→frame/scene analysis→candidate discovery→ranking→render→review→publish→analytics sequence.
3. Failure/retry/resume and idempotency flow.
4. Provider adapter and capability registry design.
5. NVIDIA API Catalog vs self-hosted NIM separation and GPU detection strategy.
6. Storage/database/job state ownership.
7. API/event contracts at design level.
8. OAuth/security/rights/SSRF/trust boundaries.
9. Local developer, optional GPU worker and cloud deployment topology.
10. Alternatives and trade-offs; do not introduce microservices/Kubernetes without evidence.

Include Mermaid diagrams and a module ownership table. State what should be reused from the existing repository versus newly built. Do not copy AutoShorts source unless licensing is confirmed. No application code. Stop for approval.


Global rules: Follow `.github/copilot-instructions.md` and the relevant skills. Inspect existing repository state before edits. Do not invent API/model facts. Keep the scope of this prompt only. Do not advance to the next phase automatically. End with a gate report and explicit status.
