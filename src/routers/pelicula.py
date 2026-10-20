from fastapi import APIRouter, HTTPException, status
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlmodel import paginate
from sqlmodel import select

from src.database import SessionDep
from src.models.pelicula import (
    Pelicula,
    PeliculaCreate,
    PeliculaNested,
    PeliculaPublic,
    PeliculaUpdate,
)

router = APIRouter(
    prefix="/peliculas",
    tags=["Películas"],
)

NO_ENCONTRADA = {404: {"description": "Película no encontrada"}}


@router.post("/", response_model=PeliculaPublic, status_code=status.HTTP_201_CREATED)
def crear_pelicula(new_pelicula: PeliculaCreate, db: SessionDep):
    pelicula = Pelicula.model_validate(new_pelicula)
    db.add(pelicula)
    db.commit()
    db.refresh(pelicula)
    return pelicula


@router.get("/", response_model=Page[PeliculaPublic])
def listar_peliculas(db: SessionDep):
    query = select(Pelicula).order_by(Pelicula.id)
    return paginate(db, query)


@router.get("/{pelicula_id}", response_model=PeliculaNested, responses=NO_ENCONTRADA)
def obtener_pelicula(pelicula_id: int, db: SessionDep):
    pelicula = db.get(Pelicula, pelicula_id)
    if not pelicula:
        raise HTTPException(status_code=404, detail="Película no encontrada")
    return pelicula


@router.put("/{pelicula_id}", response_model=PeliculaPublic, responses=NO_ENCONTRADA)
def actualizar_pelicula(pelicula_id: int, data: PeliculaUpdate, db: SessionDep):
    pelicula = db.get(Pelicula, pelicula_id)
    if not pelicula:
        raise HTTPException(status_code=404, detail="Película no encontrada")
    pelicula.sqlmodel_update(data.model_dump(exclude_unset=True))
    db.add(pelicula)
    db.commit()
    db.refresh(pelicula)
    return pelicula


@router.delete(
    "/{pelicula_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        **NO_ENCONTRADA,
        409: {"description": "La película tiene funciones asociadas"},
    },
)
def eliminar_pelicula(pelicula_id: int, db: SessionDep):
    pelicula = db.get(Pelicula, pelicula_id)
    if not pelicula:
        raise HTTPException(status_code=404, detail="Película no encontrada")
    if pelicula.funciones:
        raise HTTPException(
            status_code=409, detail="No se puede borrar una película con funciones"
        )
    db.delete(pelicula)
    db.commit()
