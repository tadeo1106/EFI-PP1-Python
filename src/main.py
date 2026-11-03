from contextlib import asynccontextmanager
from pathlib import Path

from alembic.config import Config
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_pagination.api import add_pagination

from alembic import command
from src.routers.funcion import router as funcion_router
from src.routers.genero import router as genero_router
from src.routers.pelicula import router as pelicula_router
from src.routers.sala import router as sala_router

BASE_DIR = Path(__file__).resolve().parent.parent


def run_migrations():
    ini_path = BASE_DIR / "alembic.ini"
    alembic_dir = BASE_DIR / "alembic"

    # Verificación rápida en los logs para confirmar que se subieron los archivos
    if not ini_path.exists():
        raise FileNotFoundError(f"No se encontró alembic.ini en: {ini_path}")

    alembic_cfg = Config(str(ini_path))

    # Forzamos la ruta absoluta de la carpeta de migraciones
    alembic_cfg.set_main_option("script_location", str(alembic_dir))

    command.upgrade(alembic_cfg, "head")


@asynccontextmanager
async def lifespan(app: FastAPI):
    run_migrations()
    yield


app = FastAPI(
    lifespan=lifespan,
    title="Cine API",
    description="API para ministrar peliculas, salas, funciones .",
    version="1.0.0",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://efi-javascript-ten.vercel.app",
        "http://localhost:5173",
        "http://localhost:5174",
        "http://localhost:5178",
    ],
    allow_credentials=True,  # Permite el envío de cookies/tokens en los headers
    allow_methods=["*"],  # Métodos permitidos (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # headers permitidos
)

app.include_router(sala_router)
app.include_router(genero_router)
app.include_router(pelicula_router)
app.include_router(funcion_router)
add_pagination(app)
