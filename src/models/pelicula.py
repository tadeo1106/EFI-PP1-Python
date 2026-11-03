from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

from src.models.config import (
    DescripcionPelicula,
    Duracion,
    NombrePelicula,
    UrlPortada,
)
from src.models.genero import Genero, GeneroPublic
from src.models.resumenes import FuncionResumen

if TYPE_CHECKING:
    from src.models.funcion import Funcion


class PeliculaBase(SQLModel):
    nombre: NombrePelicula
    descripcion: DescripcionPelicula
    portada: UrlPortada = None
    genero_id: int = Field(foreign_key="genero.id")
    duracion: Duracion


class PeliculaCreate(PeliculaBase):
    pass


class PeliculaUpdate(PeliculaBase):
    pass


class Pelicula(PeliculaBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    genero: Optional[Genero] = Relationship(back_populates="peliculas")
    funciones: list["Funcion"] = Relationship(back_populates="pelicula")


class PeliculaPublic(PeliculaBase):
    id: int


class PeliculaNested(PeliculaPublic):
    genero: GeneroPublic
    funciones: list[FuncionResumen] = []
