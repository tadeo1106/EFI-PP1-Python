from datetime import datetime
from typing import Optional

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


def determinar_mes(m=0):
    fecha_actual = datetime.now()
    mes = fecha_actual.month + m
    year = fecha_actual.year

    if mes > 12:
        mes -= 12
        year += 1

    inicio_mes = datetime(year, mes, 1)
    if mes == 12:
        fin_mes = datetime(year + 1, 1, 1)
    else:
        fin_mes = datetime(year, mes + 1, 1)

    return inicio_mes, fin_mes


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
    estado: Optional[str] = Query(
        default=None, description="Filtrar por estado: proximamente o en-cartelera"
    ),
):
    query = select(Pelicula)

    if genero_id is not None:
        query = query.where(Pelicula.genero_id == genero_id)

    if estado is not None:
        if estado == "en-cartelera":
            inicio, fin = determinar_mes(1)
        elif estado == "proximamente":
            inicio, fin = determinar_mes(2)

        else:
            raise HTTPException(
                status_code=400,
                detail="estado debe ser 'en-cartelera' o 'proximamente'",
            )

        query = query.where(
            Pelicula.funciones.any(
                (Funcion.fecha_hora >= inicio) & (Funcion.fecha_hora < fin)
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
