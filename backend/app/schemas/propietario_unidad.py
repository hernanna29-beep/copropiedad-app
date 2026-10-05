from datetime import datetime

from pydantic import BaseModel, ConfigDict


class PropietarioUnidadCreate(BaseModel):
    propietario_id: int
    unidad_id: int


class PropietarioUnidadUpdate(BaseModel):
    activo: bool


class PropietarioUnidadResponse(BaseModel):
    id: int
    propietario_id: int
    unidad_id: int
    activo: bool

    model_config = ConfigDict(from_attributes=True)