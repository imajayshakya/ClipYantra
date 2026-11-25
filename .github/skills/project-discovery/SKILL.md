---
name: project-discovery
description: Read-only inventory of the existing ClipYantra repository and constraints.
---

# Project Discovery

Perform Phase 0 discovery only.

1. Read `AGENTS.md`, `.github/copilot-instructions.md` and documentation index.
2. Inspect `git status --short`, branch, recent commits and repository tree.
3. Inspect existing source, configuration, dependencies, migrations, tests, CI, Docker and deployment files.
4. Identify actual GPU/hardware only from evidence available in the environment; if unavailable, list required commands for the owner to run.
5. Compare existing implementation with `docs/01-PRODUCT-REQUIREMENTS.md` and `docs/02-ARCHITECTURE.md`.
6. Identify conflicts, duplicates, unfinished integrations and current test commands.
7. Produce `docs/DISCOVERY-REPORT.md` only if documentation file creation is authorized; otherwise return the report in chat.

STRICT: read-only. Do not install packages, edit files, scaffold, modify migrations, run destructive commands or contact production services. Finish with `NEEDS APPROVAL` and ask for one next decision.