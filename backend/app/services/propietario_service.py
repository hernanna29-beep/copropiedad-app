from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.propietario import Propietario
from app.schemas.propietario import PropietarioCreate, PropietarioUpdate


def crear_propietario(
    db: Session,
    datos: PropietarioCreate,
) -> Propietario:
    propietario_existente = db.execute(
        select(Propietario).where(
            Propietario.numero_documento == datos.numero_documento
        )
    ).scalar_one_or_none()

    if propietario_existente:
        raise ValueError(
            "Ya existe un propietario con ese número de documento"
        )

    propietario = Propietario(**datos.model_dump())

    try:
        db.add(propietario)
        db.commit()
        db.refresh(propietario)
        return propietario

    except IntegrityError:
        db.rollback()
        raise ValueError(
            "Ya existe un propietario con ese número de documento"
        )


def listar_propietarios(db: Session) -> list[Propietario]:
    consulta = (
        select(Propietario)
        .where(Propietario.activo.is_(True))
        .order_by(Propietario.id)
    )

    resultado = db.execute(consulta)

    return list(resultado.scalars().all())


def obtener_propietario(
    db: Session,
    propietario_id: int,
) -> Propietario | None:
    return db.get(Propietario, propietario_id)


def actualizar_propietario(
    db: Session,
    propietario: Propietario,
    datos: PropietarioUpdate,
) -> Propietario:
    cambios = datos.model_dump(exclude_unset=True)

    if "numero_documento" in cambios:
        propietario_existente = db.execute(
            select(Propietario).where(
                Propietario.numero_documento == cambios["numero_documento"],
                Propietario.id != propietario.id,
            )
        ).scalar_one_or_none()

        if propietario_existente:
            raise ValueError(
                "Ya existe otro propietario con ese número de documento"
            )

    for campo, valor in cambios.items():
        setattr(propietario, campo, valor)

    try:
        db.commit()
        db.refresh(propietario)
        return propietario

    except IntegrityError:
        db.rollback()
        raise ValueError(
            "Ya existe otro propietario con ese número de documento"
        )


def desactivar_propietario(
    db: Session,
    propietario: Propietario,
) -> Propietario:
    propietario.activo = False

    db.commit()
    db.refresh(propietario)

    return propietario