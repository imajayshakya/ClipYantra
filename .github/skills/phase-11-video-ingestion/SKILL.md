---
name: phase-11-video-ingestion
description: "Design and implement authorized video ingestion with resilient source handling."
disable-model-invocation: true
---

# Feature Phase — Mixed Video Ingestion

Use `media-pipeline`, `chunked-development` and `testing-verification`. Implement only the approved ingestion slice.

Support user-authorized uploads and supported media imports: MP4/MOV/WebM and other verified FFmpeg-readable formats; authorized direct media URLs; Azure Blob/local storage; optional watched folders; platform imports only where terms/API authorize access. A public video page URL is not automatically a downloadable source file.

Requirements: rights declaration, source provenance, FFprobe metadata, secure storage keys, multipart/resumable upload where needed, deduplication, cancellation, progress, cleanup and recovery. Protect against SSRF: allowlist schemes, block private/link-local/metadata IP ranges after DNS resolution, validate redirects and re-check destination. Do not implement DRM bypass or access-control circumvention. Do not expose permanent public Blob containers.

Deliver ingestion service, storage adapters, API/UI for upload, database state, tests and docs. Implement one slice at a time; stop at gate.


Global rules: Follow `.github/copilot-instructions.md` and the relevant skills. Inspect existing repository state before edits. Do not invent API/model facts. Keep the scope of this prompt only. Do not advance to the next phase automatically. End with a gate report and explicit status.
