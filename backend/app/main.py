from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers.copropiedades import router as copropiedades_router
from app.routers.unidades import router as unidades_router
from app.routers.propietarios import router as propietarios_router
from app.routers.propietario_unidad import router as propietario_unidad_router
from app.routers.usuarios import router as usuarios_router
from app.routers.auth import router as auth_router
from app.routers.pagos import router as pagos_router
from app.routers.comprobantes_pago import router as comprobantes_pago_router

app = FastAPI(
    title="COPROPIEDAD APP API",
    description="API para la gestión integral de copropiedades",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(copropiedades_router)
app.include_router(unidades_router)
app.include_router(propietarios_router)
app.include_router(propietario_unidad_router
)
app.include_router(usuarios_router)
app.include_router(auth_router)
app.include_router(pagos_router)
app.include_router(comprobantes_pago_router)


@app.get("/")
def inicio():
    return {
        "mensaje": "COPROPIEDAD APP API funcionando correctamente",
        "version": "1.0.0",
        "estado": "activo",
    }


@app.get("/health")
def health():
    return {
        "status": "ok",
    }
