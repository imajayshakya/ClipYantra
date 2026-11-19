---
name: phase-12-transcription-and-alignment
description: "Build transcription, word alignment, and diarization with timestamp-safe processing."
disable-model-invocation: true
---

# Feature Phase — Transcription, Word Alignment and Diarization

Use `ai-provider-integration`, `media-pipeline` and `testing-verification`.

Implement common transcription interface with local WhisperX/faster-whisper and approved cloud adapters (NVIDIA Nemotron Transcribe NIM, OpenAI, Groq, Deepgram as verified). Verify current official docs and deployed model capabilities. Treat NVIDIA NIM as a distinct self-hosted service; check OS, container, driver and supported GPU before enabling. Never assume hosted API Catalog and NIM share the same request schema.

Support English, Hindi and Hinglish test corpus, word/sentence timestamps, alignment, optional diarization, SRT/VTT/JSON export, chunk offsets, overlap deduplication, retry and persisted provider/model metadata. If a provider lacks word timestamps, use a separately verified aligner. Do not invent diarization when unavailable. Add transcript review/edit path and deterministic fixtures. Stop at gate.


Global rules: Follow `.github/copilot-instructions.md` and the relevant skills. Inspect existing repository state before edits. Do not invent API/model facts. Keep the scope of this prompt only. Do not advance to the next phase automatically. End with a gate report and explicit status.
