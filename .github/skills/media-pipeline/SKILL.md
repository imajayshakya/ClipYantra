---
name: media-pipeline
description: Implements restartable media ingestion, transcription, indexing, rendering and QA stages.
---

# Media Pipeline

Read `docs/06-MEDIA-PIPELINE.md`. Preserve originals, source timestamps and stage outputs. Use FFprobe for validation and FFmpeg for deterministic processing. Separate transcription, AI analysis, rendering and publishing. Make jobs recoverable. Validate final outputs before they become publishable.
