---
name: social-publishing
description: "Implement official OAuth-based Instagram Reels and YouTube Shorts publishing with approval policies, scheduling safety and duplicate prevention."
argument-hint: "[phase, feature, or slice ID]"
---

# Social Publishing

Use only for official platform integrations, publishing, scheduling, analytics and account management.

## Instagram
Use the current official Meta Instagram Platform/Graph API. Verify supported professional account type, permissions, app review, media container workflow, URL accessibility, media requirements, status polling and publish endpoint before implementation.

## YouTube
Use official YouTube Data API OAuth and supported upload/resumable upload workflow. Verify quota, privacy behavior, Shorts classification and API policies. Do not assume a `publishAt` or scheduled upload capability without checking the current API requirements; implement internal scheduling where needed.

## Safety and reliability
- Never collect platform passwords.
- Never use browser automation/scraping to publish.
- Use OAuth; encrypt refresh/access tokens and redact them from logs.
- Require rights declaration and policy checks.
- Manual approval is default until user enables auto mode.
- Support per-channel and per-category policy.
- Enforce configured score/QA gates and frequency limits.
- Use idempotency keys, durable attempt records and reconciliation before retry after uncertain network outcomes.
- Persist platform IDs and raw non-sensitive status responses.
- Distinguish mock/sandbox tests from real connected-account tests.

A scheduled post must not depend on the frontend being open. PostgreSQL is source of truth; use transactionally claimed jobs/outbox and a worker.

