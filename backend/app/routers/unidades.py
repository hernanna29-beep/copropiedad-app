from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.unidad import (
    UnidadCreate,
    UnidadResponse,
    UnidadUpdate,
)
from app.services.unidad_service import (
    actualizar_unidad,
    crear_unidad,
    desactivar_unidad,
    listar_unidades,
    obtener_unidad,
)


router = APIRouter(
    prefix="/unidades",
    tags=["Unidades"],
)


@router.post(
    "/",
    response_model=UnidadResponse,
    status_code=status.HTTP_201_CREATED,
)
def crear(
    datos: UnidadCreate,
    db: Session = Depends(get_db),
):
    return crear_unidad(db, datos)


@router.get(
    "/",
    response_model=list[UnidadResponse],
)
def listar(
    copropiedad_id: int | None = None,
    db: Session = Depends(get_db),
):
    return listar_unidades(
        db,
        copropiedad_id=copropiedad_id,
    )


@router.get(
    "/{unidad_id}",
    response_model=UnidadResponse,
)
def obtener(
    unidad_id: int,
    db: Session = Depends(get_db),
):
    unidad = obtener_unidad(db, unidad_id)

    if not unidad:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Unidad no encontrada",
        )

    return unidad


@router.put(
    "/{unidad_id}",
    response_model=UnidadResponse,
)
def actualizar(
    unidad_id: int,
    datos: UnidadUpdate,
    db: Session = Depends(get_db),
):
    unidad = obtener_unidad(db, unidad_id)

    if not unidad:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Unidad no encontrada",
        )

    return actualizar_unidad(
        db,
        unidad,
        datos,
    )


@router.delete(
    "/{unidad_id}",
    response_model=UnidadResponse,
)
def desactivar(
    unidad_id: int,
    db: Session = Depends(get_db),
):
    unidad = obtener_unidad(db, unidad_id)

    if not unidad:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Unidad no encontrada",
        )

    return desactivar_unidad(
        db,
        unidad,
    )