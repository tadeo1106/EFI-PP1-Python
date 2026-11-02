from datetime import datetime, timedelta
from typing import Literal, Optional

from fastapi import APIRouter, HTTPException, status
from fastapi.param_functions import Query
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlmodel import paginate
from sqlmodel import select

from src.core import exceptions
from src.database import SessionDep
from src.models.funcion import Funcion
from src.models.genero import Genero
from src.models.pelicula import (
    Pelicula,
    PeliculaCreate,
    PeliculaNested,
    PeliculaPublic,
    PeliculaUpdate,
)
from src.models.resumenes import PeliculaResumen

router = APIRouter(
    prefix="/peliculas",
    tags=["Películas"],
)


def inicio_fin_semana():

    hoy = datetime.now()
    inicio_semana = hoy - timedelta(days=hoy.weekday())
    print("Inicio de semana (lunes)", hoy)
    inicio_semana = inicio_semana.replace(hour=0, minute=0, second=0, microsecond=0)

    fin_semana = inicio_semana + timedelta(days=6, hours=23, minutes=59, seconds=59)

    return inicio_semana, fin_semana


@router.post("/", response_model=PeliculaPublic, responses=exceptions.not_found)
def crear_pelicula(new_pelicula: PeliculaCreate, db: SessionDep):
    genero = db.get(Genero, new_pelicula.genero_id)
    if not genero:
        raise HTTPException(status_code=404, detail=exceptions.GENERO_NO_ENCONTRADO)
    pelicula = Pelicula.model_validate(new_pelicula)
    db.add(pelicula)
    db.commit()
    db.refresh(pelicula)
    return pelicula


@router.get("/", response_model=Page[PeliculaResumen])
def listar_peliculas(
    db: SessionDep,
    genero_id: Optional[int] = Query(
        default=None, description="Filtrar por ID de género"
    ),
    estado: Literal["proximamente", "en-cartelera"] | None = Query(
        default=None, description="Filtrar por estado"
    ),
    estado_semana: Optional[bool] = Query(
        default=None,
        description="Filtrar por las peliculas que tienen funciones de esta semana: True o False",
    ),
):
    query = select(Pelicula)

    if genero_id is not None:
        query = query.where(Pelicula.genero_id == genero_id)

    if estado:
        if estado == "en-cartelera":
            query = query.where(Pelicula.funciones.any())
        elif estado == "proximamente":
            query = query.where(~Pelicula.funciones.any())

        else:
            raise HTTPException(
                status_code=400,
                detail="estado debe ser 'en-cartelera' o 'proximamente'",
            )
    if estado_semana:
        hoy = datetime.now()
        inicio_semana, fin_semana = inicio_fin_semana()
        query = query.where(
            Pelicula.funciones.any(
                (Funcion.fecha_hora >= hoy) & (Funcion.fecha_hora <= fin_semana)
            )
        )
    query = query.order_by(Pelicula.nombre)

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
    genero = db.get(Genero, data.genero_id)
    if not genero:
        raise HTTPException(status_code=404, detail=exceptions.GENERO_NO_ENCONTRADO)
    pelicula.sqlmodel_update(data.model_dump(exclude_unset=True))
    db.add(pelicula)
    db.commit()
    db.refresh(pelicula)
    return pelicula


@router.delete(
    "/{pelicula_id}",
    responses={**exceptions.not_found, **exceptions.conflict},
    status_code=status.HTTP_204_NO_CONTENT,
)
def eliminar_pelicula(pelicula_id: int, db: SessionDep):
    pelicula = db.get(Pelicula, pelicula_id)
    if not pelicula:
        raise HTTPException(status_code=404, detail=exceptions.PELICULA_NO_ENCONTRADA)
    if pelicula.funciones:
        raise HTTPException(status_code=409, detail=exceptions.PELICULA_CON_FUNCIONES)
    db.delete(pelicula)
    db.commit()
