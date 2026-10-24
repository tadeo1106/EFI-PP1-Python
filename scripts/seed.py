"""Script de poblado (seed) para la base de datos de EFI.

Reglas aplicadas:
- Sin tildes en nombres, generos ni descripciones.
- Generos unificados y unicos.
- Exactamente 3 salas: Sala 1, Sala 2, Sala 3.
- 10 peliculas obtenidas de PP1-EFI-JavaScript/ideas.
- Peliculas estrenadas: funciones a partir del 8 de noviembre de 2026.
- Peliculas no estrenadas: funciones en diciembre de 2026.
"""

from datetime import datetime

from sqlmodel import Session, select

from src.database import engine
from src.models.funcion import Funcion
from src.models.genero import Genero
from src.models.pelicula import Pelicula
from src.models.sala import Sala


def run_seed():
    with Session(engine) as session:
        print("Eliminando datos previos...")
        # Limpieza respetando integridad referencial
        for f in session.exec(select(Funcion)).all():
            session.delete(f)
        session.commit()

        for p in session.exec(select(Pelicula)).all():
            session.delete(p)
        session.commit()

        for s in session.exec(select(Sala)).all():
            session.delete(s)
        session.commit()

        for g in session.exec(select(Genero)).all():
            session.delete(g)
        session.commit()

        print("Insertando generos...")
        generos_data = [
            "Accion",
            "Terror",
            "Drama",
            "Suspenso",
            "Crimen",
            "Ciencia Ficcion",
        ]
        generos = {}
        for nombre in generos_data:
            genero = Genero(nombre=nombre)
            session.add(genero)
            session.flush()
            generos[nombre] = genero.id

        print("Insertando salas...")
        salas_data = [
            {"nombre": "Sala 1", "capacidad": 120},
            {"nombre": "Sala 2", "capacidad": 100},
            {"nombre": "Sala 3", "capacidad": 80},
        ]
        salas = {}
        for s in salas_data:
            sala = Sala(**s)
            session.add(sala)
            session.flush()
            salas[s["nombre"]] = sala.id

        print("Insertando peliculas...")
        peliculas_data = [
            # Peliculas ya estrenadas
            {
                "key": "batman",
                "nombre": "The Batman",
                "descripcion": (
                    "En su segundo ano luchando contra el crimen, Batman"
                    " explora la corrupcion existente en Gotham City y el"
                    " vinculo de esta con su propia familia, mientras persigue"
                    " a un asesino en serie conocido como el Acertijo."
                ),
                "portada": "/batman.jpg",
                "genero_id": generos["Accion"],
                "duracion": 176,
            },
            {
                "key": "it",
                "nombre": "IT: Capitulo Dos",
                "descripcion": (
                    "Veintisiete anos despues de su primer encuentro con el"
                    " aterrador Pennywise, el Club de los Perdedores se reune de"
                    " nuevo para poner fin a la maldicion en el pueblo de"
                    " Derry."
                ),
                "portada": "/it.jpg",
                "genero_id": generos["Terror"],
                "duracion": 169,
            },
            {
                "key": "joker",
                "nombre": "Joker",
                "descripcion": (
                    "La pasion de Arthur Fleck por hacer reir a la gente lo"
                    " lleva al limite en una sociedad que lo ignora y maltrata,"
                    " transformandolo progresivamente en el infame criminal"
                    " conocido como Joker."
                ),
                "portada": "/joker.jpg",
                "genero_id": generos["Drama"],
                "duracion": 122,
            },
            {
                "key": "lacasa",
                "nombre": "La Casa",
                "descripcion": (
                    "Una historia de intriga y secretos familiares donde los"
                    " limites entre la cordura y el engano se desdibujan: todos"
                    " tenemos una guerra privada que el otro desconoce."
                ),
                "portada": "/lacasa.jpg",
                "genero_id": generos["Suspenso"],
                "duracion": 95,
            },
            {
                "key": "losotros",
                "nombre": "Los Otros",
                "descripcion": (
                    "En una aislada mansion victoriana al final de la Segunda"
                    " Guerra Mundial, una madre protege a sus dos hijos"
                    " fotosensibles mientras extranas presencias amenazan su"
                    " hogar."
                ),
                "portada": "/losotros.jpg",
                "genero_id": generos["Terror"],
                "duracion": 104,
            },
            {
                "key": "scarface",
                "nombre": "Scarface",
                "descripcion": (
                    "Tony Montana, un refugiado cubano en Miami, construye un"
                    " poderoso y despiadado imperio del narcotrafico a costa de"
                    " la violencia, la ambicion desmedida y la paranoia."
                ),
                "portada": "/scarface.jpg",
                "genero_id": generos["Crimen"],
                "duracion": 170,
            },
            # Peliculas no estrenadas (proximamente)
            {
                "key": "domsday",
                "nombre": "Avengers: Doomsday",
                "descripcion": (
                    "Los heroes mas poderosos de la Tierra deben unirse ante la"
                    " mayor amenaza cosmica jamas enfrentada, el Doctor Doom,"
                    " que busca remodelar el multiverso a su voluntad."
                ),
                "portada": "/domsday.jpg",
                "genero_id": generos["Accion"],
                "duracion": 160,
            },
            {
                "key": "duna",
                "nombre": "Duna: Parte Tres",
                "descripcion": (
                    "La epica conclusion de la saga de Paul Atreides en Arrakis,"
                    " consolidando su liderazgo y enfrentando el destino de una"
                    " guerra santa que consume a toda la galaxia."
                ),
                "portada": "/duna.jpg",
                "genero_id": generos["Ciencia Ficcion"],
                "duracion": 165,
            },
            {
                "key": "exorcista",
                "nombre": "El Exorcista: Martires",
                "descripcion": (
                    "Una nueva y escalofriante entrega en la que la oscuridad"
                    " ancestral debe ser cazada antes de que consuma a una"
                    " nueva familia y a quienes intentan salvarlos."
                ),
                "portada": "/exorcista.jpg",
                "genero_id": generos["Terror"],
                "duracion": 118,
            },
            {
                "key": "spiderman",
                "nombre": "Spider-Man: Un Nuevo Dia",
                "descripcion": (
                    "Tras perderlo todo, Peter Parker intenta reconstruir su"
                    " vida en las calles de Nueva York mientras una nueva y"
                    " letal amenaza pone a prueba su deber como el Hombre"
                    " Arana."
                ),
                "portada": "/spiderman.jpg",
                "genero_id": generos["Accion"],
                "duracion": 135,
            },
        ]

        peliculas = {}
        for p in peliculas_data:
            key = p.pop("key")
            pelicula = Pelicula(**p)
            session.add(pelicula)
            session.flush()
            peliculas[key] = pelicula.id

        print("Insertando funciones...")
        funciones_data = [
            # --- Peliculas estrenadas: Funciones a partir del 8 de Noviembre de 2026 ---
            # The Batman
            {
                "pelicula_id": peliculas["batman"],
                "sala_id": salas["Sala 1"],
                "fecha_hora": datetime(2026, 11, 8, 17, 0),
                "precio": 4500.0,
                "entradas_disponibles": 110,
            },
            {
                "pelicula_id": peliculas["batman"],
                "sala_id": salas["Sala 2"],
                "fecha_hora": datetime(2026, 11, 9, 20, 30),
                "precio": 4500.0,
                "entradas_disponibles": 95,
            },
            {
                "pelicula_id": peliculas["batman"],
                "sala_id": salas["Sala 1"],
                "fecha_hora": datetime(2026, 11, 15, 17, 0),
                "precio": 4500.0,
                "entradas_disponibles": 120,
            },
            # IT: Capitulo Dos
            {
                "pelicula_id": peliculas["it"],
                "sala_id": salas["Sala 3"],
                "fecha_hora": datetime(2026, 11, 8, 22, 30),
                "precio": 4000.0,
                "entradas_disponibles": 75,
            },
            {
                "pelicula_id": peliculas["it"],
                "sala_id": salas["Sala 1"],
                "fecha_hora": datetime(2026, 11, 10, 22, 0),
                "precio": 4000.0,
                "entradas_disponibles": 100,
            },
            {
                "pelicula_id": peliculas["it"],
                "sala_id": salas["Sala 2"],
                "fecha_hora": datetime(2026, 11, 16, 22, 30),
                "precio": 4000.0,
                "entradas_disponibles": 85,
            },
            # Joker
            {
                "pelicula_id": peliculas["joker"],
                "sala_id": salas["Sala 2"],
                "fecha_hora": datetime(2026, 11, 8, 18, 0),
                "precio": 4000.0,
                "entradas_disponibles": 90,
            },
            {
                "pelicula_id": peliculas["joker"],
                "sala_id": salas["Sala 3"],
                "fecha_hora": datetime(2026, 11, 11, 20, 0),
                "precio": 4000.0,
                "entradas_disponibles": 70,
            },
            {
                "pelicula_id": peliculas["joker"],
                "sala_id": salas["Sala 1"],
                "fecha_hora": datetime(2026, 11, 17, 19, 30),
                "precio": 4000.0,
                "entradas_disponibles": 115,
            },
            # La Casa
            {
                "pelicula_id": peliculas["lacasa"],
                "sala_id": salas["Sala 3"],
                "fecha_hora": datetime(2026, 11, 8, 19, 30),
                "precio": 3500.0,
                "entradas_disponibles": 60,
            },
            {
                "pelicula_id": peliculas["lacasa"],
                "sala_id": salas["Sala 2"],
                "fecha_hora": datetime(2026, 11, 12, 18, 0),
                "precio": 3500.0,
                "entradas_disponibles": 80,
            },
            {
                "pelicula_id": peliculas["lacasa"],
                "sala_id": salas["Sala 3"],
                "fecha_hora": datetime(2026, 11, 18, 20, 30),
                "precio": 3500.0,
                "entradas_disponibles": 75,
            },
            # Los Otros
            {
                "pelicula_id": peliculas["losotros"],
                "sala_id": salas["Sala 1"],
                "fecha_hora": datetime(2026, 11, 8, 20, 30),
                "precio": 3500.0,
                "entradas_disponibles": 105,
            },
            {
                "pelicula_id": peliculas["losotros"],
                "sala_id": salas["Sala 3"],
                "fecha_hora": datetime(2026, 11, 13, 21, 0),
                "precio": 3500.0,
                "entradas_disponibles": 70,
            },
            {
                "pelicula_id": peliculas["losotros"],
                "sala_id": salas["Sala 2"],
                "fecha_hora": datetime(2026, 11, 19, 21, 30),
                "precio": 3500.0,
                "entradas_disponibles": 90,
            },
            # Scarface
            {
                "pelicula_id": peliculas["scarface"],
                "sala_id": salas["Sala 2"],
                "fecha_hora": datetime(2026, 11, 8, 21, 0),
                "precio": 4000.0,
                "entradas_disponibles": 85,
            },
            {
                "pelicula_id": peliculas["scarface"],
                "sala_id": salas["Sala 1"],
                "fecha_hora": datetime(2026, 11, 14, 21, 0),
                "precio": 4000.0,
                "entradas_disponibles": 110,
            },
            {
                "pelicula_id": peliculas["scarface"],
                "sala_id": salas["Sala 3"],
                "fecha_hora": datetime(2026, 11, 20, 19, 0),
                "precio": 4000.0,
                "entradas_disponibles": 75,
            },
            # --- Peliculas no estrenadas: Funciones en Diciembre de 2026 ---
            # Avengers: Doomsday
            {
                "pelicula_id": peliculas["domsday"],
                "sala_id": salas["Sala 1"],
                "fecha_hora": datetime(2026, 12, 18, 18, 0),
                "precio": 5000.0,
                "entradas_disponibles": 120,
            },
            {
                "pelicula_id": peliculas["domsday"],
                "sala_id": salas["Sala 1"],
                "fecha_hora": datetime(2026, 12, 18, 21, 30),
                "precio": 5000.0,
                "entradas_disponibles": 120,
            },
            {
                "pelicula_id": peliculas["domsday"],
                "sala_id": salas["Sala 2"],
                "fecha_hora": datetime(2026, 12, 19, 20, 0),
                "precio": 5000.0,
                "entradas_disponibles": 100,
            },
            {
                "pelicula_id": peliculas["domsday"],
                "sala_id": salas["Sala 3"],
                "fecha_hora": datetime(2026, 12, 20, 18, 0),
                "precio": 5000.0,
                "entradas_disponibles": 80,
            },
            # Duna: Parte Tres
            {
                "pelicula_id": peliculas["duna"],
                "sala_id": salas["Sala 2"],
                "fecha_hora": datetime(2026, 12, 17, 19, 0),
                "precio": 4800.0,
                "entradas_disponibles": 100,
            },
            {
                "pelicula_id": peliculas["duna"],
                "sala_id": salas["Sala 1"],
                "fecha_hora": datetime(2026, 12, 19, 17, 0),
                "precio": 4800.0,
                "entradas_disponibles": 115,
            },
            {
                "pelicula_id": peliculas["duna"],
                "sala_id": salas["Sala 3"],
                "fecha_hora": datetime(2026, 12, 21, 20, 30),
                "precio": 4800.0,
                "entradas_disponibles": 75,
            },
            # El Exorcista: Martires
            {
                "pelicula_id": peliculas["exorcista"],
                "sala_id": salas["Sala 3"],
                "fecha_hora": datetime(2026, 12, 5, 22, 0),
                "precio": 4200.0,
                "entradas_disponibles": 80,
            },
            {
                "pelicula_id": peliculas["exorcista"],
                "sala_id": salas["Sala 2"],
                "fecha_hora": datetime(2026, 12, 12, 22, 30),
                "precio": 4200.0,
                "entradas_disponibles": 95,
            },
            {
                "pelicula_id": peliculas["exorcista"],
                "sala_id": salas["Sala 1"],
                "fecha_hora": datetime(2026, 12, 26, 22, 0),
                "precio": 4200.0,
                "entradas_disponibles": 110,
            },
            # Spider-Man: Un Nuevo Dia
            {
                "pelicula_id": peliculas["spiderman"],
                "sala_id": salas["Sala 1"],
                "fecha_hora": datetime(2026, 12, 12, 18, 30),
                "precio": 4500.0,
                "entradas_disponibles": 120,
            },
            {
                "pelicula_id": peliculas["spiderman"],
                "sala_id": salas["Sala 2"],
                "fecha_hora": datetime(2026, 12, 15, 20, 0),
                "precio": 4500.0,
                "entradas_disponibles": 100,
            },
            {
                "pelicula_id": peliculas["spiderman"],
                "sala_id": salas["Sala 3"],
                "fecha_hora": datetime(2026, 12, 22, 17, 30),
                "precio": 4500.0,
                "entradas_disponibles": 80,
            },
        ]

        for f in funciones_data:
            funcion = Funcion(**f)
            session.add(funcion)

        session.commit()
        print("Poblado completado con exito!")


if __name__ == "__main__":
    run_seed()
