from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.propietario_unidad import (
    PropietarioUnidadCreate,
    PropietarioUnidadResponse,
    PropietarioUnidadUpdate,
)
from app.services.propietario_unidad_service import (
    actualizar_relacion,
    crear_relacion,
    desactivar_relacion,
    listar_relaciones,
    obtener_relacion,
)


router = APIRouter(
    prefix="/propietario-unidad",
    tags=["Propietario - Unidad"],
)


@router.post(
    "/",
    response_model=PropietarioUnidadResponse,
    status_code=status.HTTP_201_CREATED,
)
def crear(
    datos: PropietarioUnidadCreate,
    db: Session = Depends(get_db),
):
    try:
        return crear_relacion(db, datos)

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(error),
        )


@router.get(
    "/",
    response_model=list[PropietarioUnidadResponse],
)
def listar(
    db: Session = Depends(get_db),
):
    return listar_relaciones(db)


@router.get(
    "/{relacion_id}",
    response_model=PropietarioUnidadResponse,
)
def obtener(
    relacion_id: int,
    db: Session = Depends(get_db),
):
    relacion = obtener_relacion(db, relacion_id)

    if not relacion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Relación propietario-unidad no encontrada",
        )

    return relacion


@router.put(
    "/{relacion_id}",
    response_model=PropietarioUnidadResponse,
)
def actualizar(
    relacion_id: int,
    datos: PropietarioUnidadUpdate,
    db: Session = Depends(get_db),
):
    relacion = obtener_relacion(db, relacion_id)

    if not relacion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Relación propietario-unidad no encontrada",
        )

    return actualizar_relacion(db, relacion, datos)


@router.delete(
    "/{relacion_id}",
    response_model=PropietarioUnidadResponse,
)
def desactivar(
    relacion_id: int,
    db: Session = Depends(get_db),
):
    relacion = obtener_relacion(db, relacion_id)

    if not relacion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Relación propietario-unidad no encontrada",
        )

    return desactivar_relacion(db, relacion)