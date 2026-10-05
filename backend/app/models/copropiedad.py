from datetime import datetime

from sqlalchemy import String, Text, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Copropiedad(Base):
    __tablename__ = "copropiedades"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )

    nombre: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    nit: Mapped[str | None] = mapped_column(
        String(30),
        nullable=True,
        unique=True,
    )

    direccion: Mapped[str | None] = mapped_column(
        String(200),
        nullable=True,
    )

    ciudad: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    telefono: Mapped[str | None] = mapped_column(
        String(30),
        nullable=True,
    )

    email: Mapped[str | None] = mapped_column(
        String(150),
        nullable=True,
    )

    descripcion: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    fecha_creacion: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    activo: Mapped[bool] = mapped_column(
        default=True,
        nullable=False,
    )