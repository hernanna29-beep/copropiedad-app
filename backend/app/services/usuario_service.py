from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from pwdlib import PasswordHash

from app.models.propietario import Propietario
from app.models.usuario import Usuario
from app.schemas.usuario import UsuarioCreate, UsuarioUpdate


password_hash = PasswordHash.recommended()


def crear_usuario(db: Session, datos: UsuarioCreate) -> Usuario:
    # Verificar que el propietario exista, si se proporciona
    if datos.propietario_id is not None:
        propietario = db.get(Propietario, datos.propietario_id)

        if not propietario:
            raise ValueError("El propietario no existe")

        if not propietario.activo:
            raise ValueError("El propietario está inactivo")

    # Verificar email existente
    usuario_existente = db.execute(
        select(Usuario).where(Usuario.email == str(datos.email))
    ).scalar_one_or_none()

    if usuario_existente:
        raise ValueError("Ya existe un usuario con ese correo electrónico")

    usuario = Usuario(
        propietario_id=datos.propietario_id,
        email=str(datos.email),
        password_hash=password_hash.hash(datos.password),
        nombres=datos.nombres,
        apellidos=datos.apellidos,
        rol=datos.rol,
        activo=True,
    )

    try:
        db.add(usuario)
        db.commit()
        db.refresh(usuario)

        return usuario

    except IntegrityError:
        db.rollback()
        raise ValueError("No fue posible crear el usuario")


def listar_usuarios(db: Session) -> list[Usuario]:
    consulta = (
        select(Usuario)
        .where(Usuario.activo.is_(True))
        .order_by(Usuario.id)
    )

    resultado = db.execute(consulta)

    return list(resultado.scalars().all())


def obtener_usuario(
    db: Session,
    usuario_id: int,
) -> Usuario | None:
    return db.get(Usuario, usuario_id)


def actualizar_usuario(
    db: Session,
    usuario: Usuario,
    datos: UsuarioUpdate,
) -> Usuario:

    cambios = datos.model_dump(
        exclude_unset=True,
        exclude_none=True,
    )

    # Validar propietario si se está modificando
    if "propietario_id" in cambios:
        propietario_id = cambios["propietario_id"]

        if propietario_id is not None:
            propietario = db.get(
                Propietario,
                propietario_id,
            )

            if not propietario:
                raise ValueError("El propietario no existe")

            if not propietario.activo:
                raise ValueError("El propietario está inactivo")

    # Validar email si se está modificando
    if "email" in cambios:
        email_existente = db.execute(
            select(Usuario).where(
                Usuario.email == str(cambios["email"]),
                Usuario.id != usuario.id,
            )
        ).scalar_one_or_none()

        if email_existente:
            raise ValueError(
                "Ya existe otro usuario con ese correo electrónico"
            )

        cambios["email"] = str(cambios["email"])

    for campo, valor in cambios.items():
        setattr(usuario, campo, valor)

    try:
        db.commit()
        db.refresh(usuario)

        return usuario

    except IntegrityError:
        db.rollback()
        raise ValueError(
            "No fue posible actualizar el usuario"
        )


def desactivar_usuario(
    db: Session,
    usuario: Usuario,
) -> Usuario:

    usuario.activo = False

    db.commit()
    db.refresh(usuario)

    return usuario