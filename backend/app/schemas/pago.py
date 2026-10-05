from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class PagoBase(BaseModel):
    unidad_id: int
    concepto: str
    periodo: str
    valor: Decimal
    estado: str = "PENDIENTE"
    fecha_vencimiento: date | None = None
    fecha_pago: date | None = None
    referencia: str | None = None
    observaciones: str | None = None


class PagoCreate(PagoBase):
    pass


class PagoUpdate(BaseModel):
    concepto: str | None = None
    periodo: str | None = None
    valor: Decimal | None = None
    estado: str | None = None
    fecha_vencimiento: date | None = None
    fecha_pago: date | None = None
    referencia: str | None = None
    observaciones: str | None = None


class PagoResponse(PagoBase):
    id: int
    activo: bool
    fecha_creacion: datetime

    model_config = ConfigDict(from_attributes=True)