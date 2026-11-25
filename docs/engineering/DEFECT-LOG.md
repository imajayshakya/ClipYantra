# Defect Log

Resolved implementation defects are recorded below. Open defects require an owner and retest evidence.

| Defect ID | Title | Severity | Priority | Requirement/AC | Reproduction | Expected vs actual | Evidence | Status | Regression test |
|---|---|---|---|---|---|---|---|---|---|
| DEF-FOUND-001 | Malformed/out-of-range/whitespace/length PostgreSQL URL | Medium | P1 | AC-FND-006 | Set non-numeric, whitespace, out-of-range or extremely long port in DATABASE_URL | Expected sanitized ConfigurationError; raw-port/parser/range/length path fixed | Independent review and red/green tests `test_malformed_postgresql_url_is_sanitized`, `test_out_of_range_postgresql_port_is_sanitized`, `test_whitespace_postgresql_port_is_sanitized`, `test_extremely_long_postgresql_port_is_sanitized` | RESOLVED | All URL-validation regression tests; independent verification rerun |
