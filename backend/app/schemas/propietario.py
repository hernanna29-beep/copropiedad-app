from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class PropietarioBase(BaseModel):
    tipo_documento: str = Field(
        ...,
        min_length=2,
        max_length=20,
        description="Tipo de documento"
    )

    numero_documento: str = Field(
        ...,
        min_length=3,
        max_length=30,
        description="Número de documento"
    )

    nombres: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description="Nombres del propietario"
    )

    apellidos: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description="Apellidos del propietario"
    )

    telefono: str | None = Field(
        default=None,
        max_length=30,
        description="Teléfono de contacto"
    )

    email: str | None = Field(
        default=None,
        max_length=150,
        description="Correo electrónico"
    )

    direccion: str | None = Field(
        default=None,
        max_length=200,
        description="Dirección de residencia"
    )


class PropietarioCreate(PropietarioBase):
    pass


class PropietarioUpdate(BaseModel):
    tipo_documento: str | None = Field(
        default=None,
        min_length=2,
        max_length=20
    )

    numero_documento: str | None = Field(
        default=None,
        min_length=3,
        max_length=30
    )

    nombres: str | None = Field(
        default=None,
        min_length=2,
        max_length=100
    )

    apellidos: str | None = Field(
        default=None,
        min_length=2,
        max_length=100
    )

    telefono: str | None = Field(
        default=None,
        max_length=30
    )

    email: str | None = Field(
        default=None,
        max_length=150
    )

    direccion: str | None = Field(
        default=None,
        max_length=200
    )

    activo: bool | None = None


class PropietarioResponse(PropietarioBase):
    id: int
    fecha_creacion: datetime
    activo: bool

    model_config = ConfigDict(from_attributes=True)