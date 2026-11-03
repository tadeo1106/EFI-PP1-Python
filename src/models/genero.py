from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

from src.models.config import NombreGenero
from src.models.resumenes import PeliculaResumen

if TYPE_CHECKING:
    from src.models.pelicula import Pelicula


class GeneroBase(SQLModel):
    nombre: NombreGenero


class GeneroCreate(GeneroBase):
    pass


class GeneroUpdate(GeneroBase):
    pass


class Genero(GeneroBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    peliculas: list["Pelicula"] = Relationship(back_populates="genero")


class GeneroPublic(GeneroBase):
    id: int


class GeneroNested(GeneroPublic):
    peliculas: list[PeliculaResumen] = []
