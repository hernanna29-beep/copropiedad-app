from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict


class ComprobantePagoResponse(BaseModel):
    id: int
    pago_id: int
    nombre_archivo: str
    tipo_archivo: str
    tamano_archivo: int
    estado: str
    observaciones: str | None = None
    fecha_subida: datetime

    model_config = ConfigDict(from_attributes=True)


class ComprobantePagoActualizar(BaseModel):
    estado: Literal["APROBADO", "RECHAZADO"]
    observaciones: str | None = None