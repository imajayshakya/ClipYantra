import os
from alembic import command
from alembic.config import Config
from sqlalchemy import create_engine, inspect


def test_ing001_migration_upgrade_and_downgrade(tmp_path, monkeypatch):
    database_path = tmp_path / "ing001.db"
    # Use async URL for alembic (env var) and sync URL for test inspection
    async_database_url = f"sqlite+aiosqlite:///{database_path}"
    sync_database_url = f"sqlite:///{database_path}"
    monkeypatch.setenv("DATABASE_URL", async_database_url)

    # Alembic config is in backend/alembic.ini - set working directory to backend
    # and use absolute paths for alembic script_location
    backend_dir = os.path.join(os.path.dirname(__file__), "..")
    alembic_ini_path = os.path.join(backend_dir, "alembic.ini")
    alembic_script_location = os.path.join(backend_dir, "alembic")
    
    config = Config(alembic_ini_path)
    config.set_main_option("script_location", alembic_script_location)
    command.upgrade(config, "head")

    engine = create_engine(sync_database_url)
    table_names = set(inspect(engine).get_table_names())
    engine.dispose()

    assert "source_videos" in table_names
    assert "source_rights" in table_names
    assert "upload_sessions" in table_names

    command.downgrade(config, "base")

    engine = create_engine(sync_database_url)
    table_names = set(inspect(engine).get_table_names())
    engine.dispose()

    assert "source_videos" not in table_names
    assert "source_rights" not in table_names
    assert "upload_sessions" not in table_names
