import json
import os

def guardar_datos(datos, nombre_archivo):
    """Tarea: Guardar datos en archivos locales (.json)"""
    if not os.path.exists('data'):
        os.makedirs('data')
    
    ruta = f"data/{nombre_archivo}.json"
    with open(ruta, 'w', encoding='utf-8') as f:
        json.dump(datos, f, indent=4, ensure_ascii=False)
    print(f" Archivo '{nombre_archivo}.json' guardado en /data")

def cargar_datos(nombre_archivo):
    """Tarea: Cargar datos desde archivos locales"""
    ruta = f"data/{nombre_archivo}.json"
    if os.path.exists(ruta):
        with open(ruta, 'r', encoding='utf-8') as f:
            return json.load(f)
    print(" El archivo no existe.")
    return None