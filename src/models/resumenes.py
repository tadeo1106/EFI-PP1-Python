from datetime import datetime

from sqlmodel import SQLModel


class PeliculaResumen(SQLModel):
    id: int
    nombre: str
    portada: str | None = None


class FuncionResumen(SQLModel):
    id: int
    fecha_hora: datetime
    precio: float
    entradas_disponibles: int
