# Feature Phase — Instagram and YouTube Official Publishing

Use `social-publishing` and `testing-verification`. Research the current official APIs at implementation time; record source URLs and verification date.

Instagram: OAuth for eligible professional accounts, permission/app-review awareness, media container creation, media URL availability, status polling and publish call. YouTube: OAuth, resumable upload, metadata/privacy controls and processing status. Implement account connection, token encryption/refresh, publisher adapters, status persistence, attempts and reconciliation. Support mock tests and optional live smoke tests only with explicitly configured credentials.

Do not use browser automation, password collection, scraping or unauthorized media downloading. Never assume a public URL can be processed by a renderer. Require rights declaration and applicable approval policy. Reconcile uncertain upload result before retry to avoid duplicates. Stop at gate.


Global rules: Follow `.github/copilot-instructions.md` and the relevant skills. Inspect existing repository state before edits. Do not invent API/model facts. Keep the scope of this prompt only. Do not advance to the next phase automatically. End with a gate report and explicit status.
