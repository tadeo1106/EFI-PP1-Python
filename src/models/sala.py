from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

from src.models.config import Capacidad, NombreSala
from src.models.resumenes import FuncionResumen

if TYPE_CHECKING:
    from src.models.funcion import Funcion


class SalaBase(SQLModel):
    nombre: NombreSala
    capacidad: Capacidad


class SalaCreate(SalaBase):
    pass


class SalaUpdate(SalaBase):
    pass


class Sala(SalaBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    funciones: list["Funcion"] = Relationship(back_populates="sala")


class SalaPublic(SalaBase):
    id: int


class SalaNested(SalaPublic):
    funciones: list[FuncionResumen] = []
