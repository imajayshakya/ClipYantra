# Slice PROC-001 — Analysis (Candidate Discovery & Ranking)

**Status:** PLANNED — Awaiting `APPROVE SLICE PROC-001`
**Requirements baseline:** `APPROVE REQUIREMENTS v1`
**Design artifacts:** `APPROVE UX v1`, `APPROVE VISUAL DIRECTION v1`, `APPROVE WIREFRAMES v1`, `APPROVE DESIGN SYSTEM v1`, `APPROVE DESIGN v1`
**Architecture:** `APPROVE ARCHITECTURE v1`
**Contracts:** `APPROVE CONTRACTS v1`
**QE plan:** `APPROVE QE PLAN v1`
**Scope IDs:** FR-014, FR-015, FR-016, FR-017, FR-018, NFR-001, NFR-002, NFR-006, NFR-008
**Depends on:** ING-003 (ACCEPTED), ING-004 (PLANNED)
**Blocks:** PROC-002 (Candidate Generation), EDIT-001 (Clip Studio)
**Owner:** Backend engineer + AI engineer
**Estimated effort:** 5–7 days

---

## 1. Slice overview

| Field | Value |
|---|---|
| Slice ID | PROC-001 |
| Title | Analysis — Candidate Discovery & Ranking |
| Milestone | M2 — AI Processing & Candidate Discovery |
| Depends on | ING-003 (ACCEPTED), ING-004 (PLANNED) |
| Blocks | PROC-002 (Candidate Generation), EDIT-001 (Clip Studio), REN-001 (Rendering) |
| Owner | Backend engineer + AI engineer |
| Estimated effort | 5–7 days |

**Goal:** Transform transcribed + scene-indexed video into ranked clip candidates. Use deterministic low-cost signals to propose candidate windows, then evaluate with multimodal LLMs per content profile. Persist candidates with scores, evidence, and explanations for human review.

**Out of scope:** Rendering (REN-001), Clip Studio editing (EDIT-001/002), publishing (PUB-001+), analytics (AN-001), B-roll generation (future), speaker diarization (ING-005).

---

## 2. User value

Creators get multiple self-contained clip candidates per long video, each with:
- Start/end timestamps snapped to word/scene boundaries
- Editorial rationale (hook, context, payoff, standalone value)
- Profile-specific scores (Podcast, Educational, Gaming, Entertainment)
- Confidence/uncertainty indicators
- Transcript evidence spans
- Model/provider used for traceability

---

## 3. Scope

### In scope
1. **Deterministic candidate proposer** — Fast, cheap window proposals from transcript + scenes + audio signals
2. **Profile-specific evaluator** — Multimodal LLM evaluation per content profile (4 profiles)
3. **Ranking & deduplication** — Score normalization, overlap removal, diversity enforcement
4. **Candidate persistence** — ClipCandidate entity with scores, evidence, status
5. **Model evaluation logging** — ModelEvaluation entity per provider/candidate
6. **Celery job pipeline** — Async, restartable analysis job with progress
6. **API endpoints** — Trigger analysis, get status, list candidates, get candidate detail
7. **Database models & migration** — ClipCandidate, ModelEvaluation tables
8. **Provider integration** — Via existing capability registry (OpenAI, Anthropic, Gemini, NVIDIA)
9. **Tests** — Unit (proposer, evaluator, ranking), Integration (API, job pipeline)

### Out of scope
- Rendering clips (REN-001)
- Clip Studio timeline editing (EDIT-001)
- Caption generation (EDIT-001)
- B-roll insertion (future)
- Publishing (PUB-001+)
- Speaker diarization (ING-005)
- Face tracking (ING-005)
- Real-time/streaming analysis

---

## 4. Prerequisites

| Prerequisite | Status | Notes |
|---|---|---|
| ING-003 ACCEPTED | ✅ | Transcripts + segments available |
| ING-004 PLANNED/ACCEPTED | 🔄 | Scenes + keyframes (can run in parallel; proposer uses scenes if available) |
| Capability registry | ✅ | From ING-003 |
| Transcription providers | ✅ | 5 providers configured |
| ProcessingJobs + outbox | ✅ | From contracts |
| Provider configs/secrets | 🔄 | Workspace-level config needed |

---

## 5. API / Data Impact

### New API endpoints (under `/api/v1/sources/{media_asset_id}/analysis`)

