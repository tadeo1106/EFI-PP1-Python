from typing import Annotated

from sqlmodel import Field

NombreGenero = Annotated[str, Field(min_length=2, max_length=50)]

NombrePelicula = Annotated[str, Field(min_length=1, max_length=150)]
DescripcionPelicula = Annotated[str | None, Field(max_length=1000)]
UrlPortada = Annotated[str | None, Field(max_length=500)]

NombreSala = Annotated[str, Field(min_length=1, max_length=30)]
Capacidad = Annotated[int, Field(gt=0, le=1000)]

Precio = Annotated[float, Field(gt=0)]
Entradas = Annotated[int, Field(ge=0)]
