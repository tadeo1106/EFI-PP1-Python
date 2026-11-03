from datetime import datetime

from sqlmodel import SQLModel


class GeneroResumen(SQLModel):
    id: int
    nombre: str


class PeliculaResumen(SQLModel):
    id: int
    nombre: str
    portada: str | None = None
    duracion: int
    descripcion: str
    genero: GeneroResumen


class FuncionResumen(SQLModel):
    id: int
    fecha_hora: datetime
    precio: float
