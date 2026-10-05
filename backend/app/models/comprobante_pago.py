from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class ComprobantePago(Base):
    __tablename__ = "comprobantes_pago"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )

    pago_id: Mapped[int] = mapped_column(
        ForeignKey("pagos.id"),
        nullable=False,
        index=True,
    )

    nombre_archivo: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    ruta_archivo: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )

    tipo_archivo: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    tamano_archivo: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    estado: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        default="EN_REVISION",
    )

    observaciones: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    fecha_subida: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
    )
