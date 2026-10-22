from fastapi import APIRouter, HTTPException, status
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlmodel import paginate
from sqlmodel import select

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

router = APIRouter(
    prefix="/funciones",
    tags=["Funciones"],
)


@router.post(
    "/",
    response_model=FuncionPublic,
    status_code=status.HTTP_201_CREATED,
    responses=exceptions.not_found,
)
def crear_funcion(new_funcion: FuncionCreate, db: SessionDep):
    pelicula = db.get(Pelicula, new_funcion.pelicula_id)
    if not pelicula:
        raise HTTPException(status_code=404, detail=exceptions.PELICULA_NO_ENCONTRADA)
    funcion = Funcion.model_validate(new_funcion)
    db.add(funcion)
    db.commit()
    db.refresh(funcion)
    return funcion


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
    responses=exceptions.not_found,
)
def actualizar_funcion(funcion_id: int, data: FuncionUpdate, db: SessionDep):
    funcion = db.get(Funcion, funcion_id)
    if not funcion:
        raise HTTPException(status_code=404, detail=exceptions.FUNCION_NO_ENCONTRADA)
    if data.pelicula_id is not None and not db.get(Pelicula, data.pelicula_id):
        raise HTTPException(status_code=404, detail=exceptions.PELICULA_NO_ENCONTRADA)
    funcion.sqlmodel_update(data.model_dump(exclude_unset=True))
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
