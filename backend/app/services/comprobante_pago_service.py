from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.comprobante_pago import ComprobantePago
from app.models.pago import Pago


ESTADOS_PERMITIDOS = {"APROBADO", "RECHAZADO"}


def crear_comprobante(
    db: Session,
    pago_id: int,
    nombre_archivo: str,
    ruta_archivo: str,
    tipo_archivo: str,
    tamano_archivo: int,
) -> ComprobantePago:
    comprobante = ComprobantePago(
        pago_id=pago_id,
        nombre_archivo=nombre_archivo,
        ruta_archivo=ruta_archivo,
        tipo_archivo=tipo_archivo,
        tamano_archivo=tamano_archivo,
        estado="EN_REVISION",
    )

    db.add(comprobante)
    db.commit()
    db.refresh(comprobante)

    return comprobante


def listar_comprobantes_por_pago(
    db: Session,
    pago_id: int,
) -> list[ComprobantePago]:
    consulta = (
        select(ComprobantePago)
        .where(ComprobantePago.pago_id == pago_id)
        .order_by(ComprobantePago.fecha_subida.desc())
    )

    resultado = db.execute(consulta)

    return list(resultado.scalars().all())


def obtener_comprobante(
    db: Session,
    comprobante_id: int,
) -> ComprobantePago | None:
    return db.get(ComprobantePago, comprobante_id)


def listar_comprobantes_en_revision(
    db: Session,
) -> list[ComprobantePago]:
    consulta = (
        select(ComprobantePago)
        .where(ComprobantePago.estado == "EN_REVISION")
        .order_by(ComprobantePago.fecha_subida.asc())
    )

    resultado = db.execute(consulta)

    return list(resultado.scalars().all())


def actualizar_estado_comprobante(
    db: Session,
    comprobante_id: int,
    estado: str,
    observaciones: str | None = None,
) -> ComprobantePago | None:

    if estado not in ESTADOS_PERMITIDOS:
        raise ValueError(
            "Estado no permitido. Use APROBADO o RECHAZADO"
        )

    comprobante = db.get(
        ComprobantePago,
        comprobante_id,
    )

    if comprobante is None:
        return None

    if comprobante.estado != "EN_REVISION":
        raise ValueError(
            "El comprobante ya fue procesado"
        )

    pago = db.get(
        Pago,
        comprobante.pago_id,
    )

    if pago is None:
        raise ValueError(
            "El pago asociado al comprobante no existe"
        )

    try:
        comprobante.estado = estado
        comprobante.observaciones = observaciones

        if estado == "APROBADO":
            pago.estado = "PAGADO"
            pago.fecha_pago = date.today()

        elif estado == "RECHAZADO":
            pago.estado = "PENDIENTE"
            pago.fecha_pago = None

        db.commit()
        db.refresh(comprobante)
        db.refresh(pago)

        return comprobante

    except Exception:
        db.rollback()
        raise