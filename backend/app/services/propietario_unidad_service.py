from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.propietario import Propietario
from app.models.propietario_unidad import PropietarioUnidad
from app.models.unidad import Unidad
from app.schemas.propietario_unidad import (
    PropietarioUnidadCreate,
    PropietarioUnidadUpdate,
)


def crear_relacion(
    db: Session,
    datos: PropietarioUnidadCreate,
) -> PropietarioUnidad:

    propietario = db.get(Propietario, datos.propietario_id)

    if not propietario:
        raise ValueError("El propietario no existe")

    if not propietario.activo:
        raise ValueError("El propietario está inactivo")

    unidad = db.get(Unidad, datos.unidad_id)

    if not unidad:
        raise ValueError("La unidad no existe")

    if not unidad.activo:
        raise ValueError("La unidad está inactiva")

    relacion_existente = db.execute(
        select(PropietarioUnidad).where(
            PropietarioUnidad.propietario_id == datos.propietario_id,
            PropietarioUnidad.unidad_id == datos.unidad_id,
        )
    ).scalar_one_or_none()

    if relacion_existente:
        if not relacion_existente.activo:
            relacion_existente.activo = True
            db.commit()
            db.refresh(relacion_existente)
            return relacion_existente

        raise ValueError(
            "El propietario ya está asociado a esta unidad"
        )

    relacion = PropietarioUnidad(
        propietario_id=datos.propietario_id,
        unidad_id=datos.unidad_id,
        activo=True,
    )

    try:
        db.add(relacion)
        db.commit()
        db.refresh(relacion)
        return relacion

    except IntegrityError:
        db.rollback()
        raise ValueError(
            "No fue posible crear la asociación propietario-unidad"
        )


def listar_relaciones(
    db: Session,
) -> list[PropietarioUnidad]:

    consulta = (
        select(PropietarioUnidad)
        .where(PropietarioUnidad.activo.is_(True))
        .order_by(PropietarioUnidad.id)
    )

    resultado = db.execute(consulta)

    return list(resultado.scalars().all())


def obtener_relacion(
    db: Session,
    relacion_id: int,
) -> PropietarioUnidad | None:

    return db.get(PropietarioUnidad, relacion_id)


def actualizar_relacion(
    db: Session,
    relacion: PropietarioUnidad,
    datos: PropietarioUnidadUpdate,
) -> PropietarioUnidad:

    relacion.activo = datos.activo

    db.commit()
    db.refresh(relacion)

    return relacion


def desactivar_relacion(
    db: Session,
    relacion: PropietarioUnidad,
) -> PropietarioUnidad:

    relacion.activo = False

    db.commit()
    db.refresh(relacion)

    return relacion