| Method | Path | Purpose |
|---|---|---|
| POST | `/candidates` | Trigger candidate discovery + ranking job |
| GET | `/candidates` | Get analysis job status/progress |
| POST | `/candidates/retry` | Retry failed analysis |
| GET | `/candidates/list` | List clip candidates (paginated, filterable) |
| GET | `/candidates/{candidate_id}` | Get candidate detail with scores/evidence |
| GET | `/candidates/{candidate_id}/evaluations` | List model evaluations for candidate |

### Request/Response schemas

```python
# POST /candidates request
class AnalysisRequest(BaseModel):
    content_profile: Literal["podcast", "educational", "gaming", "entertainment"] = "podcast"
    target_count: int = Field(default=8, ge=1, le=20)  # desired candidate count
    min_duration_sec: int = Field(default=15, ge=5)
    max_duration_sec: int = Field(default=90, le=180)
    provider_hint: Optional[str] = None  # override routing for evaluation
    routing_mode: Literal["local_first", "balanced", "cloud_first", "user_selected"] = "balanced"
    use_scenes: bool = True  # if ING-004 available
    deduplicate_overlap_threshold: float = Field(default=0.3, ge=0.0, le=1.0)  # IoU threshold

# POST /candidates response
class AnalysisResponse(BaseModel):
    job_id: str
    status: Literal["queued", "running"]
    idempotency_key: str

# GET /candidates response
class AnalysisStatusResponse(BaseModel):
    job_id: str
    status: Literal["queued", "proposing", "evaluating", "ranking", "succeeded", "failed", "cancelled"]
    progress: Optional[float] = None  # 0.0-1.0
    candidates_found: int = 0
    candidates_ranked: int = 0
    error: Optional[str] = None

# GET /candidates/list response
class CandidateListResponse(BaseModel):
    candidates: List[ClipCandidateResponse]
    total: int
    page: int
    page_size: int

class ClipCandidateResponse(BaseModel):
    candidate_id: str
    media_asset_id: str
    start_ms: int
    end_ms: int
    duration_ms: int
    content_profile: str
    overall_score: float  # 0.0-1.0 normalized
    scores: Dict[str, float]  # rubric dimensions: hook, context, payoff, standalone, visual, emotional
    confidence: float  # 0.0-1.0
    transcript_evidence: List[TranscriptEvidence]  # segment refs supporting candidate
    scene_evidence: Optional[List[str]] = None  # scene_ids overlapping
    explanation: str  # human-readable rationale
    status: Literal["discovered", "validated", "ranked", "pending_review", "needs_edit", "accepted", "rejected", "duplicate"]
    primary_model: str  # provider/model that produced primary evaluation
    created_at: datetime
    updated_at: datetime

class TranscriptEvidence(BaseModel):
    segment_id: str
    start_ms: int
    end_ms: int
    text: str
    relevance: str  # "hook", "context", "payoff", "standalone"

class ModelEvaluationResponse(BaseModel):
    evaluation_id: str
    candidate_id: str
    provider: str
    model: str
    prompt_version: str
    rubric_scores: Dict[str, float]
    raw_output_ref: Optional[str] = None  # storage key for raw response
    latency_ms: int
    cost_estimate_usd: Optional[float] = None
    created_at: datetime
```

### Database changes

