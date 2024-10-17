import os
import asyncio
from dotenv import load_dotenv
from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy import engine_from_config
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import create_async_engine

from alembic import context

from app.db.models import Base


# 환경 결정 (기본값 development) 
env = os.getenv('ALEMBIC_ENV', 'development')

# SQL query log 출력 여부 결정 
if env == 'development': 
    echo = True 
else: 
    echo = False 

# 환경에 따른 환경설정 파일 결정 
env_file = {
    'development': '.env.local',    
    'production': '.env.production'
}.get(env, '.env')  # 둘 다 파일이 없을 경우 .env에서 가지고 옴

load_dotenv(env_file)

DB_URL = {
    'development': os.getenv('DEV_DATABASE_URL'),
    'production': os.getenv('PROD_DATABASE_URL')
}.get(env, os.getenv('DATABASE_URL'))

if not DB_URL:
    raise ValueError(f"No database URL configured for the {env} environment.")

config = context.config
config.set_main_option('sqlalchemy.url', DB_URL)

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    url = config.get_main_option("sqlalchemy.url")
    connectable = create_async_engine(
        url,
        echo=echo,
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


if context.is_offline_mode():
    print("Running migrations in offline mode.")
    run_migrations_offline()
else:
    print("Running migrations in online mode.")
    asyncio.run(run_migrations_online())
