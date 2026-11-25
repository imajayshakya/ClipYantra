# Backend Foundation

FOUND-001 provides typed settings, liveness/readiness endpoints and PostgreSQL `SELECT 1` readiness when configured.

## Run

From the repository root:

```powershell
python -m pip install -e ".[test]"
python -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000
```

## Health

- `GET /health/live` - process liveness, HTTP 200.
- `GET /health/ready` - component readiness.

With no `DATABASE_URL`, readiness is HTTP 503 and the database component is `not_configured`.
Redis, object storage and worker components remain `not_configured` until implemented.

## Tests

```powershell
python -m pytest backend/tests/test_config.py backend/tests/test_database_probe.py backend/tests/test_health.py -q
```

The default suite uses injected database results; it does not claim a live PostgreSQL connection was tested.
