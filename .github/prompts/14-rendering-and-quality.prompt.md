# Feature Phase — FFmpeg Rendering and Media QA

Use `media-pipeline` and `testing-verification`.

Implement deterministic FFmpeg rendering with configurable 9:16, 1:1 and 16:9 presets; default social export 1080x1920 when source quality supports it. Include accurate trims, active-speaker/face tracking (only if implemented and tested), safe crop controls, blur background, audio normalization, word-timed captions, editable templates, logo/brand overlays and output version history.

Do not claim face tracking if the implementation only center-crops. Preserve source timestamps. Rendering must be restartable and independent from transcription. Validate container/codecs, dimensions, FPS, duration, audio presence, A/V sync, subtitle timing, black/frozen frames, safe margins and playability with FFprobe plus tests. Use royalty-cleared/authorized assets only. Stop at gate.


Global rules: Follow `.github/copilot-instructions.md` and the relevant skills. Inspect existing repository state before edits. Do not invent API/model facts. Keep the scope of this prompt only. Do not advance to the next phase automatically. End with a gate report and explicit status.
