from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_pagination.api import add_pagination

from src.routers.funcion import router as funcion_router
from src.routers.genero import router as genero_router
from src.routers.pelicula import router as pelicula_router
from src.routers.sala import router as sala_router

app = FastAPI(
    title="Cine API",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,  # Permite el envío de cookies/tokens en los headers
    allow_methods=["*"],  # Métodos permitidos (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # headers permitidos
)

app.include_router(sala_router)
app.include_router(genero_router)
app.include_router(pelicula_router)
app.include_router(funcion_router)
add_pagination(app)
