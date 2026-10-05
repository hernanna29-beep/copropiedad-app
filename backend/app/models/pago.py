from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import Boolean, Date, DateTime, ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Pago(Base):
    __tablename__ = "pagos"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    unidad_id: Mapped[int] = mapped_column(
        ForeignKey("unidades.id"),
        nullable=False,
        index=True
    )

    concepto: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    periodo: Mapped[str] = mapped_column(
        String(20),
        nullable=False
    )

    valor: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False
    )

    estado: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        default="PENDIENTE"
    )

    fecha_vencimiento: Mapped[date | None] = mapped_column(
        Date,
        nullable=True
    )

    fecha_pago: Mapped[date | None] = mapped_column(
        Date,
        nullable=True
    )

    referencia: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True
    )

    observaciones: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True
    )

    activo: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False
    )

    fecha_creacion: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.utcnow
    )