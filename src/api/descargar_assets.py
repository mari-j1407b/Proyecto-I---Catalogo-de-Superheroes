import requests
import os
import time
import re

API_KEY = "f4748b79d0a351345220d671c07880ff5ebb10bc"
HEADERS = {"User-Agent": "ProyectoAssetsMarvel_V2"}

def limpiar_nombre_segun_mari(nombre, es_comic=False):
    if not nombre: return "sin-nombre"
    nombre_limpio = nombre.lower()
    nombre_limpio = re.sub(r'[^a-z0-9\s-]', '', nombre_limpio)
    nombre_limpio = nombre_limpio.strip().replace(" ", "-")
    nombre_limpio = re.sub(r'-+', '-', nombre_limpio)
    return f"{nombre_limpio}-comic" if es_comic else nombre_limpio

def ejecutar_descargas():
    tareas = [
        ["characters", "assets/personajes", False],
        ["issues", "assets/comics", True]
    ]

    for endpoint, carpeta, es_comic in tareas:
        if not os.path.exists(carpeta): os.makedirs(carpeta, exist_ok=True)
        
        print(f"\n--- 📦 Revisando {endpoint} en {carpeta} ---")
        api_url = f"https://comicvine.gamespot.com/api/{endpoint}/?api_key={API_KEY}&format=json&limit=100"
        
        try:
            res = requests.get(api_url, headers=HEADERS)
            if res.status_code == 420:
                print("⚠️ Comic Vine dice: 'Vas muy rápido'. Esperando 10 segundos...")
                time.sleep(10)
                continue
            
            items = res.json().get('results', [])
            exitos = 0

            for item in items:
                # Lógica para obtener el nombre
                nombre_raw = item.get('name') if not es_comic else item.get('volume', {}).get('name')
                if not nombre_raw or not item.get('image'): continue

                nombre_limpio = limpiar_nombre_segun_mari(nombre_raw, es_comic=es_comic)
                ruta_final = f"{carpeta}/{nombre_limpio}.jpg"

                # 🚀 PASO CLAVE: Si ya existe, no lo descargues otra vez
                if os.path.exists(ruta_final):
                    exitos += 1
                    continue

                img_url = item['image'].get('medium_url')
                if not img_url: continue

                try:
                    img_res = requests.get(img_url, headers=HEADERS, timeout=10)
                    if img_res.status_code == 200:
                        with open(ruta_final, 'wb') as f:
                            f.write(img_res.content)
                        print(f"✅ Nuevo: {nombre_limpio}.jpg")
                        exitos += 1
                        time.sleep(0.5) # Pausa un poco más larga para evitar bloqueos
                except Exception:
                    print(f"❌ Error saltado en: {nombre_limpio}")
                    continue

            print(f"✔️ {endpoint} al día: {exitos}/100 archivos en carpeta.")

        except Exception as e:
            print(f"💥 Error crítico en {endpoint}: {e}")

if __name__ == "__main__":
    ejecutar_descargas()