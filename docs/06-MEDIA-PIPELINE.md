# Media Processing Pipeline

**Status:** PROPOSED

## 1. Pipeline stages

`registered → validated → normalized → transcribed → aligned → indexed → candidates_discovered → candidates_ranked → rendered → qa_passed → review_ready`

Publishing is downstream and separate.

## 2. Ingestion

- Validate file extension and actual media probe result.
- Enforce configurable upload size, duration and codec limits.
- Store original immutable source and checksum.
- Capture user rights declaration and source provenance.
- Use private object storage and temporary signed URLs.
- Prevent SSRF in URL imports (block loopback, private, link-local and metadata IP ranges; validate redirects and DNS resolution).

## 3. Normalization

Use FFprobe to record streams, duration, dimensions, frame rate, pixel format, codecs, rotation and audio properties. Use FFmpeg to extract audio and optional proxies. Never overwrite source.

## 4. Transcription and time alignment

- Select provider based on language, diarization/timestamp requirements, user policy and availability.
- Split long audio with overlap while maintaining absolute source offsets.
- Store segment/word start and end in milliseconds.
- Deduplicate overlapping chunk text.
- Preserve original language and transcript version.
- Support manual transcript corrections.

## 5. Scene and signal indexing

- Detect scene boundaries and representative frames.
- Build face/speaker tracks where enabled.
- Optionally derive audio energy, silence, laugh/reaction and speech-turn features.
- Gaming can use adaptive sampling around audio peaks, scene changes, gameplay events and facecam reaction.
- Optional chat/replay data requires source-specific authorization and availability; it must never be assumed.

## 6. Candidate discovery and selection

- Use deterministic low-cost signals to propose windows.
- Use transcript semantics and multimodal analysis to evaluate candidate windows.
- Keep enough pre-roll/post-roll for setup and payoff.
- Respect content-profile-specific rubric.
- Deduplicate and ensure source coverage/diversity.
- Validate start/end within source bounds and snap to word/scene boundaries when appropriate.
- Reject clips with incomplete sentences, missing setup, ungrounded claims or no supported source evidence.

## 7. Rendering

- Store a declarative render specification, not only an FFmpeg command string.
- Create versioned output with source map/sidecar metadata.
- Support vertical, square and original-aspect presets.
- Support caption tracks, brand overlays, audio gain, crop keyframes, optional effects and B-roll.
- Use font/asset licensing checks.
- Run rendering in isolated worker scratch space with resource/time limits.

## 8. Optional B-roll behavior

- Generate cues only when source narration refers to something filmable and an asset helps.
- Respect protected opening/closing moments and speaker gestures/important screen content.
- Store cue source, licence/attribution, source URL, time interval and asset checksum.
- Avoid repeated stock asset use within a single task when feasible.
- If B-roll provider/plan/download fails, continue without B-roll only when the chosen policy permits; record warning. Do not replace it with unlicensed generated assets.

## 9. Quality assurance

Validate: playable file, expected streams, duration, frame dimensions, frame rate, aspect ratio, audio level/clipping, A/V sync, subtitle timing, subtitle safe area, black frames, crop/faces, output file size and platform preset. QA failure blocks publishing.

## 10. Restartability

Each stage records input hash/version, configuration, output references, started/completed time, state, attempt count and error diagnostics. Re-run only a stage when its inputs/config change or its prior run failed. Keep completed transcription/analysis when only the renderer changes.
