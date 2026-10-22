from fastapi import APIRouter, HTTPException, status
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlmodel import paginate
from sqlmodel import select

from src.core import exceptions
from src.database import SessionDep
from src.models.genero import (
    Genero,
    GeneroCreate,
    GeneroNested,
    GeneroPublic,
    GeneroUpdate,
)

router = APIRouter(
    prefix="/generos",
    tags=["Géneros"],
)


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


@router.get("/{genero_id}", response_model=GeneroNested, responses=exceptions.not_found)
def obtener_genero(genero_id: int, db: SessionDep):
    genero = db.get(Genero, genero_id)
    if not genero:
        raise HTTPException(status_code=404, detail=exceptions.GENERO_NO_ENCONTRADO)
    return genero


@router.put("/{genero_id}", response_model=GeneroPublic, responses=exceptions.not_found)
def actualizar_genero(genero_id: int, data: GeneroUpdate, db: SessionDep):
    genero = db.get(Genero, genero_id)
    if not genero:
        raise HTTPException(status_code=404, detail=exceptions.GENERO_NO_ENCONTRADO)
    genero.sqlmodel_update(data.model_dump())
    db.add(genero)
    db.commit()
    db.refresh(genero)
    return genero


@router.delete(
    "/{genero_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={**exceptions.conflict, **exceptions.not_found},
)
def eliminar_genero(genero_id: int, db: SessionDep):
    genero = db.get(Genero, genero_id)
    if not genero:
        raise HTTPException(status_code=404, detail=exceptions.GENERO_NO_ENCONTRADO)
    if genero.peliculas:
        raise HTTPException(status_code=409, detail=exceptions.GENERO_CON_PELICULAS)
    db.delete(genero)
    db.commit()

    return {"detail": "Género eliminado correctamente"}
