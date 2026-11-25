# Analytics and Learning Loop

**Status:** PROPOSED

## 1. Goal

Connect actual clip performance to the creative decisions that produced it, so the product can give evidence-based recommendations. Analytics are not proof that an AI score predicts reach.

## 2. Data model

Analytics snapshot: platform, account, external post ID, metric name, metric value, metric period/window, captured_at, provider response reference, API version and availability state.

Creative metadata: source ID, candidate ID, category, transcript language, duration, hook type, caption style, framing mode, edit version, provider/model, prompt version, publishing time and schedule policy.

## 3. Metrics

Collect only metrics the connected platform/API exposes for that account and permission. Examples may include views/plays, likes, comments, shares, saves, reach, impressions, watch time, average view duration and retention. Preserve metric definitions and API version because platforms change metric names and meanings.

## 4. Collection schedule

- Initial capture after successful publication.
- Follow-up snapshots at configurable intervals (e.g. 1h, 12h, 24h, 72h), subject to API quotas and platform metric availability.
- Backfill/reconcile missing snapshots.
- Stop polling after retention/collection window or API access is revoked.

## 5. Learning loop

- Compare content categories and creative variables within similar cohorts.
- Account for sample size and timing differences.
- Avoid overfitting on one high-performing clip.
- Separate correlation from causal claims.
- Produce recommendations with evidence, sample size and confidence.
- Keep human review before automatically changing creative policies.

## 6. Dashboards

- Channel overview.
- Published content table.
- Per-clip performance timeline.
- Category/hook/duration/caption comparison.
- Provider and rendering cost vs usable clip output.
- Recommendations and experiment history.

## 7. Privacy and platform rules

Respect platform analytics permissions, rate limits, data retention and user disconnect/deletion requests. Never scrape private analytics pages.
