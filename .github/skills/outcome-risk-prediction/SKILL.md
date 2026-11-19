---
name: outcome-risk-prediction
description: "Estimate likely delivery outcomes, technical risks, cost and latency drivers, quality uncertainties and validation experiments without making unsupported promises."
argument-hint: "[phase, feature, or slice ID]"
---

# Outcome and Risk Prediction

Use after architecture design and before design approval. Treat predictions as hypotheses, not facts.

For each subsystem assess:
- Feasibility: high/medium/low and why.
- Confidence: high/medium/low, based on evidence.
- Main dependencies and unknowns.
- Quality risks and likely failure modes.
- Latency and cost drivers; provide formulae or measurement plans rather than invented prices.
- Hardware constraints and what must be detected at runtime.
- External API permissions, quotas, review and policy dependencies.
- Operational complexity and recovery requirements.

For this product explicitly assess:
- Transcription quality for English, Hindi and Hinglish.
- Long-video chunking and timestamp drift.
- Podcast speaker diarization.
- Gaming event detection and sampling density.
- Comedy setup/punchline completeness.
- NVIDIA modality/model endpoint compatibility and GPU feasibility.
- LLM selection quality versus human editor baseline.
- FFmpeg render quality and throughput.
- Instagram/YouTube OAuth/publishing constraints.
- Copyright/source rights and media URL security.

Provide:
1. Outcome scenarios (conservative/base/optimistic) with assumptions.
2. Confidence and evidence for each prediction.
3. Risk register: probability, impact, detectability, mitigation, owner.
4. Benchmark plan using a representative test corpus.
5. Go/no-go criteria for the next phase.

Do not invent API prices, exact processing times, model limits or success percentages. Mark unknowns as TBD and propose how to measure them.
