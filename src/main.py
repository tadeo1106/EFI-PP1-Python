from fastapi import FastAPI
from fastapi_pagination.api import add_pagination

from src.routers.genero import router

app = FastAPI(
    title="Cine API",
)

app.include_router(router, prefix="/generos", tags=["Géneros"])
add_pagination(app)
