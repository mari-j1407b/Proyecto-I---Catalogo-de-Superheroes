from api.marvel_api import obtener_personajes_completos
from  structures.lista_doble import ListaDoble

personajes = obtener_personajes_completos()
lista = ListaDoble()

for p in personajes:
    lista.insertar(p)