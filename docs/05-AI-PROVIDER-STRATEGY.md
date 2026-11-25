# AI Provider Strategy — ClipYantra

**Status:** IN PROGRESS - Phase 08 provider architecture baseline. Model IDs and capabilities must be re-verified at implementation time.

## 1. Design

Implement two independent registries:

1. **Provider registry:** how to call an integration (hosted API, self-hosted service, local runtime).
2. **Capability registry:** what a particular model can reliably accept/return (text, image, video, audio, JSON schema, language, timestamps, diarization, context limits).

The router selects only from currently verified compatible capabilities. A provider being enabled does not imply every model is suitable for every task.

## 2. Provider roles under consideration

| Provider | Candidate responsibilities | Validation required |
|---|---|---|
| NVIDIA API Catalog | Nemotron multimodal, vision-language and text reasoning | Current model ID, modality, payload format, API compatibility and hosted limits |
| NVIDIA NIM | Self-hosted inference and speech services | GPU/driver/runtime compatibility, model container, licence and hardware |
| Gemini | Video understanding, scene context, multimodal event discovery | Video duration/sampling, language, file API and pricing |
| OpenAI | Transcription, structured selection/ranking, metadata and evaluation | Current model IDs, file limits, output schema support and prices |
| Anthropic | Transcript reasoning and frame/contact-sheet analysis | Image input constraints, context and pricing |
| Groq | Fast transcription/inference | Model availability, rate limits, language and timestamps |
| Deepgram | Speech recognition, diarization, word timings | Language/model and output fields |
| WhisperX/faster-whisper | Local ASR and alignment | GPU/CPU, model size, language, timestamp quality |
| Ollama/Qwen | Local text/vision analysis | Installed model, VRAM, context and image modality support |

## 3. Routing profiles

- `local_first`: local models where verified; no silent cloud fallback unless user explicitly permits it.
- `balanced`: local transcription/cheap deterministic analysis plus selective cloud multimodal/ranking.
- `cloud_first`: hosted providers for requested tasks, with explicit cost controls.
- `manual`: user selects provider/model for each task.

## 3.1 Hierarchical routing precedence

Resolved provider routing is:

1. Workspace default configuration.
2. Content-profile-specific override.
3. Per-job manual override.

Supported routing modes:

- `local-first`: prefer verified local capability; no silent cloud fallback unless permitted.
- `balanced`: balance local deterministic/ASR work with selective cloud reasoning.
- `cloud-first`: prefer hosted providers within cost limits.
- `user-selected`: use the explicitly selected provider/model for that task.

Per-brand routing is deferred.

The provider registry must represent:

- NVIDIA API Catalog / Nemotron.
- NVIDIA NIM.
- Gemini.
- OpenAI.
- Anthropic / Claude.
- Groq.
- Deepgram.
- Ollama.
- WhisperX/faster-whisper.

## 4. Suggested task flow

1. Local FFmpeg/FFprobe metadata and deterministic extraction.
2. Speech transcription via configured ASR (WhisperX, NVIDIA Transcribe NIM, Groq, Deepgram or OpenAI as capability-verified options).
3. Word alignment and diarization if needed.
4. Scene/event indexing and frame sampling.
5. Deterministic candidate proposals from transcript boundaries, silence/audio peaks, scenes, chat/replay signals only when authorized/available.
6. Multimodal LLM evaluates only shortlisted windows.
7. Ranking model scores hook, standalone context, payoff/completeness, value, emotional signal and visual suitability.
8. Independent validator checks timestamps and transcript evidence.
9. Persist model-specific scores and disagreements.

## 5. NVIDIA requirements

Treat NVIDIA API Catalog and NVIDIA NIM as distinct adapters and deployments. Do not assume Nemotron Omni, Super VL, text models and Nemotron Transcribe share payloads, supported modalities, language support or runtime requirements. At startup/settings validation:

- Load configured model capabilities from versioned metadata.
- Verify endpoint connectivity.
- Check expected request schema.
- For self-hosted NIM, check GPU/runtime readiness from actual deployment health, not a guessed GPU-name rule.
- Mark unavailable models as unavailable; do not fake success.
- Record official documentation URL and verification date for each enabled model.

## 6. Structured output

Every provider adapter must normalize outputs into internal Pydantic schemas. Preserve the raw response only when needed for debugging and redact sensitive fields. Use schema validation, bounded retries for malformed output, and explicit failed status if the provider cannot satisfy the contract.

## 7. Cost and usage

Record provider, model, task, input/output units where available, source duration, frame count, latency, retry count, estimated/actual cost, currency and pricing verification date. Support budgets per workspace/job. Do not use stale hardcoded model prices.

## 8. Model benchmark

Benchmark identical sample assets and prompt versions. Human editorial annotations are the reference. Compare: candidate relevance, boundary accuracy, standalone comprehension, context preservation, language/transcript alignment, diversity, latency, failure rate and cost per usable clip. Do not call editorial score a probability of virality.
