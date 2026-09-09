from pathlib import Path
import sys

from alembic import context
from sqlalchemy import engine_from_config
from sqlalchemy import pool


# Add services/api to Python path so "app" can be imported.
API_DIR = Path(__file__).resolve().parents[2] / "services" / "api"
sys.path.insert(0, str(API_DIR))


from app.core.config import settings
from app.core.database import Base
from app import models

config = context.config

# Use DATABASE_URL from the root .env file.
config.set_main_option("sqlalchemy.url", settings.database_url)

# Alembic uses this to detect model changes.
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations without creating a database connection."""
    url = config.get_main_option("sqlalchemy.url")

    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations using a live database connection."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()