from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class CopropiedadBase(BaseModel):
    nombre: str = Field(
        ...,
        min_length=2,
        max_length=150,
        description="Nombre de la copropiedad",
    )

    nit: str | None = Field(
        default=None,
        max_length=30,
        description="NIT de la copropiedad",
    )

    direccion: str | None = Field(
        default=None,
        max_length=200,
        description="Dirección de la copropiedad",
    )

    ciudad: str | None = Field(
        default=None,
        max_length=100,
        description="Ciudad",
    )

    telefono: str | None = Field(
        default=None,
        max_length=30,
        description="Teléfono de contacto",
    )

    email: str | None = Field(
        default=None,
        max_length=150,
        description="Correo electrónico",
    )

    descripcion: str | None = Field(
        default=None,
        description="Descripción de la copropiedad",
    )


class CopropiedadCreate(CopropiedadBase):
    pass


class CopropiedadUpdate(BaseModel):
    nombre: str | None = Field(
        default=None,
        min_length=2,
        max_length=150,
    )

    nit: str | None = Field(
        default=None,
        max_length=30,
    )

    direccion: str | None = Field(
        default=None,
        max_length=200,
    )

    ciudad: str | None = Field(
        default=None,
        max_length=100,
    )

    telefono: str | None = Field(
        default=None,
        max_length=30,
    )

    email: str | None = Field(
        default=None,
        max_length=150,
    )

    descripcion: str | None = None

    activo: bool | None = None


class CopropiedadResponse(CopropiedadBase):
    id: int
    fecha_creacion: datetime
    activo: bool

    model_config = ConfigDict(
        from_attributes=True
    )