**New table: `clip_candidates`**
```sql
CREATE TABLE clip_candidates (
    candidate_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    media_asset_id UUID NOT NULL REFERENCES media_assets(media_asset_id) ON DELETE CASCADE,
    source_video_id UUID NOT NULL REFERENCES source_videos(source_id) ON DELETE CASCADE,
    start_ms INTEGER NOT NULL,
    end_ms INTEGER NOT NULL,
    content_profile VARCHAR(32) NOT NULL,
    overall_score DECIMAL(4,3) NOT NULL,  -- 0.000-1.000
    scores JSONB NOT NULL,  -- {"hook": 0.8, "context": 0.7, "payoff": 0.9, "standalone": 0.6, "visual": 0.5, "emotional": 0.7}
    confidence DECIMAL(4,3) NOT NULL,
    transcript_evidence JSONB NOT NULL,  -- [{"segment_id": "...", "start_ms": 1000, "end_ms": 5000, "text": "...", "relevance": "hook"}, ...]
    scene_evidence JSONB DEFAULT '[]',  -- [scene_id, ...]
    explanation TEXT NOT NULL,
    status VARCHAR(32) NOT NULL DEFAULT 'discovered',
    analysis_job_id UUID REFERENCES processing_jobs(job_id) ON DELETE SET NULL,
    primary_provider VARCHAR(64),
    primary_model VARCHAR(128),
    primary_prompt_version VARCHAR(64),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT valid_time_range CHECK (end_ms > start_ms),
    CONSTRAINT valid_score_range CHECK (overall_score BETWEEN 0 AND 1),
    CONSTRAINT valid_confidence CHECK (confidence BETWEEN 0 AND 1),
    CONSTRAINT within_source CHECK (end_ms <= (SELECT duration_ms FROM source_videos WHERE source_id = clip_candidates.source_video_id))
);

CREATE INDEX idx_candidates_media_asset ON clip_candidates(media_asset_id);
CREATE INDEX idx_candidates_source_video ON clip_candidates(source_video_id);
CREATE INDEX idx_candidates_status ON clip_candidates(status);
CREATE INDEX idx_candidates_score ON clip_candidates(overall_score DESC);
CREATE INDEX idx_candidates_analysis_job ON clip_candidates(analysis_job_id);
```

**New table: `model_evaluations`**
```sql
CREATE TABLE model_evaluations (
    evaluation_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    candidate_id UUID NOT NULL REFERENCES clip_candidates(candidate_id) ON DELETE CASCADE,
    provider VARCHAR(64) NOT NULL,
    model VARCHAR(128) NOT NULL,
    prompt_version VARCHAR(64) NOT NULL,
    rubric_scores JSONB NOT NULL,  -- same dimensions as clip_candidates.scores
    raw_output_ref VARCHAR(512),  -- storage key for debugging
    latency_ms INTEGER NOT NULL,
    cost_estimate_usd DECIMAL(10,6),
    tokens_input INTEGER,
    tokens_output INTEGER,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_evaluations_candidate ON model_evaluations(candidate_id);
CREATE INDEX idx_evaluations_provider_model ON model_evaluations(provider, model);
```

**Extended `processing_jobs`** (already exists):
- job_kind: add `'candidate_analysis'` to enum/check constraint

---

## 6. Implementation Steps

### Step 1: Database models and migration (Day 1)
- [ ] Add `ClipCandidate` and `ModelEvaluation` SQLAlchemy models in `backend/app/db/models.py`
- [ ] Create Alembic migration `backend/alembic/versions/XXXX_proc001_candidates.py`
- [ ] Add repository methods in `backend/app/db/source_repository.py`:
  - `create_candidate()`, `get_candidate()`, `list_candidates()`, `update_candidate_status()`, `create_evaluation()`, `get_evaluations_for_candidate()`
- [ ] Test migration up/down with SQLite

### Step 2: Deterministic candidate proposer (Day 1-2)
- [ ] Create `backend/app/services/candidate_proposer.py`:
  - `propose_candidates(transcript_segments, scenes, audio_signals, params) -> List[CandidateWindow]`
  - Signals used:
    - Transcript: sentence boundaries, question/answer pairs, topic shifts, entity density
    - Scenes: scene boundaries (from ING-004), keyframe visual change
    - Audio: silence gaps, energy peaks, speech rate changes
    - Gaming (if profile=gaming): event markers, facecam reaction timestamps
  - Output: list of `{start_ms, end_ms, signal_sources, initial_score}`
  - Respect min/max duration, snap to word boundaries
- [ ] Add config in `backend/app/config.py` for proposer thresholds

### Step 3: Profile-specific evaluator (Day 2-3)
- [ ] Create `backend/app/services/candidate_evaluator.py`:
  - `evaluate_candidate(candidate_window, transcript, scenes, keyframes, profile, provider_hint, routing_mode) -> EvaluationResult`
  - Load profile-specific prompt templates (4 profiles)
  - Use capability registry to select provider/model
  - Structured output: rubric scores + explanation + confidence
  - Bounded retries for malformed JSON output
  - Cost/latency tracking
- [ ] Create profile prompt templates in `backend/app/prompts/`:
  - `podcast_evaluation.txt`, `educational_evaluation.txt`, `gaming_evaluation.txt`, `entertainment_evaluation.txt`
  - Each defines rubric dimensions, few-shot examples, output schema

