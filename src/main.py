from fastapi import FastAPI
from fastapi_pagination.api import add_pagination

from src.routers.funcion import router as funcion_router
from src.routers.genero import router as genero_router
from src.routers.pelicula import router as pelicula_router
from src.routers.sala import router as sala_router

app = FastAPI(
    title="Cine API",
)

app.include_router(sala_router)
app.include_router(genero_router)
app.include_router(pelicula_router)
app.include_router(funcion_router)
add_pagination(app)

