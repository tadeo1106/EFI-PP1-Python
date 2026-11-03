from typing import Any

PELICULA_NO_ENCONTRADA = "Pelicula no encontrada"
FUNCION_NO_ENCONTRADA = "Función no encontrada"
SALA_NO_ENCONTRADA = "Sala no encontrada"
GENERO_NO_ENCONTRADO = "Genero no encontrado"
GENERO_CON_PELICULAS = "No se puede borrar un género con películas"
SALA_CON_FUNCIONES = "No se puede borrar una sala con funciones"
PELICULA_CON_FUNCIONES = "La película tiene funciones asociadas y no se puede eliminar"
SALA_OCUPADA = "Ya existe una función en esa sala a esa hora"

not_found: dict[int | str, dict[str, Any]] = {
    404: {
        "description": "No se encontró el recurso con ese id",
        "content": {"application/json": {"example": {"detail": FUNCION_NO_ENCONTRADA}}},
    },
}

conflict_funcion: dict[int | str, dict[str, Any]] = {
    409: {
        "description": "Conflicto: el horario ya está ocupado",
        "content": {"application/json": {"example": {"detail": SALA_OCUPADA}}},
    }
}

conflict: dict[int | str, dict[str, Any]] = {
    409: {
        "description": "EL recurso tiene dependencias y no se puede borrar",
        "content": {"application/json": {"example": {"detail": GENERO_CON_PELICULAS}}},
    }
}
