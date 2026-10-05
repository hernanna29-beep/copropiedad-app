from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.pago import Pago
from app.models.unidad import Unidad
from app.models.propietario_unidad import PropietarioUnidad
from app.schemas.pago import PagoCreate, PagoUpdate


def crear_pago(db: Session, datos: PagoCreate) -> Pago:
    unidad = db.get(Unidad, datos.unidad_id)

    if not unidad:
        raise ValueError("La unidad no existe")

    if not unidad.activo:
        raise ValueError("La unidad está inactiva")

    pago = Pago(
        unidad_id=datos.unidad_id,
        concepto=datos.concepto,
        periodo=datos.periodo,
        valor=datos.valor,
        estado=datos.estado,
        fecha_vencimiento=datos.fecha_vencimiento,
        fecha_pago=datos.fecha_pago,
        referencia=datos.referencia,
        observaciones=datos.observaciones,
        activo=True,
    )

    try:
        db.add(pago)
        db.commit()
        db.refresh(pago)
        return pago
    except IntegrityError:
        db.rollback()
        raise ValueError("No fue posible crear el pago")


def listar_pagos(db: Session) -> list[Pago]:
    consulta = (
        select(Pago)
        .where(Pago.activo.is_(True))
        .order_by(Pago.id)
    )

    resultado = db.execute(consulta)

    return list(resultado.scalars().all())


def obtener_pago(db: Session, pago_id: int) -> Pago | None:
    return db.get(Pago, pago_id)


def actualizar_pago(
    db: Session,
    pago: Pago,
    datos: PagoUpdate,
) -> Pago:

    cambios = datos.model_dump(
        exclude_unset=True,
        exclude_none=True,
    )

    for campo, valor in cambios.items():
        setattr(pago, campo, valor)

    try:
        db.commit()
        db.refresh(pago)
        return pago
    except IntegrityError:
        db.rollback()
        raise ValueError("No fue posible actualizar el pago")


def desactivar_pago(db: Session, pago: Pago) -> Pago:
    pago.activo = False

    db.commit()
    db.refresh(pago)

    return pago
def listar_mis_pagos(db: Session, propietario_id: int) -> list[Pago]:
    consulta = (
        select(Pago)
        .join(Unidad, Pago.unidad_id == Unidad.id)
        .join(
            PropietarioUnidad,
            PropietarioUnidad.unidad_id == Unidad.id,
        )
        .where(
            PropietarioUnidad.propietario_id == propietario_id,
            Pago.activo.is_(True),
        )
        .order_by(Pago.id)
    )

    resultado = db.execute(consulta)

    return list(resultado.scalars().all())
def obtener_pago_del_propietario(
    db: Session,
    pago_id: int,
    propietario_id: int,
) -> Pago | None:
    consulta = (
        select(Pago)
        .join(Unidad, Pago.unidad_id == Unidad.id)
        .join(
            PropietarioUnidad,
            PropietarioUnidad.unidad_id == Unidad.id,
        )
        .where(
            Pago.id == pago_id,
            PropietarioUnidad.propietario_id == propietario_id,
            Pago.activo.is_(True),
        )
    )

    resultado = db.execute(consulta)

    return resultado.scalar_one_or_none()