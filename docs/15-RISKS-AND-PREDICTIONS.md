# Risks, Assumptions and Outcome Predictions

**Status:** IN PROGRESS - Phase 08 prediction baseline  
**Version:** v1  
**Date:** 2026-11-23

This is a hypothesis register, not a numerical forecast. The operational owner and mitigation list is maintained in [docs/engineering/RISKS.md](engineering/RISKS.md).

## 1. Evidence classes

- **Measured fact:** observed in repository discovery or a confirmed Product Owner Decision v1.
- **Documented assumption:** a proposed architecture or implementation choice with a stated uncertainty.
- **Hypothesis:** an expected outcome that requires benchmark or user evidence.

No throughput, cost or quality success rate is claimed until measured.

## 2. Measured facts

| Fact | Source | Consequence |
|---|---|---|
| The repository is documentation/customization-heavy and has no package manifest or application source found during discovery | Repository discovery | No UI primitive or runtime dependency is selected |
| Development hardware is AMD Ryzen 5 3500U with Vega 8 integrated graphics and 6 GB RAM | Discovery | NVIDIA/CUDA local inference cannot be assumed |
| PostgreSQL is proposed as authoritative workflow state | Requirements/architecture proposals | Redis/Celery is execution infrastructure |
| MVP is Docker-based, single-owner/workspace and SaaS-ready | Product Owner Decision v1 | Future tenancy must be isolated without a rewrite |
| MVP supports local uploads, direct authorized URLs, Azure Blob, watched folders and authorized platforms | Product Owner Decision v1 | Adapter architecture is required |
| MVP publishes to Instagram/Facebook Reels and YouTube Shorts through official APIs | Product Owner Decision v1 | Separate Meta and YouTube adapters are required |
| Routing precedence is workspace default, then profile override, then per-job override | Product Owner Decision v1 | Resolver and audit record are required |
| Tablet supports management/review; full timeline is desktop-first | Product Owner Decision v1 | No desktop parity promise on tablet |

## 3. Documented assumptions

| Assumption | Why it is not a fact | Validation |
|---|---|---|
| Redis/Celery fits MVP operations | No implementation benchmark or alternative test exists | Queue depth, lease and failure benchmark |
| Docker on the owner host has enough CPU/RAM/disk for all worker classes | Hardware/resource allocation is unknown | Docker resource and media benchmark |
| Azure Blob is the preferred cloud object adapter | Blob credentials/storage topology are not frozen | Storage contract and failover benchmark |
| Official provider APIs can satisfy the adapter contracts | Current official model IDs and limits require verification | Provider contract tests and official-doc verification date |
| SSE plus durable status refetch is sufficient realtime UX | Browser/load behavior is not measured | Reconnect, proxy and event-order benchmark |
| Full Clip Studio can be delivered through typed operations and source maps | Source-map complexity is not implemented | Small vertical slice and edit/failure tests |

## 4. Outcome risk register

