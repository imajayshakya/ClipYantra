# Phase 06 — Placeholder Scaffolding Only

Proceed only after `APPROVE CONTRACTS v1`. Verify approval. Use `scaffold-only`.

Create the minimum approved project skeleton and wiring. Before changes, inspect git status and preserve all existing work.

Allowed: folders, package config, env example, typed interface shells, router registration, database connection scaffolding, migration baseline if approved, worker registration, health endpoints, provider/storage/publisher abstract classes, docs, startup/import smoke tests.

Forbidden: production business logic, real paid model calls, real publishing, fake success responses, unapproved refactors, broad feature implementation. Unimplemented methods must fail explicitly or return disabled/501 states.

For every created module mark its status: `SCAFFOLDED`, `IMPLEMENTED`, or `NOT STARTED`. Run startup/import/lint/type checks. Report exact results and all placeholders. Stop for scaffold review; ask `APPROVE SCAFFOLD v1` before feature code.


Global rules: Follow `.github/copilot-instructions.md` and the relevant skills. Inspect existing repository state before edits. Do not invent API/model facts. Keep the scope of this prompt only. Do not advance to the next phase automatically. End with a gate report and explicit status.
