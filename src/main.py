from api.marvel_api import obtener_comics, obtener_personajes
from utils.file_manager import guardar_datos

def generar_todo_el_contenido():
    print("--- 🛠️ GENERANDO BASES DE DATOS LOCALES (100 elementos) ---")
    print("\n[1/2] Descargando y guardando personajes...")
    lista_personajes = obtener_personajes()
    if lista_personajes:
        guardar_datos(lista_personajes, "personajes_locales")
        print(f"✅ Se guardaron {len(lista_personajes)} personajes.")
    else:
        print("❌ Error al obtener personajes.")
    print("\n[2/2] Descargando y guardando cómics...")
    lista_comics = obtener_comics()
    if lista_comics:
        guardar_datos(lista_comics, "comics_locales")
        print(f"✅ Se guardaron {len(lista_comics)} cómics.")
    else:
        print("❌ Error al obtener cómics.")
if __name__ == "__main__":
    generar_todo_el_contenido()