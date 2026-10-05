from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.unidad import Unidad
from app.schemas.unidad import UnidadCreate, UnidadUpdate


def crear_unidad(db: Session, datos: UnidadCreate) -> Unidad:
    unidad = Unidad(**datos.model_dump())

    db.add(unidad)
    db.commit()
    db.refresh(unidad)

    return unidad


def listar_unidades(
    db: Session,
    copropiedad_id: int | None = None
) -> list[Unidad]:

    consulta = select(Unidad).where(Unidad.activo.is_(True))

    if copropiedad_id is not None:
        consulta = consulta.where(
            Unidad.copropiedad_id == copropiedad_id
        )

    consulta = consulta.order_by(Unidad.id)

    resultado = db.execute(consulta)

    return list(resultado.scalars().all())


def obtener_unidad(
    db: Session,
    unidad_id: int
) -> Unidad | None:

    return db.get(Unidad, unidad_id)


def actualizar_unidad(
    db: Session,
    unidad: Unidad,
    datos: UnidadUpdate
) -> Unidad:

    cambios = datos.model_dump(exclude_unset=True)

    for campo, valor in cambios.items():
        setattr(unidad, campo, valor)

    db.commit()
    db.refresh(unidad)

    return unidad


def desactivar_unidad(
    db: Session,
    unidad: Unidad
) -> Unidad:

    unidad.activo = False

    db.commit()
    db.refresh(unidad)

    return unidad