| ID | Hypothesis / prediction | Likelihood | Impact | Confidence | Leading indicator | Mitigation / evidence required |
|---|---|---|---|---|---|---|
| R-001 | Reusing SupoClip source patterns may create licence obligations | Medium | Critical | High | Source comparison or copied substantial text/code | Legal/licence review; architecture ideas only |
| R-002 | Local Ollama/NIM/WhisperX inference may be too slow or memory-heavy on Vega 8 | High | High | High | OOM, VRAM, latency and duration benchmark | Cloud/balanced defaults; no GPU assumption; benchmark |
| R-003 | 6 GB RAM plus Docker will cause worker or system exhaustion | High | High | High | OOM events, swap, worker restart and queue age | Hard limits, separated workers, bounded concurrency |
| R-004 | Local Docker orchestration may not isolate CPU/media/AI workers enough | Medium | High | Medium | Resource contention and temp-disk pressure | Compose resource limits and dedicated worker pools |
| R-005 | Watched-folder ingestion may miss, duplicate or replay sources | Medium | High | Medium | Missing/duplicate ledger and restart findings | Cursor/checksum, leases and quarantine |
| R-006 | Azure import/credential handling may create SSRF or secret exposure | Medium | Critical | Medium | SSRF test, secret scan or redirect leak | Server credentials, redirect validation and short-lived access |
| R-007 | Direct URL/platform imports may violate rights or platform restrictions | Medium | Critical | High | Unsupported source or terms-change report | Rights gate, official adapters only, block disallowed sources |
| R-008 | Meta/YouTube app review or account eligibility may delay publishing | High | High | Medium | Account permission and test-app status | Separate adapters, sandbox/test accounts and staged publishing |
| R-009 | Platform API quotas/changes may block publishing or reconciliation | Medium | High | High | 429/5xx, deprecation and permission change | Backoff, pause, capability profiles and official-doc version |
| R-010 | Unknown publish outcomes may be retried as duplicates | Medium | Critical | High | Timeout injection and duplicate discovery | Idempotency key, reconciliation state and no blind retry |
| R-011 | Routing precedence/fallback may select the wrong provider | Medium | High | High | Routing scenario mismatch | Central resolver, audit, capability validation and tests |
| R-012 | Cloud multimodal cost/latency may exceed user tolerance | Medium | High | Medium | Cost per hour, p95 latency and provider failures | Signal-first sampling, budget, cache and fallback |
| R-013 | Transcript quality may vary by language, accent or noise | Medium | Medium | High | Alignment, word-error and speaker-fixture results | Compare providers and allow correction/uncertain state |
| R-014 | Candidate quality may vary by content profile | High | High | High | Human-labelled relevance/boundary/results | Profile benchmark and evidence validator |
| R-015 | Gaming moments may be missed by sparse sampling | High | High | High | Gaming fixture recall and event misses | Event-triggered sampling and denser keyframe indexing |
| R-016 | Render throughput/memory may not scale for representative source duration | Medium | High | Medium | Render duration, memory/disk and queue age | Dedicated worker, proxy workflow and bounded concurrency |
| R-017 | Caption/crop validation may fail platform safe-margin rules | Medium | High | High | Pixel/codec/QA fixture failure | Platform presets, FFprobe/FFmpeg validation and visual regression |
| R-018 | AI edit operations may alter meaning or remove context | Medium | High | Medium | Rejected context and preview-diff fixture | Typed operations, bounds, preview, confirmation and undo |
| R-019 | B-roll/font/music rights metadata may be incomplete | Medium | High | Medium | Missing provenance or license audit | Asset registry, declaration and fail-soft behavior |
| R-020 | Tenant/workspace/brand isolation may leak future SaaS data | Medium | Critical | Medium | Cross-workspace query test | Workspace-scoped repositories and isolation fixtures |
| R-021 | Secrets or transcripts may appear in logs/browser payloads | Medium | Critical | High | Secret scan, network and log review | Server-side secrets, redaction and telemetry policy |
| R-022 | Media/transcript retention may conflict with user/legal policy | Medium | High | Medium | Deletion/retention audit | Configurable retention, explicit purge and audit |
| R-023 | Analytics metric names or versions may differ across platforms | Medium | High | High | Adapter fixture mismatch | Versioned definitions and unavailable-metric state |
| R-024 | Live-stream/dubbing scope may leak into MVP inadvertently | Low | Medium | High | Deferred feature references in routes/contracts | Explicit scope boundary and no coupled implementation |
| R-025 | Acceptance criteria remain below measurable coverage | High | High | High | Requirements with no AC/test mapping | AC expansion and traceability before contracts |
| R-026 | Architecture/API/data/contract documents drift | Medium | High | High | Contradictory endpoint/state/provider/storage names | Consolidated review and contract freeze |
| R-027 | Clip Studio implementation may exceed a small-slice model | High | High | Medium | Source-map defects and estimate variance | Small vertical slices, immutable sources and independent verification |
| R-028 | Tablet editing UI may imply desktop timeline parity | Medium | Medium | High | Unsupported control or usability findings | Visible desktop-only boundary and numeric alternatives |

## 5. Benchmark plan

No benchmark result is claimed without execution.

### 5.1 Fixture profiles

| Profile | Fixture characteristics | Required evidence |
|---|---|---|
| Podcast/interview | 20-60 minute source, multiple speakers, Q&A and long answers | Transcript alignment, candidate completeness and context |
| Educational/technical | 20-120 minute source, code/demo and terminology | Technical context preservation and word timing |
| Gaming | 20-60 minute source, event spikes, facecam and gameplay | Event sampling recall and render legibility |
| Entertainment/funny | 10-30 minute source, setup/punchline/reaction | Payoff preservation and caption/crop usability |

### 5.2 Benchmarks

- hardware inventory and Docker resource envelope;
- local ASR, WhisperX and optional Ollama/NIM startup/memory;
- cloud ASR/transcription cost and latency;
- candidate relevance and boundary overlap against human annotations;
- provider disagreement and fallback;
- FFprobe/FFmpeg render throughput and memory/disk;
- 9:16 caption/crop safe margin and codec validation;
- OAuth/sandbox publish/reconcile duplicate and timeout cases;
- worker crash, retry and checkpoint recovery;
- SSE reconnect and durable status refetch;
- tablet and mobile usability at 768/390/360 px.

### 5.3 Required metrics

- source duration and resolution;
- provider/model/prompt version;
- audio/video stage duration;
- memory/VRAM/disk use;
- retry/failure count;
- cost per source hour where available;
- candidate boundary overlap;
- human completeness verdict;
- publish reconciliation outcome;
- defect severity and accessibility evidence.

The benchmark plan must not hardcode success thresholds until representative fixtures are measured and approved.

## 6. Architecture recommendations

1. Start with upload, rights, FFprobe, PostgreSQL job, Redis/Celery checkpoint and SSE.
2. Use cloud ASR/candidate providers for MVP until local AMD feasibility is measured.
3. Keep media workers isolated from API and publishing processes.
4. Freeze provider capability metadata through versioned contract tests.
5. Implement publish only after clip QA and approval states are stable.
6. Keep tablet and mobile UI review-focused for MVP.
7. Complete AC/traceability and architecture contracts before slice implementation.

## 7. Gate status

**Current status:** NEEDS APPROVAL - architecture and risk baseline requires review against the resolved product-owner decisions and benchmark plan.
