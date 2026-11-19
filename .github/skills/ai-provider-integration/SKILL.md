---
name: ai-provider-integration
description: "Design, implement and verify pluggable AI provider adapters, with NVIDIA/Nemotron as a first-class provider and capability-checked routing."
argument-hint: "[phase, feature, or slice ID]"
---

# AI Provider Integration

Use for any AI provider/model integration or routing change.

## Required abstraction
- Provider adapter interface.
- Model registry with verified capability metadata.
- Task-to-model routing policy.
- Structured input/output schemas.
- Timeout, retry, cancellation and rate-limit handling.
- Secret management.
- Usage/cost/latency telemetry where provider returns it.
- Provider health/capability checks.
- Fallback policy and clear degraded status.

## Providers in product scope
NVIDIA API Catalog, optional NVIDIA NIM; Gemini; OpenAI; Anthropic; Groq; Deepgram; Ollama/Qwen; WhisperX/local ASR.

## NVIDIA requirements
Treat hosted NVIDIA API Catalog and self-hosted NVIDIA NIM as separate deployment adapters unless current docs prove compatibility. Verify each exact model ID, endpoint, request/response schema, modalities, language support, video/audio limits, context limits, streaming and GPU requirements from official NVIDIA docs at implementation time. Candidate families include Nemotron multimodal/video, vision-language, text reasoning and Nemotron Transcribe; do not assume capabilities from family naming.

Never route audio/video to a text-only model. Never route Hindi/Hinglish transcription to a model documented as English-only. For long video, chunk or sample according to verified model limits and preserve source timestamps. For gaming, design event-triggered/dense frame sampling tests.

## Provider testing
- Unit tests with mocked transport.
- Schema contract tests.
- Invalid/missing credential handling.
- Timeout, 429, 5xx and malformed response handling.
- Capability mismatch rejection.
- Fallback behavior.
- Optional live smoke test only when credentials are provided.

Never log API keys, raw private media, or sensitive transcript content by default.
