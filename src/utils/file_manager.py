import json
import os

def guardar_datos(nombre_archivo, datos):
    carpeta = os.path.dirname(nombre_archivo)
    if not os.path.exists(carpeta):
        os.makedirs(carpeta)

    with open(nombre_archivo, "w") as archivo:
        json.dump(datos, archivo, indent=4)
    
def cargar_datos(nombre_archivo):
    with open(nombre_archivo, "r") as archivo:
        return json.load(archivo)
    