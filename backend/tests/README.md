# Backend Foundation Tests

FOUND-001 uses pytest for typed settings, database probe and health endpoint contracts.

Run from the repository root:

```powershell
python -m pytest backend/tests/test_config.py backend/tests/test_database_probe.py backend/tests/test_health.py -q
```

The test suite uses synthetic settings and injected database probe results. It does not claim a live PostgreSQL connection.
