from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr


class UsuarioCreate(BaseModel):
    propietario_id: int | None = None
    email: EmailStr
    password: str
    nombres: str
    apellidos: str
    rol: str = "RESIDENTE"


class UsuarioUpdate(BaseModel):
    propietario_id: int | None = None
    email: EmailStr | None = None
    nombres: str | None = None
    apellidos: str | None = None
    rol: str | None = None
    activo: bool | None = None


class UsuarioResponse(BaseModel):
    id: int
    propietario_id: int | None
    email: EmailStr
    nombres: str
    apellidos: str
    rol: str
    activo: bool
    fecha_creacion: datetime
    ultimo_acceso: datetime | None

    model_config = ConfigDict(from_attributes=True)