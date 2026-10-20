from fastapi import FastAPI
from fastapi_pagination.api import add_pagination

from src.routers.genero import router as genero_router
from src.routers.sala import router as sala_router

app = FastAPI(
    title="Cine API",
)

app.include_router(sala_router)
app.include_router(genero_router)
add_pagination(app)
