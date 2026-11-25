# Publishing and Scheduling

**Status:** PROPOSED — current platform APIs/permissions must be verified before implementation

## 1. Platforms

- Instagram Reels through the official Meta API for eligible professional accounts and approved permissions.
- Facebook Reels only through the applicable supported Meta publishing APIs and page/account permissions.
- YouTube Shorts through the official YouTube Data API upload flow; Short classification follows YouTube's current rules.

Do not promise that every personal account, content type or region is eligible. Verify permissions and publishing limits in official documentation at implementation time.

## 2. OAuth and credentials

- OAuth state/nonce and redirect validation.
- Least-privilege scopes.
- Encrypted token storage or secret-manager references.
- Refresh/reconnect handling.
- Token revocation and disconnect workflow.
- Never log tokens or send them to frontend clients.

## 3. Publishing state machine

`draft → awaiting_approval → scheduled → claimed → uploading → platform_processing → published`

Other states: `retry_wait`, `unknown_outcome`, `failed`, `cancelled`, `needs_reconnect`, `rejected`.

## 4. Scheduling architecture

- PostgreSQL is source of truth for due posts.
- Scheduler claims rows transactionally using locking/leases.
- Transactional outbox dispatches publish events.
- Workers call provider adapter.
- Store request hash, idempotency key, attempt number and platform response reference.
- On unknown outcome, query/reconcile provider state before retrying.
- Use UTC internally; display with account/workspace timezone.

## 5. Policy modes

- Manual: only an explicit human approval publishes.
- Automatic: only if user opts in and every policy predicate passes.
- Hybrid: policy selected per channel/category.

Automatic policy predicates can include rights verified, QA passed, score threshold, approved template, allowed category, platform metadata valid, posting quota, schedule window and connected account.

## 6. Platform-specific validation

Validation rules must be configured from current official documentation and may include duration, aspect ratio, container, codecs, frame rate, audio, caption, title/description and privacy requirements. Do not hardcode stale limits in multiple code paths; use versioned platform profiles.

## 7. Failure and duplicate handling

- Unique logical publish idempotency key.
- Platform upload IDs/session IDs persisted where available.
- Reconcile interrupted uploads.
- Never blindly repeat a publish call after a timeout.
- Distinguish upload accepted, processing, published and failed.
- Provide retry only when outcome is known safe.

## 8. Audit trail

Record who connected account, which policy was active, which clip version was approved, metadata sent, schedule, attempt result and resulting platform ID/permalink.
