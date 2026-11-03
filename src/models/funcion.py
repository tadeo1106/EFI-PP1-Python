from typing import TYPE_CHECKING, Optional

from pydantic import NaiveDatetime
from sqlmodel import Field, Relationship, SQLModel

from src.models.config import Entradas, Precio
from src.models.resumenes import PeliculaResumen
from src.models.sala import SalaPublic

if TYPE_CHECKING:
    from src.models.pelicula import Pelicula
    from src.models.sala import Sala


class FuncionBase(SQLModel):
    fecha_hora: NaiveDatetime
    precio: Precio
    entradas_disponibles: Entradas
    sala_id: int = Field(foreign_key="sala.id")
    pelicula_id: int = Field(foreign_key="pelicula.id")


class FuncionCreate(FuncionBase):
    pass


class FuncionUpdate(FuncionBase):
    pass


class Funcion(FuncionBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    sala: Optional["Sala"] = Relationship(back_populates="funciones")
    pelicula: Optional["Pelicula"] = Relationship(back_populates="funciones")


class FuncionPublic(FuncionBase):
    id: int


class FuncionNested(FuncionPublic):
    pelicula: PeliculaResumen
    sala: SalaPublic
