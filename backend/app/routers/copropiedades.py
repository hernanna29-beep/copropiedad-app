from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.copropiedad import (
    CopropiedadCreate,
    CopropiedadResponse,
    CopropiedadUpdate,
)
from app.services.copropiedad_service import (
    actualizar_copropiedad,
    crear_copropiedad,
    desactivar_copropiedad,
    listar_copropiedades,
    obtener_copropiedad,
)


router = APIRouter(
    prefix="/copropiedades",
    tags=["Copropiedades"],
)


@router.post(
    "/",
    response_model=CopropiedadResponse,
    status_code=status.HTTP_201_CREATED,
)
def crear(
    datos: CopropiedadCreate,
    db: Session = Depends(get_db),
):
    try:
        return crear_copropiedad(db, datos)

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(error),
        )


@router.get(
    "/",
    response_model=list[CopropiedadResponse],
)
def listar(
    db: Session = Depends(get_db),
):
    return listar_copropiedades(db)


@router.get(
    "/{copropiedad_id}",
    response_model=CopropiedadResponse,
)
def obtener(
    copropiedad_id: int,
    db: Session = Depends(get_db),
):
    copropiedad = obtener_copropiedad(
        db,
        copropiedad_id,
    )

    if not copropiedad:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Copropiedad no encontrada",
        )

    return copropiedad


@router.put(
    "/{copropiedad_id}",
    response_model=CopropiedadResponse,
)
def actualizar(
    copropiedad_id: int,
    datos: CopropiedadUpdate,
    db: Session = Depends(get_db),
):
    copropiedad = obtener_copropiedad(
        db,
        copropiedad_id,
    )

    if not copropiedad:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Copropiedad no encontrada",
        )

    try:
        return actualizar_copropiedad(
            db,
            copropiedad,
            datos,
        )

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(error),
        )


@router.delete(
    "/{copropiedad_id}",
    response_model=CopropiedadResponse,
)
def desactivar(
    copropiedad_id: int,
    db: Session = Depends(get_db),
):
    copropiedad = obtener_copropiedad(
        db,
        copropiedad_id,
    )

    if not copropiedad:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Copropiedad no encontrada",
        )

    return desactivar_copropiedad(
        db,
        copropiedad,
    )