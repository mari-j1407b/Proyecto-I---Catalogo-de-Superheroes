import requests
import os
import time

API_KEY = "f4748b79d0a351345220d671c07880ff5ebb10bc"
HEADERS = {"User-Agent": "MiProyectoMarvel"}

def limpiar_nombre(nombre, es_comic=False):
    nombre_limpio = nombre.lower().replace(" ", "-")
    if es_comic:
        return f"{nombre_limpio}-comic"
    return nombre_limpio

def descargar_imagenes(tipo="characters", carpeta="assets/personajes"):
    url = f"https://comicvine.gamespot.com/api/{tipo}/?api_key={API_KEY}&format=json&limit=100"
    print(f"Obteniendo datos de {tipo}...")
    
    res = requests.get(url, headers=HEADERS)
    if res.status_code != 200: return

    items = res.json()['results']
    
    for i in items:
        nombre_original = i.get('name') or i.get('volume', {}).get('name')
        if not nombre_original: continue
        
        img_url = i['image']['medium_url']
        nombre_archivo = limpiar_nombre(nombre_original, es_comic=(tipo=="issues"))
        
        img_data = requests.get(img_url, headers=HEADERS).content
        
        ruta_final = f"{carpeta}/{nombre_archivo}.jpg"
        with open(ruta_final, 'wb') as f:
            f.write(img_data)
        
        print(f"✅ Guardado: {nombre_archivo}.jpg")
        time.sleep(0.1) 


descargar_imagenes("characters", "assets/personajes")
descargar_imagenes("issues", "assets/comics")