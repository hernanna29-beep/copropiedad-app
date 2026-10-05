from sqlalchemy import Boolean, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class PropietarioUnidad(Base):
    __tablename__ = "propietario_unidad"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )

    propietario_id: Mapped[int] = mapped_column(
        ForeignKey("propietarios.id"),
        nullable=False,
        index=True,
    )

    unidad_id: Mapped[int] = mapped_column(
        ForeignKey("unidades.id"),
        nullable=False,
        index=True,
    )

    activo: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    __table_args__ = (
        UniqueConstraint(
            "propietario_id",
            "unidad_id",
            name="uq_propietario_unidad",
        ),
    )