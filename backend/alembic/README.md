# ING-001 Alembic Migration

Synthetic SQLite migration test:

```powershell
$env:DATABASE_URL = "sqlite:///C:/tmp/clipyantra-ing001.db"
alembic -c backend/alembic.ini upgrade head
alembic -c backend/alembic.ini downgrade base
Remove-Item Env:DATABASE_URL
```

No migration is applied by application startup.
