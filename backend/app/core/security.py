from datetime import datetime, timedelta, timezone

import jwt
from pwdlib import PasswordHash


SECRET_KEY = "CAMBIAR_ESTA_CLAVE_EN_PRODUCCION"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


password_hash = PasswordHash.recommended()


def verificar_password(
    password_plano: str,
    password_hash_guardado: str,
) -> bool:
    return password_hash.verify(
        password_plano,
        password_hash_guardado,
    )


def crear_access_token(
    data: dict,
    expires_delta: timedelta | None = None,
) -> str:
    datos = data.copy()

    if expires_delta:
        expiracion = datetime.now(timezone.utc) + expires_delta
    else:
        expiracion = datetime.now(timezone.utc) + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )

    datos.update({"exp": expiracion})

    return jwt.encode(
        datos,
        SECRET_KEY,
        algorithm=ALGORITHM,
    )