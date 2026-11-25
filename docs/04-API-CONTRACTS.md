# API Contracts — ClipYantra

**Status:** FROZEN v1 - Phase 10; approved by `APPROVE CONTRACTS v1`

## 1. API conventions

- Base prefix: `/api/v1`.
- JSON request/response schemas, validated with Pydantic.
- UUID IDs; timestamps are ISO-8601 UTC.
- Use pagination (`limit`, `cursor`) for collections.
- Use consistent errors: `code`, `message`, `details`, `request_id`.
- Long-running operations return `202 Accepted` with `job_id` and status URL.
- SSE endpoint provides progress events; reconnect must use event IDs or a refetch fallback.
- All resource endpoints enforce workspace and resource authorization.

## 2. Proposed endpoint groups

| Method | Route | Purpose |
|---|---|---|
| POST | `/workspaces` | Create workspace |
| GET | `/workspaces/{id}` | Read workspace |
| POST | `/sources/uploads` | Create upload session |
| POST | `/sources` | Register authorized URL/import |
| POST | `/sources/url` | Register direct authorized media URL |
| POST | `/sources/azure` | Register authorized Azure Blob import |
| POST | `/sources/watched-folders` | Configure or scan a watched folder |
| POST | `/sources/platform` | Start authorized official-platform import |
| GET | `/sources` | List source videos |
| GET | `/sources/{id}` | Source details |
| POST | `/sources/{id}/process` | Start pipeline |
| GET | `/jobs/{id}` | Durable job status |
| GET | `/jobs/{id}/events` | SSE progress stream |
| GET | `/sources/{id}/transcript` | Read transcript |
| GET | `/candidates` | Cross-source candidate list |
| GET | `/sources/{id}/candidates` | List candidates |
| POST | `/candidates/{id}/accept` | Accept candidate and create draft |
| POST | `/candidates/{id}/reject` | Reject candidate |
| POST | `/candidates/{id}/render` | Create clip version/render job |
| GET | `/clips/{id}` | Read clip version |
| GET | `/exports` | List rendered assets |
| GET | `/exports/{id}` | Read render/QA status |
| PATCH | `/clips/{id}/draft` | Update validated draft graph |
| POST | `/clips/{id}/edit-operations` | Apply allow-listed edit op |
| POST | `/clips/{id}/undo` | Undo one operation |
| POST | `/clips/{id}/redo` | Redo one operation |
| POST | `/clips/{id}/qa` | Run QA |
| POST | `/clips/{id}/approvals` | Record approval/rejection |
| GET | `/social/accounts` | List connected accounts |
| POST | `/social/oauth/{provider}/start` | Begin OAuth |
| GET | `/social/oauth/{provider}/callback` | OAuth callback |
| POST | `/social/accounts/{id}/disconnect` | Disconnect account and revoke as permitted |
| POST | `/publishing/posts` | Create publish draft |
| POST | `/publishing/posts/{id}/schedule` | Schedule post |
| POST | `/publishing/posts/{id}/cancel` | Cancel post |
| POST | `/publishing/posts/{id}/reconcile` | Reconcile unknown platform outcome |
| GET | `/calendar` | Calendar view |
| GET | `/calendar/queue` | Reconciliation and pending publish queue |
| GET | `/published` | Published post list |
| GET | `/published/{id}` | Published post and available analytics |
| GET | `/analytics` | Analytics summary |
| GET/PATCH | `/brands` | Brand profiles and reusable assets |
| GET/PATCH | `/settings/providers` | Provider config metadata (never expose secrets) |
| GET/PATCH | `/settings/provider-routing` | Workspace/profile/job routing precedence |
| GET/PATCH | `/settings/workspace` | Workspace timezone, retention and owner settings |
| GET | `/audit` | Audit history for rights, approval, provider and publishing |

## 3. Example: create processing job

Request:

```json
{
  "source_video_id": "uuid",
  "profile": "podcast_interview",
  "clip_count_target": 8,
  "duration_policy": {"min_seconds": 20, "max_seconds": 60},
  "ai_profile": "balanced",
  "output_presets": ["vertical_9_16"],
  "language_policy": "auto"
}
```

Response (`202`):

```json
{
  "job_id": "uuid",
  "status": "queued",
  "status_url": "/api/v1/jobs/uuid",
  "events_url": "/api/v1/jobs/uuid/events"
}
```

## 4. Progress event contract

Event names: `job.started`, `stage.started`, `stage.progress`, `stage.completed`, `job.warning`, `job.failed`, `job.completed`.

Common fields: `event_id`, `job_id`, `source_video_id`, `stage`, `progress_percent`, `message_code`, safe display message, timestamp. Do not send secrets, raw provider payloads or full private transcript through generic progress events.

## 5. Edit operations contract

Natural-language AI edit requests must produce a validated list of typed operations, e.g. `TrimRange`, `SetAspectRatio`, `SetCropKeyframes`, `UpdateCaptionText`, `SetCaptionStyle`, `AddBrollCue`, `AdjustAudioGain`, `AddZoomEffect`. Server validates values against allow-lists and timeline bounds. Do not execute model-generated code or raw FFmpeg strings.

## 6. API contract governance

- Keep OpenAPI generated from actual FastAPI schemas.
- Store example requests/responses in tests.
- Breaking changes require versioning or an approved migration plan.
- Contract freeze occurs only after `APPROVE CONTRACTS v1`.

## 6.1 Frozen request/response names

Candidate freeze names:

- `SourceCreateRequest` / `SourceCreateResponse`
- `ProcessingJobCreateRequest` / `ProcessingJobResponse`
- `TranscriptResponse`
- `CandidateListResponse`
- `DraftUpdateRequest` / `DraftResponse`
- `EditOperationRequest` / `EditOperationResponse`
- `RenderCreateRequest` / `RenderResponse`
- `ApprovalRequest` / `ApprovalResponse`
- `PublishPostRequest` / `PublishPostResponse`
- `ProviderRoutingPolicyRequest` / `ProviderRoutingPolicyResponse`
- `ErrorResponse`

The actual Pydantic field and enum names are frozen in the contract freeze document.

## 6.2 Error contract

Every API error returns:

```json
{
  "code": "JOB_NOT_FOUND",
  "message": "The requested processing job was not found.",
  "details": {},
  "request_id": "uuid"
}
```

Rules:

- `details` is an object, not a free-form string;
- validation details use stable field/error-code entries;
- secrets, provider tokens and private transcript payloads are never included;
- HTTP 400/422 maps validation and illegal state;
- HTTP 401/403 maps authentication/authorization/rights;
- HTTP 409 maps optimistic conflict or duplicate active side effect;
- HTTP 429 maps provider/quota limits;
- HTTP 503 maps unavailable storage/provider/worker with retry guidance.

## 6.3 Contract freeze invariants

- UUIDs are strings in JSON.
- timestamps use ISO-8601 UTC storage and API response values.
- source-relative time values use milliseconds or an explicit unit field.
- clip-relative time values are namespaced and not mixed with source time.
- enum values are stable, lower-snake-case strings.
- Pydantic validates unknown fields according to the approved strictness policy.
- list responses use `{items,total,next_cursor}` or an approved pagination envelope.
- 202 responses include status URL and events URL where applicable.
- 204 is used only for operations with no response body.
- OpenAPI examples must match Pydantic schemas.
