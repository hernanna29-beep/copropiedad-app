from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.propietario import (
    PropietarioCreate,
    PropietarioResponse,
    PropietarioUpdate,
)
from app.services.propietario_service import (
    actualizar_propietario,
    crear_propietario,
    desactivar_propietario,
    listar_propietarios,
    obtener_propietario,
)


router = APIRouter(
    prefix="/propietarios",
    tags=["Propietarios"],
)


@router.post(
    "/",
    response_model=PropietarioResponse,
    status_code=status.HTTP_201_CREATED,
)
def crear(
    datos: PropietarioCreate,
    db: Session = Depends(get_db),
):
    try:
        return crear_propietario(db, datos)

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(error),
        )


@router.get(
    "/",
    response_model=list[PropietarioResponse],
)
def listar(
    db: Session = Depends(get_db),
):
    return listar_propietarios(db)


@router.get(
    "/{propietario_id}",
    response_model=PropietarioResponse,
)
def obtener(
    propietario_id: int,
    db: Session = Depends(get_db),
):
    propietario = obtener_propietario(
        db,
        propietario_id,
    )

    if not propietario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Propietario no encontrado",
        )

    return propietario


@router.put(
    "/{propietario_id}",
    response_model=PropietarioResponse,
)
def actualizar(
    propietario_id: int,
    datos: PropietarioUpdate,
    db: Session = Depends(get_db),
):
    propietario = obtener_propietario(db, propietario_id)

    if not propietario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Propietario no encontrado",
        )

    try:
        return actualizar_propietario(db, propietario, datos)

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(error),
        )


@router.delete(
    "/{propietario_id}",
    response_model=PropietarioResponse,
)
def desactivar(
    propietario_id: int,
    db: Session = Depends(get_db),
):
    propietario = obtener_propietario(
        db,
        propietario_id,
    )

    if not propietario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Propietario no encontrado",
        )

    return desactivar_propietario(
        db,
        propietario,
    )