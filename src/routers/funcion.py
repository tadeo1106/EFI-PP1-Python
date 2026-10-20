from fastapi import APIRouter, HTTPException, status
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlmodel import paginate
from sqlmodel import select

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

NO_ENCONTRADA = {404: {"description": "Función no encontrada"}}


@router.post(
    "/",
    response_model=FuncionPublic,
    status_code=status.HTTP_201_CREATED,
    responses={404: {"description": "Función o película no encontrada"}},
)
def crear_funcion(new_funcion: FuncionCreate, db: SessionDep):
    pelicula = db.get(Pelicula, new_funcion.pelicula_id)
    if not pelicula:
        raise HTTPException(status_code=404, detail="Película no encontrada")
    funcion = Funcion.model_validate(new_funcion)
    db.add(funcion)
    db.commit()
    db.refresh(funcion)
    return funcion


@router.get("/", response_model=Page[FuncionPublic])
def listar_funciones(db: SessionDep):
    query = select(Funcion).order_by(Funcion.id)
    return paginate(db, query)


@router.get("/{funcion_id}", response_model=FuncionNested, responses=NO_ENCONTRADA)
def obtener_funcion(funcion_id: int, db: SessionDep):
    funcion = db.get(Funcion, funcion_id)
    if not funcion:
        raise HTTPException(status_code=404, detail="Función no encontrada")
    return funcion


@router.put(
    "/{funcion_id}",
    response_model=FuncionPublic,
    responses={404: {"description": "Función o película no encontrada"}},
)
def actualizar_funcion(funcion_id: int, data: FuncionUpdate, db: SessionDep):
    funcion = db.get(Funcion, funcion_id)
    if not funcion:
        raise HTTPException(status_code=404, detail="Función no encontrada")
    if data.pelicula_id is not None and not db.get(Pelicula, data.pelicula_id):
        raise HTTPException(status_code=404, detail="Película no encontrada")
    funcion.sqlmodel_update(data.model_dump(exclude_unset=True))
    db.add(funcion)
    db.commit()
    db.refresh(funcion)
    return funcion


@router.delete(
    "/{funcion_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses=NO_ENCONTRADA,
)
def eliminar_funcion(funcion_id: int, db: SessionDep):
    funcion = db.get(Funcion, funcion_id)
    if not funcion:
        raise HTTPException(status_code=404, detail="Función no encontrada")
    db.delete(funcion)
    db.commit()