### Step 4: Ranking & deduplication (Day 3)
- [ ] Create `backend/app/services/candidate_ranker.py`:
  - `rank_and_deduplicate(candidates, evaluations, params) -> List[RankedCandidate]`
  - Normalize scores across providers (z-score or min-max)
  - Remove overlaps > threshold (IoU of time ranges)
  - Enforce diversity: spread across source duration, different topics/speakers
  - Select top-N by final score
  - Output final ranked list with unified scores

### Step 5: Celery job pipeline (Day 3-4)
- [ ] Create `backend/app/services/analysis_job.py`:
  - Celery task `analyze_media_asset(media_asset_id, params_dict)`
  - Stages with progress: load data (10%) → propose (30%) → evaluate (70%) → rank (90%) → persist (100%)
  - Idempotency: params hash + media_asset_id → existing job check
  - On success: create ClipCandidate + ModelEvaluation records
  - On failure: mark job failed, emit error event
  - Checkpointing: save proposer output, evaluator output per stage
- [ ] Register task in `backend/app/workers/__init__.py`

### Step 6: API endpoints (Day 4-5)
- [ ] Create `backend/app/api/v1/endpoints/analysis.py`:
  - All 6 endpoints as specified in Section 5
  - Dependency injection: SourceRepository, CapabilityRegistry, Celery app
  - Idempotency key from header or generated from params hash
  - Input validation via Pydantic schemas
  - Error responses per frozen `ErrorResponse` shape
- [ ] Wire router in `backend/app/api/v1/api.py`

### Step 7: Schemas (Day 5)
- [ ] Create `backend/app/schemas/analysis.py`:
  - `AnalysisRequest`, `AnalysisResponse`
  - `AnalysisStatusResponse`
  - `ClipCandidateResponse`, `CandidateListResponse`
  - `TranscriptEvidence`, `ModelEvaluationResponse`
  - `AnalysisRetryRequest` (if needed)

### Step 8: Tests (Day 5-6)
- [ ] Unit tests: `backend/tests/unit/test_candidate_proposer.py`
  - Test proposal from transcript boundaries
  - Test scene-aware proposals
  - Test min/max duration enforcement
  - Test word-boundary snapping
- [ ] Unit tests: `backend/tests/unit/test_candidate_evaluator.py`
  - Mock provider responses
  - Test 4 profile prompts
  - Test structured output parsing
  - Test retry on malformed output
- [ ] Unit tests: `backend/tests/unit/test_candidate_ranker.py`
  - Test score normalization
  - Test overlap deduplication
  - Test diversity enforcement
  - Test top-N selection
- [ ] Integration tests: `backend/tests/integration/test_analysis_api.py`
  - POST /candidates → 202, returns job_id
  - GET /candidates → status progression
  - GET /candidates/list → paginated, filterable
  - GET /candidates/{id} → detail with scores/evidence
  - Idempotency: same params = same job_id
  - Retry failed job
- [ ] Migration test: `backend/tests/test_proc001_migration.py`

### Step 9: Documentation and verification (Day 6-7)
- [ ] Update `docs/slices/PROC-001.md` with implementation evidence
- [ ] Update `docs/engineering/REQUIREMENTS-TRACEABILITY.csv` with PROC-001 rows
- [ ] Update `docs/engineering/PHASE-STATUS.md`
- [ ] Run full test suite: `python -m pytest backend/tests/ -x -v`
- [ ] Verify all acceptance criteria

---

## 7. Tests

