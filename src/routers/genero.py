from fastapi import APIRouter, HTTPException, status
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlmodel import paginate
from sqlalchemy.orm.session import query
from sqlmodel import select

from src.database import SessionDep
from src.models.genero import (
    Genero,
    GeneroCreate,
    GeneroNested,
    GeneroPublic,
    GeneroUpdate,
)

router = APIRouter()
# falta modularizar los mensajes de error proximamente
NO_ENCONTRADO = {404: {"description": "Género no encontrado"}}


@router.post("/", response_model=GeneroPublic, status_code=status.HTTP_201_CREATED)
def crear_genero(new_genero: GeneroCreate, db: SessionDep):
    genero = Genero.model_validate(new_genero)
    db.add(genero)
    db.commit()
    db.refresh(genero)
    return genero


@router.get("/", response_model=Page[GeneroPublic])
def listar_generos(db: SessionDep):
    query = select(Genero).order_by(Genero.id)
    return paginate(db, query)


@router.get("/{genero_id}", response_model=GeneroNested, responses=NO_ENCONTRADO)
def obtener_genero(genero_id: int, db: SessionDep):
    genero = db.get(Genero, genero_id)
    if not genero:
        raise HTTPException(status_code=404, detail="Género no encontrado")
    return genero


@router.put("/{genero_id}", response_model=GeneroPublic, responses=NO_ENCONTRADO)
def actualizar_genero(genero_id: int, data: GeneroUpdate, db: SessionDep):
    genero = db.get(Genero, genero_id)
    if not genero:
        raise HTTPException(status_code=404, detail="Género no encontrado")
    genero.sqlmodel_update(data.model_dump())
    db.add(genero)
    db.commit()
    db.refresh(genero)
    return genero


@router.delete(
    "/{genero_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        **NO_ENCONTRADO,
        409: {"description": "El género tiene películas asociadas"},
    },
)
def eliminar_genero(genero_id: int, db: SessionDep):
    genero = db.get(Genero, genero_id)
    if not genero:
        raise HTTPException(status_code=404, detail="Género no encontrado")
    if genero.peliculas:
        raise HTTPException(
            status_code=409, detail="No se puede borrar un género con películas"
        )
    db.delete(genero)
    db.commit()

    return {"detail": "Género eliminado correctamente"}
