---
name: media-pipeline
description: "Build resilient video ingestion, transcription, scene analysis, timestamp-safe clip generation and FFmpeg rendering for the four target content categories."
argument-hint: "[phase, feature, or slice ID]"
---

# Media Pipeline

Use for video/audio ingestion, transcription, frame sampling, scene detection, clip selection inputs, rendering and media validation.

## Core principles
- Preserve the original file; work on immutable source references.
- Probe with FFprobe before decoding.
- Use safe temporary directories and cleanup policies.
- Chunk large media and retain global source-time offsets.
- Keep media stages restartable and checkpointed.
- Store outputs in storage adapters; store metadata/state in PostgreSQL.
- Validate generated outputs before changing clip status to ready.

## Category-specific considerations
- Podcasts/interviews: speaker diarization, question-answer context, turn boundaries, two-person layouts.
- Educational/technical: preserve complete explanations, on-screen demonstrations, code/screen visibility, terminology.
- Gaming: audio cues, scene changes, game event markers where available, dense sampling around candidate windows; uniform sparse sampling is not enough by itself.
- Entertainment/funny: setup and payoff must both survive clipping; do not cut before punchline/reaction.

## Render quality checks
Validate actual duration, dimensions, codec, frame rate, audio stream, audio/video sync, black/frozen frames, subtitle timing, safe margins, crop subject visibility and playable output. Keep rendering settings/version linked to each clip version.

Do not use AI to perform deterministic trimming when FFmpeg can do it precisely. AI proposes; deterministic code validates and renders.