| Test ID | Type | Description | Acceptance Criteria |
|---|---|---|---|
| TC-PROC-001-001 | Unit | Proposer finds candidates at sentence boundaries | ≥1 candidate per 2 min of transcript |
| TC-PROC-001-002 | Unit | Proposer respects min/max duration | All candidates: min ≤ duration ≤ max |
| TC-PROC-001-003 | Unit | Proposer snaps to word boundaries | Start/end align with segment boundaries |
| TC-PROC-001-004 | Unit | Proposer uses scenes when available | Candidates align with scene boundaries |
| TC-PROC-001-005 | Unit | Evaluator returns structured rubric scores | All 6 dimensions present, 0-1 range |
| TC-PROC-001-006 | Unit | Evaluator uses profile-specific prompt | Different prompts for 4 profiles |
| TC-PROC-001-007 | Unit | Evaluator retries malformed output | ≤3 retries, then fails job |
| TC-PROC-001-008 | Unit | Ranker normalizes scores across providers | Scores comparable after normalization |
| TC-PROC-001-009 | Unit | Ranker removes overlaps > threshold | No two candidates IoU > 0.3 |
| TC-PROC-001-010 | Unit | Ranker enforces diversity | Candidates spread across source duration |
| TC-PROC-001-011 | Integration | POST /candidates returns 202 + job_id | Job queued, idempotency key stored |
| TC-PROC-001-012 | Integration | GET /candidates shows stage progress | Status: proposing → evaluating → ranking → succeeded |
| TC-PROC-001-013 | Integration | GET /candidates/list returns ranked candidates | Paginated, sorted by score desc |
| TC-PROC-001-014 | Integration | GET /candidates/{id} includes evidence | Transcript spans, scene refs, scores, explanation |
| TC-PROC-001-015 | Integration | Idempotent analysis returns same job_id | Same params = same job_id, no duplicate candidates |
| TC-PROC-001-016 | Integration | Retry failed analysis works | Clears old candidates, re-runs full pipeline |
| TC-PROC-001-017 | Migration | Alembic up/down works on SQLite | Tables created/dropped cleanly |

---

## 8. Security / Rights Checks

- [ ] Analysis only runs on MediaAssets with `rights_state = 'declared'` and user owns workspace
- [ ] Provider API keys never exposed in logs/responses (server-side only)
- [ ] LLM prompts sanitized — no user data injected without validation
- [ ] Structured output validation prevents prompt injection
- [ ] Cost limits enforced per job (configurable max USD)
- [ ] Idempotency prevents duplicate provider charges
- [ ] Raw LLM responses stored with redacted sensitive fields (optional, for debugging)

---

## 9. Rollback Strategy

| Failure Point | Rollback Action |
|---|---|
| Migration fails | `alembic downgrade -1` — drops `clip_candidates`, `model_evaluations` |
| Proposer crashes | Job failed, no candidates created (transactional) |
| Evaluator provider fails | Retry with fallback provider (capability registry); if all fail, job failed |
| Evaluator malformed output | Bounded retries (3), then job failed with error |
| Ranker produces no candidates | Job succeeds with 0 candidates (valid outcome for short/poor content) |
| Storage fails during persistence | Job failed, partial candidates rolled back (transaction) |
| Celery worker dies mid-job | Job lease expires, another worker restarts from last checkpoint |

---

## 10. Non-Goals

- Rendering clips (REN-001)
- Clip Studio timeline editing (EDIT-001)
- Caption generation (EDIT-001)
- B-roll insertion/generation (future)
- Publishing (PUB-001+)
- Speaker diarization (ING-005)
- Face tracking/clustering (ING-005)
- Real-time/streaming analysis
- Automatic publishing from candidates
- Virality prediction (scores are editorial quality, not engagement prediction)

---

## 11. Acceptance Criteria (Measurable)

| AC ID | Requirement | Verification Method |
|---|---|---|
| AC-PROC-001-001 | POST /candidates triggers async analysis job returning 202 + job_id | Integration test TC-PROC-001-011 |
| AC-PROC-001-002 | GET /candidates returns stage progress (proposing→evaluating→ranking→succeeded) | Integration test TC-PROC-001-012 |
| AC-PROC-001-003 | Deterministic proposer finds candidates from transcript + scenes + audio | Unit tests TC-PROC-001-001 through TC-PROC-001-004 |
| AC-PROC-001-004 | Profile-specific evaluator uses 4 distinct prompts | Unit test TC-PROC-001-006 |
| AC-PROC-001-005 | Evaluator returns 6 rubric dimensions (hook, context, payoff, standalone, visual, emotional) | Unit test TC-PROC-001-005 |
| AC-PROC-001-006 | Provider selection via capability registry with routing modes | Integration test (provider_hint + routing_mode params) |
| AC-PROC-001-007 | Ranker normalizes scores, deduplicates overlaps, enforces diversity | Unit tests TC-PROC-001-008 through TC-PROC-001-010 |
| AC-PROC-001-008 | Candidates persisted with scores, evidence, explanation, status | Integration test TC-PROC-001-013, TC-PROC-001-014 |
| AC-PROC-001-009 | Model evaluations logged per provider/model/prompt version | Integration test (GET /candidates/{id}/evaluations) |
| AC-PROC-001-010 | Idempotent: same params returns same job_id, no duplicate candidates | Integration test TC-PROC-001-015 |
| AC-PROC-001-011 | Failed job retry clears old candidates and re-runs | Integration test TC-PROC-001-016 |
| AC-PROC-001-012 | Alembic migration applies cleanly up and down | Migration test TC-PROC-001-017 |
| AC-PROC-001-013 | Full test suite passes (new + existing) | `pytest backend/tests/ -x -v` → 0 failures |

