from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import obtener_usuario_actual
from app.schemas.usuario import (
    UsuarioCreate,
    UsuarioResponse,
    UsuarioUpdate,
)
from app.services.usuario_service import (
    actualizar_usuario,
    crear_usuario,
    desactivar_usuario,
    listar_usuarios,
    obtener_usuario,
)


router = APIRouter(
    prefix="/usuarios",
    tags=["Usuarios"],
)

@router.post(
    "/",
    response_model=UsuarioResponse,
    status_code=status.HTTP_201_CREATED,
)
def crear(
    datos: UsuarioCreate,
    db: Session = Depends(get_db),
    usuario_actual: dict = Depends(obtener_usuario_actual),
):
    if usuario_actual["rol"] != "ADMIN":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para crear usuarios",
        )

    try:
        return crear_usuario(db, datos)
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(error),
        )

@router.get(
    "/",
    response_model=list[UsuarioResponse],
)
def listar(
    db: Session = Depends(get_db),
    usuario_actual: dict = Depends(obtener_usuario_actual),
):
    if usuario_actual["rol"] != "ADMIN":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para listar los usuarios",
        )

    return listar_usuarios(db)

@router.get(
    "/{usuario_id}",
    response_model=UsuarioResponse,
)
def obtener(
    usuario_id: int,
    db: Session = Depends(get_db),
    usuario_actual: dict = Depends(obtener_usuario_actual),
):
    if usuario_actual["rol"] == "RESIDENTE" and usuario_id != usuario_actual["id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para consultar este usuario",
        )

    usuario = obtener_usuario(db, usuario_id)

    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado",
        )

    return usuario


@router.put(
    "/{usuario_id}",
    response_model=UsuarioResponse,
)
def actualizar(
    usuario_id: int,
    datos: UsuarioUpdate,
    db: Session = Depends(get_db),
    usuario_actual: dict = Depends(obtener_usuario_actual),
):
    if usuario_actual["rol"] != "ADMIN":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para actualizar usuarios",
        )

    usuario = obtener_usuario(db, usuario_id)

    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado",
        )

    try:
        return actualizar_usuario(
            db,
            usuario,
            datos,
        )

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(error),
        )


@router.delete(
    "/{usuario_id}",
    response_model=UsuarioResponse,
)
def desactivar(
    usuario_id: int,
    db: Session = Depends(get_db),
    usuario_actual: dict = Depends(obtener_usuario_actual),
):
    if usuario_actual["rol"] != "ADMIN":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para desactivar usuarios",
        )

    usuario = obtener_usuario(db, usuario_id)

    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado",
        )

    return desactivar_usuario(db, usuario)