# AI AutoClip Studio (ClipYantra) — Agent Instructions

This file is shared project guidance for compatible coding agents. See `.github/copilot-instructions.md` for the more detailed Copilot-specific rules.

## Project
AI AutoClip Studio which named as ClipYantra ingests user-owned/authorized video, transcribes and analyzes it with a hybrid local/cloud AI stack, generates short clips, supports review, and publishes approved content to Instagram Reels and YouTube Shorts.

## Default architecture direction
Next.js/TypeScript, FastAPI/Python, PostgreSQL, Redis/Celery, FFmpeg/OpenCV/PySceneDetect, local/Azure Blob storage; modular AI adapters for NVIDIA, Gemini, OpenAI, Anthropic, Groq, Deepgram, Ollama/Qwen and WhisperX. Confirm the existing repository before changing it.

## Required work sequence
Discovery → requirements → architecture → risk/outcome analysis → explicit human design approval → contracts/data model → placeholder-only scaffold → bounded implementation slices → tests and independent review → human approval to continue.

Never infer approval. Never jump from discovery into application code. Implement one approved slice at a time. If requirements or architecture materially change, record an ADR and obtain renewed approval.

## Quality and safety
- Inspect existing work and `git status` before edits; preserve user changes.
- No fabricated test results, fake provider integrations or publishing success.
- Verify current provider/platform documentation before implementation.
- Validate every AI-generated schema/timestamp and every rendered media asset.
- Use official OAuth APIs for social publishing.
- Protect credentials and user media.
- Keep workflows idempotent and recoverable.
- Tests accompany every behavior change.
- Report scope, changed files, test evidence, gaps and gate status after each task.
