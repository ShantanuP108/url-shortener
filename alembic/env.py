from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
import sys
import os

# Ensure the app package is importable
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.models.base import Base
from app.core.config import settings  # <- Import our DB settings

# Alembic Config
config = context.config

# Override sqlalchemy.url with our dynamic URL from settings
config.set_main_option("sqlalchemy.url", settings.database_url)

# Setup logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Metadata for 'autogenerate'
target_metadata = Base.metadata


def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    url = settings.database_url
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
