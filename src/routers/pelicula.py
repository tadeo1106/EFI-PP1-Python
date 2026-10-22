from fastapi import APIRouter, HTTPException, status
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlmodel import paginate
from sqlmodel import select

from src.core import exceptions
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


@router.get(
    "/{pelicula_id}", response_model=PeliculaNested, responses=exceptions.not_found
)
def obtener_pelicula(pelicula_id: int, db: SessionDep):
    pelicula = db.get(Pelicula, pelicula_id)
    if not pelicula:
        raise HTTPException(status_code=404, detail=exceptions.PELICULA_NO_ENCONTRADA)
    return pelicula


@router.put(
    "/{pelicula_id}", response_model=PeliculaPublic, responses=exceptions.not_found
)
def actualizar_pelicula(pelicula_id: int, data: PeliculaUpdate, db: SessionDep):
    pelicula = db.get(Pelicula, pelicula_id)
    if not pelicula:
        raise HTTPException(status_code=404, detail=exceptions.PELICULA_NO_ENCONTRADA)
    pelicula.sqlmodel_update(data.model_dump(exclude_unset=True))
    db.add(pelicula)
    db.commit()
    db.refresh(pelicula)
    return pelicula


@router.delete(
    "/{pelicula_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={**exceptions.not_found, **exceptions.conflict},
)
def eliminar_pelicula(pelicula_id: int, db: SessionDep):
    pelicula = db.get(Pelicula, pelicula_id)
    if not pelicula:
        raise HTTPException(status_code=404, detail=exceptions.PELICULA_NO_ENCONTRADA)
    if pelicula.funciones:
        raise HTTPException(status_code=409, detail=exceptions.PELICULA_CON_FUNCIONES)
    db.delete(pelicula)
    db.commit()
