from datetime import datetime

from fastapi import APIRouter, HTTPException, Query, status
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlmodel import paginate
from sqlalchemy.orm.attributes import init_collection
from sqlalchemy.sql.schema import FetchedValue
from sqlmodel import Session, select

from src.core import exceptions
from src.database import SessionDep
from src.models.funcion import (
    Funcion,
    FuncionCreate,
    FuncionNested,
    FuncionPublic,
    FuncionUpdate,
)
from src.models.pelicula import Pelicula
from src.models.sala import Sala

router = APIRouter(
    prefix="/funciones",
    tags=["Funciones"],
)


def validar_funcion(
    db: Session, data: FuncionCreate | FuncionUpdate, id: int | None = None
):
    if not db.get(Pelicula, data.pelicula_id):
        raise HTTPException(status_code=404, detail=exceptions.PELICULA_NO_ENCONTRADA)

    sala = db.get(Sala, data.sala_id)
    if not sala:
        raise HTTPException(status_code=404, detail=exceptions.SALA_NO_ENCONTRADA)

    if data.entradas_disponibles > sala.capacidad:
        raise HTTPException(
            status_code=400, detail="Las entradas superan la capacidad de la sala"
        )

    consulta = select(Funcion).where(
        Funcion.sala_id == data.sala_id,
        Funcion.fecha_hora == data.fecha_hora,
    )
    if id is not None:
        consulta = consulta.where(Funcion.id != id)

    if db.exec(consulta).first():
        raise HTTPException(status_code=409, detail=exceptions.SALA_OCUPADA)


@router.post(
    "/",
    response_model=FuncionPublic,
    status_code=status.HTTP_201_CREATED,
    responses={**exceptions.not_found, **exceptions.conflict_funcion},
)
def crear_funcion(new_funcion: FuncionCreate, db: SessionDep):

    validar_funcion(db, new_funcion)

    funcion = Funcion.model_validate(new_funcion)
    db.add(funcion)
    db.commit()
    db.refresh(funcion)
    return funcion


@router.get("/proximas", response_model=list[FuncionNested])
def mostrar_proximas_funciones(db: SessionDep, limit: int = Query(default=3, le=10)):
    hoy = datetime.now()
    query = (
        select(Funcion)
        .where(Funcion.fecha_hora >= hoy)
        .order_by(Funcion.fecha_hora.asc())
        .limit(limit)
    )
    return db.exec(query).all()


@router.get("/", response_model=Page[FuncionPublic])
def listar_funciones(db: SessionDep):
    query = select(Funcion).order_by(Funcion.id)
    return paginate(db, query)


@router.get(
    "/{funcion_id}", response_model=FuncionNested, responses=exceptions.not_found
)
def obtener_funcion(funcion_id: int, db: SessionDep):
    funcion = db.get(Funcion, funcion_id)
    if not funcion:
        raise HTTPException(status_code=404, detail=exceptions.FUNCION_NO_ENCONTRADA)
    return funcion


@router.put(
    "/{funcion_id}",
    response_model=FuncionPublic,
    responses={**exceptions.not_found, **exceptions.conflict_funcion},
)
def actualizar_funcion(funcion_id: int, data: FuncionUpdate, db: SessionDep):
    funcion = db.get(Funcion, funcion_id)
    if not funcion:
        raise HTTPException(status_code=404, detail=exceptions.FUNCION_NO_ENCONTRADA)

    validar_funcion(db, data, id=funcion_id)

    funcion.sqlmodel_update(data.model_dump())
    db.add(funcion)
    db.commit()
    db.refresh(funcion)
    return funcion


@router.delete(
    "/{funcion_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses=exceptions.not_found,
)
def eliminar_funcion(funcion_id: int, db: SessionDep):
    funcion = db.get(Funcion, funcion_id)
    if not funcion:
        raise HTTPException(status_code=404, detail=exceptions.FUNCION_NO_ENCONTRADA)
    db.delete(funcion)
    db.commit()
