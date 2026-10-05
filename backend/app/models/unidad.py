from decimal import Decimal
from sqlalchemy import String, Boolean, ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Unidad(Base):
    __tablename__ = "unidades"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    copropiedad_id: Mapped[int] = mapped_column(
        ForeignKey("copropiedades.id"),
        nullable=False,
        index=True
    )

    codigo: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    tipo: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="Apartamento"
    )

    piso: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True
    )

    area_m2: Mapped[Decimal | None] = mapped_column(
        Numeric(10, 2),
        nullable=True
    )

    coeficiente: Mapped[Decimal | None] = mapped_column(
        Numeric(10, 6),
        nullable=True
    )

    habitaciones: Mapped[int | None] = mapped_column(
        nullable=True
    )

    parqueadero: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True
    )

    activo: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False
    )