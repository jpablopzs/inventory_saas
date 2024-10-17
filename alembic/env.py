import os
import sys
from sqlalchemy import pool
from alembic import context
from logging.config import fileConfig
from sqlalchemy.ext.asyncio import create_async_engine
from app.inventory.models.inventory import Base


sys.path.insert(0, os.path.realpath(os.path.join(os.path.dirname(__file__), '..', 'app')))

config = context.config

fileConfig(config.config_file_name)

target_metadata = Base.metadata



def run_migrations_offline() -> None:

    url = os.environ.get('POSTGRES_URL')
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        include_schemas=True
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    connectable = create_async_engine(
        os.environ.get('POSTGRES_URL'),
        poolclass=pool.NullPool
    )

    async with connectable.connect() as connection:
        # Ejecutar configuraciones de manera sincronizada
        await connection.run_sync(do_run_migrations)

def do_run_migrations(connection):
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        include_schemas=True
    )

    with context.begin_transaction():
        context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    import asyncio
    asyncio.run(run_migrations_online())
