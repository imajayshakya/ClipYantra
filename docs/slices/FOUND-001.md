# FOUND-001 - Application Foundation: Health, Config and Database Connectivity

**Status:** ACCEPTED v1 - explicit `ACCEPT SLICE FOUND-001`  
**Version:** v1  
**Date:** 2026-11-23

## Outcome

The backend process can start with typed settings and expose honest liveness/readiness states. If a PostgreSQL database URL is configured, readiness performs a real `SELECT 1` check without exposing credentials or provider details.

## Parent requirements

- FR-051: track task state, progress, worker health, failures and usage.
- NFR-002: PostgreSQL is authoritative workflow state.
- NFR-004: API credentials are never exposed to the browser or logs.
- NFR-006: every pipeline stage emits structured progress and diagnostics.
- NFR-010: tests cover services, APIs, workers, adapters, UI and E2E flows.

## Contract references

- `docs/02-ARCHITECTURE.md`
- `docs/03-DATA-MODEL.md`
- `docs/04-API-CONTRACTS.md`
- `docs/contracts/CONTRACT-FREEZE.md`

## Acceptance criteria

| ID | Given | When | Then |
|---|---|---|---|
| AC-FND-001 | The backend module is installed | It is started with no database URL | Liveness is HTTP 200 and readiness returns a truthful degraded/not-configured database component |
| AC-FND-002 | A valid PostgreSQL URL is configured and the database accepts `SELECT 1` | Readiness is requested | Readiness is HTTP 200 and database component status is `ready` |
| AC-FND-003 | A PostgreSQL URL is configured but the database is unreachable | Readiness is requested | Readiness is HTTP 503 and database status is `unavailable`; no connection URL or password is exposed |
| AC-FND-004 | The environment contains secret settings | Health endpoints are requested | Response contains no secret value, URL, authorization value or provider credential |
| AC-FND-005 | Redis, object storage and worker integrations are not configured | Readiness is requested | Their component status is explicit `not_configured`, never `ready` or `healthy` |
| AC-FND-006 | The environment supplies invalid database configuration | Settings are loaded | Startup fails with a sanitized configuration error that does not repeat the secret URL |
| AC-FND-007 | The backend source is installed | Placeholder dependencies are restored and tests run | Focused tests execute from documented commands and pass; no real PostgreSQL claim is made unless a live DB test runs |

## In scope

- Backend dependency manifest.
- Typed environment settings.
- FastAPI application entrypoint.
- Liveness and readiness HTTP endpoints.
- SQLAlchemy/psycopg PostgreSQL `SELECT 1` probe abstraction.
- Honest `not_configured` states for Redis, object storage and worker.
- Secret redaction in health responses and configuration errors.
- Focused unit/component tests.
- README command documentation.

## Out of scope

- Redis connection implementation.
- Celery worker startup.
- Object-storage adapters.
- Media, provider or publishing calls.
- Entity models or migrations beyond the approved foundation baseline.
- Frontend components or routes.
- Authentication or workspace authorization.
- Live PostgreSQL integration in the default CI environment.

## Dependencies

- None of the existing application slices.
- Placeholder backend scaffold.
- Contract freeze baseline.
- A PostgreSQL runtime is optional for live integration validation.

## Files expected to change

- `pyproject.toml`
- `.gitignore`
- `backend/app/main.py`
- `backend/app/core/config.py`
- `backend/app/api/health.py`
- `backend/app/db/database.py`
- `backend/tests/test_config.py`
- `backend/tests/test_health.py`
- `backend/tests/test_database_probe.py`
- `backend/README.md`
- `docs/17-ACCEPTANCE-CRITERIA.md`
- `docs/engineering/REQUIREMENTS-TRACEABILITY.csv`
- `docs/engineering/PHASE-STATUS.md`
- `docs/engineering/CHANGELOG-DEV.md`

## Test IDs

- `FND-UNIT-001`: settings defaults and timezone.
- `FND-UNIT-002`: secret redaction and invalid URL handling.
- `FND-COMP-001`: liveness success.
- `FND-COMP-002`: readiness with no database URL.
- `FND-COMP-003`: readiness with database ready.
- `FND-COMP-004`: readiness with database unavailable.
- `FND-COMP-005`: component states for Redis/storage/worker.
- `FND-COMP-006`: no secret values in health responses.

## Implementation tasks

1. Write fail-first tests for settings and health contracts.
2. Add the smallest backend dependency manifest.
3. Replace placeholder settings and health modules.
4. Add a database probe interface and PostgreSQL implementation.
5. Add liveness/readiness routes without secret payload fields.
6. Run focused tests and static syntax checks.
7. Update slice evidence and traceability.

## Rollback

Remove or revert the files listed above and restore the placeholder modules. No database schema or external side effect is changed.

## Risks

- A health probe with an incorrect timeout could block readiness.
- A database URL in logs or response payload could leak credentials.
- `not_configured` components could be mistaken for successful readiness.
- A live PostgreSQL runtime may be unavailable in this environment.

## Evidence needed

- Exact test command and exit code.
- Test counts and failures/skips.
- `python -m compileall` result.
- liveness/readiness sample JSON only for synthetic settings.
- PostgreSQL live integration result only if a runtime is available.

## Implementation evidence

- Red test run: 3 collection errors before implementation (`ConfigurationError` and `DatabaseCheckResult` imports missing).
- Green test run: 16 passed in 2.14s.
- HTTP liveness: 200 on `GET /health/live`.
- HTTP readiness: 503 on `GET /health/ready` with no database URL; database/Redis/storage/worker statuses are `not_configured`/degraded.
- Live PostgreSQL `SELECT 1`: not run because no PostgreSQL runtime or Docker CLI is available in the environment.
- Independent verification: final verifier completed; DEF-FOUND-001 resolved.
- DEF-FOUND-001: malformed/non-numeric, out-of-range, whitespace and extremely long PostgreSQL ports are converted to a sanitized `ConfigurationError`.
- DEF-FOUND-001: whitespace in explicit port text is also rejected by strict raw-port validation.
- Final independent verification: complete for synthetic/config/HTTP/component evidence.
- Final independent verification: DEF-FOUND-001 resolved; AC-FND-002 remains blocked on a live PostgreSQL runtime.
- Human acceptance: `ACCEPT SLICE FOUND-001` received.
- Live PostgreSQL evidence waiver: owner explicitly accepted the slice despite AC-FND-002 remaining without a live-runtime test.

## Approval

Implementation is authorized only for this slice under `APPROVE SLICE FOUND-001`.
