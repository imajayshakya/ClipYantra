# Feature Phase — Multi-model Highlight Discovery

Use `ai-provider-integration`, `media-pipeline` and `outcome-risk-prediction`.

Build category-specific discovery for podcasts/interviews, educational/technical, gaming and entertainment/funny. Inputs: timestamped transcript, optional diarization, scene boundaries, timestamped frames and audio event cues. Output: schema-validated candidates with precise source start/end, duration, transcript evidence, category, hook, rationale, individual provider scores and confidence.

Compare NVIDIA Nemotron multimodal/video and vision-language candidates, Gemini, OpenAI, Anthropic and local Qwen only where their verified modalities allow. NVIDIA text, vision, video/audio and transcription capabilities must be modeled separately. Honor per-model clip/video limits through segmenting/frame sampling with global timestamp offsets. Gaming uses dense/event-triggered sampling; comedy preserves setup and payoff. Deduplicate overlaps and diversify time coverage. Scores are editorial estimates, not virality probabilities.

Create a human-editor benchmark corpus and metrics for boundary accuracy, context completeness, candidate acceptance and timestamp error. Do not claim superiority without measured results. Stop at gate.


Global rules: Follow `.github/copilot-instructions.md` and the relevant skills. Inspect existing repository state before edits. Do not invent API/model facts. Keep the scope of this prompt only. Do not advance to the next phase automatically. End with a gate report and explicit status.
