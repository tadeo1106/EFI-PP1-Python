from fastapi import HTTPException
from fastapi.routing import APIRouter
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlmodel import paginate
from sqlmodel import select

from src.core import exceptions
from src.database import SessionDep
from src.models.sala import Sala, SalaCreate, SalaPublic, SalaUpdate

router = APIRouter(
    prefix="/sala",
    tags=["Sala"],
)


@router.get("/", response_model=Page[SalaPublic])
def mostrar_salas(db: SessionDep):
    query = select(Sala).order_by(Sala.id)
    return paginate(db, query)


@router.get("/{sala_id}", response_model=SalaPublic, responses=exceptions.not_found)
def mostrar_sala(sala_id: int, db: SessionDep):
    sala = db.get(Sala, sala_id)
    if not sala:
        raise HTTPException(status_code=404, detail=exceptions.SALA_NO_ENCONTRADA)
    return sala


@router.post("/", response_model=SalaPublic, status_code=201)
def crear_sala(new_sala: SalaCreate, db: SessionDep):
    sala = Sala.model_validate(new_sala)
    db.add(sala)
    db.commit()
    db.refresh(sala)
    return sala


@router.put("/{sala_id}", response_model=SalaPublic, responses=exceptions.not_found)
def actualizar_sala(sala_id: int, data: SalaUpdate, db: SessionDep):
    sala = db.get(Sala, sala_id)
    if not sala:
        raise HTTPException(status_code=404, detail=exceptions.SALA_NO_ENCONTRADA)
    sala.sqlmodel_update(data.model_dump())
    db.add(sala)
    db.commit()
    db.refresh(sala)
    return sala


@router.delete("/{sala_id}", responses=exceptions.not_found)
def eliminar_sala(
    sala_id: int,
    db: SessionDep,
):
    sala = db.get(Sala, sala_id)
    if not sala:
        raise HTTPException(status_code=404, detail=exceptions.SALA_NO_ENCONTRADA)
    db.delete(sala)
    db.commit()
    return {"message": "Sala eliminada correctamente"}