---

## 12. Files to Create/Modify

### New files
```
backend/app/services/candidate_proposer.py
backend/app/services/candidate_evaluator.py
backend/app/services/candidate_ranker.py
backend/app/services/analysis_job.py
backend/app/api/v1/endpoints/analysis.py
backend/app/schemas/analysis.py
backend/alembic/versions/XXXX_proc001_candidates.py
backend/app/prompts/podcast_evaluation.txt
backend/app/prompts/educational_evaluation.txt
backend/app/prompts/gaming_evaluation.txt
backend/app/prompts/entertainment_evaluation.txt
backend/tests/unit/test_candidate_proposer.py
backend/tests/unit/test_candidate_evaluator.py
backend/tests/unit/test_candidate_ranker.py
backend/tests/integration/test_analysis_api.py
backend/tests/test_proc001_migration.py
```

### Modified files
```
backend/app/db/models.py                          # Add ClipCandidate, ModelEvaluation models
backend/app/db/source_repository.py               # Add candidate/evaluation repository methods
backend/app/config.py                             # Add analysis config (cost limits, proposer thresholds)
backend/app/workers/__init__.py                   # Register analyze_media_asset task
backend/app/api/v1/api.py                         # Include analysis router
docs/slices/PROC-001.md                           # Implementation evidence
docs/engineering/REQUIREMENTS-TRACEABILITY.csv    # Traceability rows
docs/engineering/PHASE-STATUS.md                  # Phase status update
docs/engineering/CHANGELOG-DEV.md                 # Changelog entry
```

---

## 13. Dependencies

| Dependency | Source | Notes |
|---|---|---|
| Existing capability registry | ING-003 | Provider selection + routing |
| Transcription models/segments | ING-003 | Transcript evidence for candidates |
| Scene detection (optional) | ING-004 | Scene boundaries + keyframes (graceful degradation if not ready) |
| OpenAI/Anthropic/Gemini/NVIDIA APIs | Provider configs | For multimodal evaluation |
| Pydantic v2 | PyPI | Already in requirements |
| tiktoken | PyPI | Token counting for cost estimation (optional) |

---

## 14. Content Profile Rubrics (Reference)

### Podcast / Interview
- **Hook** (0-1): Opening question, controversial statement, strong claim
- **Context** (0-1): Guest intro, background, setup for the story
- **Payoff** (0-1): Punchline, revelation, emotional peak, actionable insight
- **Standalone** (0-1): Understandable without prior context
- **Visual** (0-1): Speaker engagement, gestures, reaction shots
- **Emotional** (0-1): Laughter, surprise, empathy, inspiration

### Educational / Technical
- **Hook** (0-1): Problem statement, "why this matters", knowledge gap
- **Context** (0-1): Prerequisites, mental model, analogies
- **Payoff** (0-1): Solution demo, result, "aha!" moment, code working
- **Standalone** (0-1): Complete concept, no missing steps
- **Visual** (0-1): Screen clarity, code readability, diagram quality
- **Emotional** (0-1): Confidence, curiosity satisfaction, empowerment

### Gaming
- **Hook** (0-1): High-stakes moment, clutch play, funny fail, rare event
- **Context** (0-1): Game state, loadout, strategy setup
- **Payoff** (0-1): Win, kill, discovery, reaction payoff
- **Standalone** (0-1): Understandable without full match context
- **Visual** (0-1): Gameplay clarity, facecam sync, UI readability
- **Emotional** (0-1): Excitement, tension, humor, satisfaction

### Entertainment / Funny
- **Hook** (0-1): Setup, premise, curiosity gap
- **Context** (0-1): Character dynamics, running gag callback
- **Payoff** (0-1): Punchline, twist, reaction, callback payoff
- **Standalone** (0-1): Funny without prior episodes
- **Visual** (0-1): Expressiveness, timing, editing beats
- **Emotional** (0-1): Laughter, surprise, relatability, delight

---

**Requesting:** `APPROVE SLICE PROC-001`