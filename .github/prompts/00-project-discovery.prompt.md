# Phase 00 — Repository and Environment Discovery

Use the `engineering-gates` skill. This phase is READ-ONLY.

Inspect the current repository and development environment for AI AutoClip Studio. Do not create, modify, delete or format files. Do not install dependencies or call paid APIs.

Inspect:
- Git status, current branch, recent commits, uncommitted changes.
- Existing frontend/backend/frameworks and folder conventions.
- Existing database, queue, worker, storage and deployment configuration.
- Existing AI providers, prompts, video pipeline, integrations, tests and docs.
- Existing `.github` customizations and any AGENTS.md.
- Available runtimes/versions and test/lint/type-check commands.
- NVIDIA GPU visibility if available (`nvidia-smi` only; do not install drivers or alter environment).
- Environment variable names only; never print secret values.
- The supplied AutoShorts repository as reference only; verify repository state and licence, and do not copy code.

Product baseline:
- Mixed authorized video sources.
- Hybrid local/cloud AI.
- NVIDIA API Catalog and optional NIM, Gemini, OpenAI, Anthropic, Groq, Deepgram, Ollama/Qwen and WhisperX.
- Content categories: podcasts/interviews, educational/technical, gaming, entertainment/funny.
- Instagram Reels and YouTube Shorts.
- Manual, policy-based automatic and hybrid publishing.

Return:
1. Repository inventory with paths.
2. Existing architecture summary.
3. Working vs incomplete capabilities.
4. Detected stack/runtime/hardware facts.
5. Current test commands and baseline results only if actually run.
6. Risks, unknowns and constraints.
7. Recommended next phase.

Do not propose a rewrite before understanding what already exists. End `GATE: DISCOVERY COMPLETE — NO FILES CHANGED`.


Global rules: Follow `.github/copilot-instructions.md` and the relevant skills. Inspect existing repository state before edits. Do not invent API/model facts. Keep the scope of this prompt only. Do not advance to the next phase automatically. End with a gate report and explicit status.
