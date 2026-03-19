from utils.file_manager import guardar_datos, cargar_datos
from models.personaje import Personaje
from models.evento import Evento
from models.comic import Comic
import os


def datos_iniciales():
    p1 = Personaje(1, "Spider-Man", "Heroe de Nueva York", "spiderman.jpg")
    p2 = Personaje(2, "Iron Man", "Genio millonario", "ironman.jpg")

    return [p1, p2]


def guardar_personajes(personajes):
    lista = [p.to_dict() for p in personajes]
    guardar_datos("storage/personajes.json", lista)


def cargar_personajes():
    datos = cargar_datos("storage/personajes.json")

    personajes = []

    for p in datos:
        personaje = Personaje(
            p["id"],
            p["nombre"],
            p["descripcion"],
            p["imagen"]
        )
        personajes.append(personaje)

    return personajes


def obtener_personajes():
    ruta = "storage/personajes.json"

    if os.path.exists(ruta):
        print("📂 Cargando desde JSON...")
        return cargar_personajes()
    else:
        print("🌐 Generando datos iniciales...")
        personajes = datos_iniciales()
        guardar_personajes(personajes)
        return personajes


def obtener_comics_personaje(id_personaje):
    comics = []

    if id_personaje == 1:
        comics.append(Comic(1, "Amazing Fantasy #15", "Primera aparición", "1962", "123", "img.jpg"))

    return comics


def obtener_eventos_personaje(id_personaje):
    eventos = []

    if id_personaje == 1:
        eventos.append(Evento(1, "Civil War", "Conflicto de héroes"))
        eventos.append(Evento(2, "Secret Wars", "Multiverso"))

    return eventos


def obtener_personajes_completos():
    personajes = obtener_personajes()

    for p in personajes:
        eventos = obtener_eventos_personaje(p.id)
        comics = obtener_comics_personaje(p.id)

        for e in eventos:
            p.agregar_evento(e)

        for c in comics:
            p.agregar_comic(c)

    return personajes

