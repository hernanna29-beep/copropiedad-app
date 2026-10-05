from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context
from dotenv import load_dotenv
import os

from app.models.copropiedad import Copropiedad
from app.models.unidad import Unidad
from app.models.propietario import Propietario
from app.models.propietario_unidad import PropietarioUnidad
from app.models.usuario import Usuario
from app.models.pago import Pago
from app.models.comprobante_pago import ComprobantePago

from app.core.database import Base


# Cargar variables del archivo .env
load_dotenv()

config = context.config

# Configurar logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Metadata de SQLAlchemy
target_metadata = Base.metadata


def get_database_url():
    database_url = os.getenv("DATABASE_URL")

    if not database_url:
        raise RuntimeError(
            "DATABASE_URL no estÃ¡ configurada en el archivo .env"
        )

    return database_url


def run_migrations_offline() -> None:
    """Ejecutar migraciones en modo offline."""

    url = get_database_url()

    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Ejecutar migraciones en modo online."""

    configuration = config.get_section(config.config_ini_section)

    configuration["sqlalchemy.url"] = get_database_url()

    connectable = engine_from_config(
        configuration,
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
