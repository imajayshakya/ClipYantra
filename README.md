# AI AutoClip Studio (ClipYantra) — VS Code Copilot Engineering Kit

This kit configures a gated, step-by-step AI-assisted development workflow for AI AutoClip Studio.

## Product baseline

- Mixed source ingestion: user-owned or authorized uploads, direct media URLs, cloud storage imports, watched folders, and supported platform imports.
- Hybrid AI: local processing plus selectable cloud providers.
- Providers: NVIDIA (API Catalog and optional self-hosted NIM), Gemini, OpenAI, Anthropic, Groq, Deepgram, Ollama/Qwen, WhisperX.
- NVIDIA model family candidates: Nemotron multimodal/video, Nemotron vision-language, Nemotron text reasoning, and Nemotron Transcribe. Model IDs and capabilities must be verified against current official documentation at implementation time; do not assume a model supports a modality because its family name suggests it.
- Content profiles: Podcasts/Interviews, Educational/Technical, Gaming, Entertainment/Funny.
- Outputs: vertical clips suitable for Instagram Reels and YouTube Shorts, plus configurable square/landscape exports where useful.
- Publishing: manual approval, policy-based automatic publishing, and hybrid per-channel/per-category rules.
- Platform publishing must use official APIs and authorized OAuth flows.
- AutoShorts (https://github.com/JayWebtech/autoshorts) is an architecture/UX reference only until its licence is explicitly verified. Do not copy its source code or assume its import feature is a publishing API.

## Install in an existing repository

1. Back up or commit your current work.
2. Copy the `.github/` folder from this kit into the root of your AI AutoClip Studio repository. Merge carefully if `.github/` already exists; do not overwrite existing workflows or instructions without reviewing the diff.
3. Optionally copy `AGENTS.md` to your repository root. Merge it with an existing file rather than replacing it.
4. Open the repository root in VS Code.
5. Select the **Copilot** agent harness in the Chat/Agents view. Choose Agent mode.
6. Check that the Workspace customizations show the agents, prompts and skills. Use Command Palette → `Chat: Open Customizations` to inspect them.
7. Start a fresh Copilot session after installing or changing customizations.

## Run the workflow in order

Invoke these prompt files one at a time from Copilot Chat:

1. `/00-project-discovery`
2. `/01-product-requirements`
3. `/02-architecture-design`
4. `/03-outcome-risk-prediction`
5. `/04-design-approval-gate`
6. `/05-contracts-and-data-model`
7. `/06-scaffold-only`
8. `/07-slice-plan`
9. `/08-implement-one-slice`
10. `/09-independent-test-review`
11. `/10-phase-gate-and-next-slice`

After the foundation, use the feature prompts in order:

12. `/11-video-ingestion`
13. `/12-transcription-and-alignment`
14. `/13-ai-highlight-discovery`
15. `/14-rendering-and-quality`
16. `/15-clip-review-studio`
17. `/16-social-publishing`
18. `/17-scheduling-and-analytics`
19. `/18-production-readiness`

Do not run every prompt in one message. Each phase must finish with evidence and a gate report. The human owner approves each gate explicitly.

## Approval protocol

Copilot must stop at each approval gate. Use an exact approval message such as:

`APPROVE DESIGN v1`

or

`APPROVE SLICE <ID>`

Do not treat silence, a request for explanation, or a model's recommendation as approval. If a material requirement changes, revise the affected design artifacts and ask for approval again.

## Multi-model review

Use Copilot as the main coordinator. For a second opinion, open the same reviewed artifacts in another supported model/harness (for example a Claude or Codex session) and ask it to act as an independent reviewer. Ask for findings only; do not let multiple agents modify the same files or branch concurrently. Reconcile disagreements in an Architecture Decision Record (ADR).

A model selected in the model picker does not necessarily change the agent harness. The harness determines which customization files and tools are loaded. Keep the primary session on the Copilot harness when relying on this `.github/` kit.

## Important rules

- The agent must inspect the repository before proposing changes.
- No application code before design approval.
- No production feature code during scaffold-only phase.
- Implement one bounded vertical slice at a time.
- Tests must be written or updated with every behavior change.
- Never claim tests passed unless the command was executed and the result was inspected.
- Do not silently change approved architecture.
- Keep secrets out of source control and frontend code.
- Verify changing API/model documentation before implementation; cite URLs and access dates in project docs.
- Do not invent NVIDIA model IDs, modalities, context limits, GPU requirements, prices, or API compatibility. Verify live documentation.
- Use authorized source media only. Respect platform terms, licensing, privacy and copyright.
