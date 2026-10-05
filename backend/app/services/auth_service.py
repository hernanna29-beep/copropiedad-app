from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.security import crear_access_token, verificar_password
from app.models.usuario import Usuario


def autenticar_usuario(
    db: Session,
    email: str,
    password: str,
) -> str | None:
    usuario = db.execute(
        select(Usuario).where(Usuario.email == email)
    ).scalar_one_or_none()

    if not usuario:
        return None

    if not usuario.activo:
        return None

    if not verificar_password(
        password,
        usuario.password_hash,
    ):
        return None

    token = crear_access_token(
        {
            "sub": str(usuario.id),
            "email": usuario.email,
            "rol": usuario.rol,
        }
    )

    return token