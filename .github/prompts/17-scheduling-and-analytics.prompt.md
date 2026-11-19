# Feature Phase — Scheduler, Hybrid Policies and Analytics

Use `social-publishing` and `testing-verification`.

Implement database-backed scheduling, configured timezone (default Asia/Kolkata), per-platform/per-channel/per-category cadence, manual/automatic/hybrid policies, minimum QA/editorial gates, post calendar, cancellation/rescheduling, rate-limit handling, duplicate protection and audit history.

Use PostgreSQL durable state, transactional claiming/leases and an outbox to dispatch Celery tasks. Reconcile external publishing outcomes before retries. Scheduler must work with frontend closed. Store platform metrics as timestamped snapshots, distinguish views/engaged views where APIs do, and record metric availability. Link analytics to source video, clip, prompt/model version, hook/category/duration and post ID. No unsupported analytics fields or causal claims. Stop at gate.


Global rules: Follow `.github/copilot-instructions.md` and the relevant skills. Inspect existing repository state before edits. Do not invent API/model facts. Keep the scope of this prompt only. Do not advance to the next phase automatically. End with a gate report and explicit status.
