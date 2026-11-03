# PP1-EFI-Python - Cine API

---

## Integrantes

- **Tadeo Frias**
- **Lucas Molinas Sanchez**

---

## Estructura del Proyecto

```text
EFI/
├── alembic/                # Configuraciones y versiones de migraciones
│   └── versions/           # Scripts de migración de esquema
├── src/
│   ├── core/
│   │   └── exceptions.py   # Mensajes y esquemas de error HTTP (404, 409)
│   ├── models/             # Modelos SQLModel (Base, Table, Public, Nested)
│   │   ├── config.py       # Tipos y validaciones con Annotated
│   │   ├── funcion.py
│   │   ├── genero.py
│   │   ├── pelicula.py
│   │   ├── resumenes.py
│   │   └── sala.py
│   ├── routers/            # Path operations agrupadas por recurso
│   │   ├── funcion.py
│   │   ├── genero.py
│   │   ├── pelicula.py
│   │   └── sala.py
│   ├── database.py         # Configuración del Engine de base de datos y SessionDep
│   └── main.py             # Instancia de FastAPI, CORS y registro de routers
├── pyproject.toml          # Metadatos del proyecto y dependencias
├── requirements.txt        # Dependencias compiladas para deployment
└── README.md               # Documentación general del proyecto
```
