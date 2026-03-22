import sys
import os
import json
from PyQt6.QtWidgets import QApplication, QMainWindow
from ui.interfaz import Ui_VentanaPrincipal 
from models.comic import Comic
from models.personaje import Personaje
from structures.lista_doble import ListaDoble

# Configuración de rutas para asegurar que encuentre la carpeta 'data'
ruta_del_archivo = os.path.abspath(__file__)
directorio_src = os.path.dirname(ruta_del_archivo)
proyecto_raiz = os.path.dirname(directorio_src)
os.chdir(proyecto_raiz)

class MundoComic(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_VentanaPrincipal() 
        self.ui.setupUi(self)
        
        # 1. Estructuras de Datos
        self.lista_comics = ListaDoble()
        self.lista_personajes = ListaDoble()
        
        # 2. Carga de datos desde tu JSON
        self.cargar_datos_en_estructuras()
        
        # 3. Conexiones: Menú Principal
        self.ui.btn_comics.clicked.connect(self.mostrar_seccion_comics)
        self.ui.btn_personajes.clicked.connect(self.mostrar_seccion_personajes)

        # 4. Navegación: Cómics (stackedWidget_2)
        self.ui.btn_sig_comics.clicked.connect(self.cambiar_pag_comics_sig)
        self.ui.btn_ant_comics.clicked.connect(self.cambiar_pag_comics_ant)

        # 5. Navegación: Personajes (stackedWidget_3)
        self.ui.btn_sig_personajes.clicked.connect(self.cambiar_pag_personajes_sig)
        self.ui.btn_ant_personajes.clicked.connect(self.cambiar_pag_personajes_ant)

        # Estado inicial
        self.ui.stackedWidget.setCurrentIndex(0)
        self.actualizar_labels_comics()

    def cargar_datos_en_estructuras(self):
        """Carga datos usando los parámetros obligatorios de tus clases"""
        try:
            ruta_p = 'data/personajes_locales.json'
            if os.path.exists(ruta_p):
                with open(ruta_p, 'r', encoding='utf-8') as f:
                    datos_p = json.load(f)
                    for p in datos_p:
                        # Extraemos datos del JSON
                        id_val = p.get('id', 0)
                        nombre_val = p.get('name', 'N/A')
                        desc_val = p.get('deck', 'Sin descripción')
                        img_val = p.get('image', {}).get('small_url', '')

                        # Crear Personaje (id, nombre, descripcion, imagen)
                        obj_p = Personaje(id_val, nombre_val, desc_val, img_val)
                        self.lista_personajes.insertar(obj_p)
                        
                        # Crear Comic temporal (id, titulo, descripcion, fecha, isbn, imagen)
                        obj_c = Comic(id_val, nombre_val, desc_val, "2026", "N/A", img_val)
                        self.lista_comics.insertar(obj_c)
            else:
                print("⚠️ No se encontró data/personajes_locales.json")
        except Exception as e:
            print(f"❌ Error en carga: {e}")

    # --- LÓGICA DE PÁGINAS ---
    def mostrar_seccion_comics(self):
        self.ui.stackedWidget.setCurrentIndex(0)
        self.actualizar_labels_comics()

    def mostrar_seccion_personajes(self):
        self.ui.stackedWidget.setCurrentIndex(1)
        self.actualizar_labels_personajes()

    def cambiar_pag_comics_sig(self):
        sw = self.ui.stackedWidget_2
        if sw.currentIndex() < sw.count() - 1:
            sw.setCurrentIndex(sw.currentIndex() + 1)
            self.actualizar_labels_comics()

    def cambiar_pag_comics_ant(self):
        sw = self.ui.stackedWidget_2
        if sw.currentIndex() > 0:
            sw.setCurrentIndex(sw.currentIndex() - 1)
            self.actualizar_labels_comics()

    def cambiar_pag_personajes_sig(self):
        sw = self.ui.stackedWidget_3
        if sw.currentIndex() < sw.count() - 1:
            sw.setCurrentIndex(sw.currentIndex() + 1)
            self.actualizar_labels_personajes()

    def cambiar_pag_personajes_ant(self):
        sw = self.ui.stackedWidget_3
        if sw.currentIndex() > 0:
            sw.setCurrentIndex(sw.currentIndex() - 1)
            self.actualizar_labels_personajes()

    # --- RENDERIZADO ---
    def actualizar_labels_comics(self):
        indice = self.ui.stackedWidget_2.currentIndex()
        mapeo = {
            0: ["label_12", "label_13", "label_34", "label_35", "label_36", "label_37", "label_38", "label_39", "label_40", "label_41"],
            1: ["label_52", "label_53", "label_54", "label_55", "label_56", "label_57", "label_58", "label_59", "label_60", "label_61"],
            2: ["label_62", "label_63", "label_64", "label_65", "label_66", "label_67", "label_68", "label_69", "label_70", "label_71"]
        }
        self.llenar_datos(mapeo.get(indice, []), self.lista_comics, indice, "titulo")

    def actualizar_labels_personajes(self):
        indice = self.ui.stackedWidget_3.currentIndex()
        mapeo = {
            0: ["label_89", "label_88", "label_87", "label_86", "label_85", "label_84", "label_83", "label_82", "label_81", "label_80"],
            1: ["label_79", "label_78", "label_77", "label_76", "label_75", "label_74", "label_73", "label_72", "label_22", "label_21"],
            2: ["label_99", "label_98", "label_97", "label_96", "label_95", "label_94", "label_93", "label_92", "label_91", "label_90"]
        }
        self.llenar_datos(mapeo.get(indice, []), self.lista_personajes, indice, "nombre")

    def llenar_datos(self, nombres_labels, lista, num_pag, atributo):
        # Empezar desde la cabeza de la lista
        puntero = lista.cabeza
        
        # Saltar los elementos de las páginas anteriores (10 por página)
        for _ in range(num_pag * 10):
            if puntero:
                puntero = puntero.siguiente
        
        for nombre in nombres_labels:
            # Buscar el label dentro de self.ui
            label_obj = getattr(self.ui, nombre, None)
            if label_obj:
                if puntero:
                    # Obtener el valor (titulo o nombre) usando getattr para ser dinámicos
                    texto = getattr(puntero.dato, atributo, "N/A")
                    label_obj.setText(f'"{texto}"')
                    puntero = puntero.siguiente
                else:
                    label_obj.setText("") # Si no hay más datos, limpiar el label

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = MundoComic()
    ventana.show()
    sys.exit(app.exec())