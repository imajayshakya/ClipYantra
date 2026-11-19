---
name: scaffold-only
description: "Create approved project scaffolding and explicit placeholders without implementing production business logic or pretending integrations work."
argument-hint: "[phase, feature, or slice ID]"
---

# Scaffold Only

Use only after the design and scaffold scope have been explicitly approved.

## Allowed
- Folder/module layout.
- Package manifests and pinned baseline dependencies after licence/compatibility review.
- Environment variable examples with empty values.
- Pydantic/TypeScript interface shells.
- SQLAlchemy model skeletons only when contracts are approved.
- Router registration and health/readiness endpoints.
- Celery app configuration and named task shells.
- Provider abstract base classes and registry interfaces.
- Storage, publisher and transcription interfaces.
- README and architecture docs.
- Minimal smoke tests for startup and imports.

## Not allowed
- Implementing business logic.
- Calling real paid APIs.
- Uploading/publishing content.
- Returning fake successful results.
- Creating insecure placeholder credentials.
- Broad refactoring or replacing existing project structure without approval.

## Placeholder contract
Every unimplemented operation must fail explicitly with a clear `NotImplementedError`, `501 Not Implemented`, or disabled capability status. Label stubs in code and docs. Do not silently return empty success data.

## Verification
Run format/lint/type checks and import/startup tests available in the repository. Report exactly which components are placeholders and what remains for the next slice.
