from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class UnidadBase(BaseModel):
    codigo: str = Field(
        ...,
        min_length=1,
        max_length=50,
        description="Código o número de la unidad"
    )

    tipo: str = Field(
        default="Apartamento",
        max_length=50,
        description="Tipo de unidad"
    )

    piso: str | None = Field(
        default=None,
        max_length=20,
        description="Piso de la unidad"
    )

    area_m2: Decimal | None = Field(
        default=None,
        ge=0,
        description="Área de la unidad en metros cuadrados"
    )

    coeficiente: Decimal | None = Field(
        default=None,
        ge=0,
        description="Coeficiente de copropiedad"
    )

    habitaciones: int | None = Field(
        default=None,
        ge=0,
        description="Cantidad de habitaciones"
    )

    parqueadero: str | None = Field(
        default=None,
        max_length=50,
        description="Identificación del parqueadero"
    )


class UnidadCreate(UnidadBase):
    copropiedad_id: int = Field(
        ...,
        gt=0,
        description="ID de la copropiedad"
    )


class UnidadUpdate(BaseModel):
    codigo: str | None = Field(
        default=None,
        min_length=1,
        max_length=50
    )

    tipo: str | None = Field(
        default=None,
        max_length=50
    )

    piso: str | None = Field(
        default=None,
        max_length=20
    )

    area_m2: Decimal | None = Field(
        default=None,
        ge=0
    )

    coeficiente: Decimal | None = Field(
        default=None,
        ge=0
    )

    habitaciones: int | None = Field(
        default=None,
        ge=0
    )

    parqueadero: str | None = Field(
        default=None,
        max_length=50
    )

    activo: bool | None = None


class UnidadResponse(UnidadBase):
    id: int
    copropiedad_id: int
    activo: bool

    model_config = ConfigDict(from_attributes=True)