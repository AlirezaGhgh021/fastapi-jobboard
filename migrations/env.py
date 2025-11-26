from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from sqlalchemy import create_engine  # ← sync engine just for Alembic
from alembic import context
from sqlmodel import SQLModel

# Import our models so Alembic can see the User table
import jobboard_api.models.user

# Import our DATABASE_URL (it's async, we will convert it)
from jobboard_api.database import DATABASE_URL

# this is the Alembic Config object
config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Tell Alembic about our models
target_metadata = SQLModel.metadata

# Convert async URL → sync URL for Alembic (this is the trick!)
SYNC_DATABASE_URL = DATABASE_URL.replace("postgresql+asyncpg://", "postgresql+psycopg2://")

# Give Alembic a proper sync engine
config.set_main_option("sqlalchemy.url", SYNC_DATABASE_URL)

def run_migrations_offline():
    context.configure(
        url=SYNC_DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    # Create a real sync engine just for migrations
    connectable = create_engine(SYNC_DATABASE_URL)

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()