from api.marvel_api import obtener_comics, obtener_personajes
from utils.file_manager import guardar_datos, cargar_datos

def ejecutar_todo():
    print("--- PROCESAMIENTO DE DATOS (ejemplos de funcionamiento) ---")
    
    print("Descargando de la API...")
    datos_api = obtener_personajes()
    
    if datos_api:
        guardar_datos(datos_api, "personajes_locales")
        
        print("Cargando desde archivo local para verificar...")
        mis_datos_guardados = cargar_datos("personajes_locales")
        
        if mis_datos_guardados:
            print(f" Se procesaron {len(mis_datos_guardados)} personajes.")
            print(f"Primer personaje cargado: {mis_datos_guardados[0]['name']}")

if __name__ == "__main__":
    ejecutar_todo()