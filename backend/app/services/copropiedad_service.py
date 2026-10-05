from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.copropiedad import Copropiedad
from app.schemas.copropiedad import CopropiedadCreate, CopropiedadUpdate


def crear_copropiedad(
    db: Session,
    datos: CopropiedadCreate
) -> Copropiedad:

    if datos.nit:
        copropiedad_existente = db.execute(
            select(Copropiedad).where(
                Copropiedad.nit == datos.nit
            )
        ).scalar_one_or_none()

        if copropiedad_existente:
            if not copropiedad_existente.activo:
                raise ValueError(
                    "Ya existe una copropiedad inactiva con ese NIT. "
                    "Puede reactivarla mediante actualización."
                )

            raise ValueError(
                "Ya existe una copropiedad con ese NIT"
            )

    copropiedad = Copropiedad(**datos.model_dump())

    try:
        db.add(copropiedad)
        db.commit()
        db.refresh(copropiedad)

        return copropiedad

    except IntegrityError:
        db.rollback()

        raise ValueError(
            "Ya existe una copropiedad con ese NIT"
        )


def listar_copropiedades(
    db: Session
) -> list[Copropiedad]:

    consulta = (
        select(Copropiedad)
        .where(Copropiedad.activo.is_(True))
        .order_by(Copropiedad.id)
    )

    resultado = db.execute(consulta)

    return list(resultado.scalars().all())


def obtener_copropiedad(
    db: Session,
    copropiedad_id: int
) -> Copropiedad | None:

    return db.get(Copropiedad, copropiedad_id)


def actualizar_copropiedad(
    db: Session,
    copropiedad: Copropiedad,
    datos: CopropiedadUpdate
) -> Copropiedad:

    cambios = datos.model_dump(exclude_unset=True)

    if "nit" in cambios and cambios["nit"]:
        copropiedad_existente = db.execute(
            select(Copropiedad).where(
                Copropiedad.nit == cambios["nit"],
                Copropiedad.id != copropiedad.id
            )
        ).scalar_one_or_none()

        if copropiedad_existente:
            raise ValueError(
                "Ya existe otra copropiedad con ese NIT"
            )

    for campo, valor in cambios.items():
        setattr(copropiedad, campo, valor)

    try:
        db.commit()
        db.refresh(copropiedad)

        return copropiedad

    except IntegrityError:
        db.rollback()

        raise ValueError(
            "Ya existe otra copropiedad con ese NIT"
        )


def desactivar_copropiedad(
    db: Session,
    copropiedad: Copropiedad
) -> Copropiedad:

    copropiedad.activo = False

    db.commit()
    db.refresh(copropiedad)

    return copropiedad