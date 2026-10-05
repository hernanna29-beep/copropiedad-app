from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from app.services.factura_service import generar_factura_pdf
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import obtener_usuario_actual
from app.schemas.pago import (
    PagoCreate,
    PagoResponse,
    PagoUpdate,
)
from app.services.pago_service import (
    actualizar_pago,
    crear_pago,
    desactivar_pago,
    listar_mis_pagos,
    listar_pagos,
    obtener_pago,
    obtener_pago_del_propietario,
)

router = APIRouter(
    prefix="/pagos",
    tags=["Pagos"],
)


@router.post(
    "/",
    response_model=PagoResponse,
    status_code=status.HTTP_201_CREATED,
)
def crear(
    datos: PagoCreate,
    db: Session = Depends(get_db),
    usuario_actual: dict = Depends(obtener_usuario_actual),
):
    if usuario_actual["rol"] != "ADMIN":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para crear pagos",
        )

    try:
        return crear_pago(db, datos)
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(error),
        )


@router.get(
    "/",
    response_model=list[PagoResponse],
)
def listar(
    db: Session = Depends(get_db),
    usuario_actual: dict = Depends(obtener_usuario_actual),
):
    if usuario_actual["rol"] != "ADMIN":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para listar todos los pagos",
        )

    return listar_pagos(db)


@router.get(
    "/mis-pagos",
    response_model=list[PagoResponse],
)
def mis_pagos(
    db: Session = Depends(get_db),
    usuario_actual: dict = Depends(obtener_usuario_actual),
):
    if usuario_actual["rol"] != "RESIDENTE":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Este endpoint está disponible para residentes",
        )

    propietario_id = usuario_actual.get("propietario_id")

    if propietario_id is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El usuario no tiene un propietario asociado",
        )

    return listar_mis_pagos(db, propietario_id)


@router.get(
    "/{pago_id}",
    response_model=PagoResponse,
)
def obtener(
    pago_id: int,
    db: Session = Depends(get_db),
    usuario_actual: dict = Depends(obtener_usuario_actual),
):
    pago = obtener_pago(db, pago_id)

    if not pago:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pago no encontrado",
        )

    if usuario_actual["rol"] != "ADMIN":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para consultar este pago",
        )

    return pago


@router.put(
    "/{pago_id}",
    response_model=PagoResponse,
)
def actualizar(
    pago_id: int,
    datos: PagoUpdate,
    db: Session = Depends(get_db),
    usuario_actual: dict = Depends(obtener_usuario_actual),
):
    if usuario_actual["rol"] != "ADMIN":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para actualizar pagos",
        )

    pago = obtener_pago(db, pago_id)

    if not pago:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pago no encontrado",
        )

    try:
        return actualizar_pago(db, pago, datos)
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(error),
        )


@router.delete(
    "/{pago_id}",
    response_model=PagoResponse,
)
def desactivar(
    pago_id: int,
    db: Session = Depends(get_db),
    usuario_actual: dict = Depends(obtener_usuario_actual),
):
    if usuario_actual["rol"] != "ADMIN":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para desactivar pagos",
        )

    pago = obtener_pago(db, pago_id)

    if not pago:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pago no encontrado",
        )

    return desactivar_pago(db, pago)
@router.get(
    "/{pago_id}/factura",
)
def descargar_factura(
    pago_id: int,
    db: Session = Depends(get_db),
    usuario_actual: dict = Depends(obtener_usuario_actual),
):
    if usuario_actual["rol"] != "RESIDENTE":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="La descarga de facturas está disponible para residentes",
        )

    propietario_id = usuario_actual.get("propietario_id")

    if propietario_id is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El usuario no tiene un propietario asociado",
        )

    pago = obtener_pago_del_propietario(
        db,
        pago_id,
        propietario_id,
    )

    if not pago:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pago no encontrado",
        )

    pdf = generar_factura_pdf(pago)

    return StreamingResponse(
        pdf,
        media_type="application/pdf",
        headers={
            "Content-Disposition": (
                f'attachment; filename="factura_{pago.id}.pdf"'
            )
        },
    )