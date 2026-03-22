import sys
import os
import json
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel
from ui.interfaz import Ui_VentanaPrincipal 
from models.comic import Comic
from models.personaje import Personaje
from structures.lista_doble import ListaDoble

# Configuración de rutas
ruta_del_archivo = os.path.abspath(__file__)
directorio_src = os.path.dirname(ruta_del_archivo)
proyecto_raiz = os.path.dirname(directorio_src)
os.chdir(proyecto_raiz)

class MundoComic(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_VentanaPrincipal() 
        self.ui.setupUi(self)
        
        self.lista_comics = ListaDoble()
        self.lista_personajes = ListaDoble()
        
        self.cargar_datos_en_estructuras()
        
        # Conexiones
        self.ui.btn_comics.clicked.connect(self.mostrar_seccion_comics)
        self.ui.btn_personajes.clicked.connect(self.mostrar_seccion_personajes)

        self.ui.btn_sig_comics.clicked.connect(self.cambiar_pag_comics_sig)
        self.ui.btn_ant_comics.clicked.connect(self.cambiar_pag_comics_ant)

        self.ui.btn_sig_personajes.clicked.connect(self.cambiar_pag_personajes_sig)
        self.ui.btn_ant_personajes.clicked.connect(self.cambiar_pag_personajes_ant)

        self.ui.stackedWidget.setCurrentIndex(0)
        self.actualizar_labels_comics()

    def cargar_datos_en_estructuras(self):
        try:
            ruta_p = 'data/personajes_locales.json'
            if os.path.exists(ruta_p):
                with open(ruta_p, 'r', encoding='utf-8') as f:
                    datos_p = json.load(f)

                    for p in datos_p:
                        id_val = p.get('id', 0)
                        nombre_val = p.get('name', 'N/A')
                        desc_val = p.get('deck', 'Sin descripción')
                        img_val = p.get('image', {}).get('small_url', '')

                        obj_p = Personaje(id_val, nombre_val, desc_val, img_val)
                        self.lista_personajes.insertar(obj_p)
                        
                        obj_c = Comic(id_val, nombre_val, desc_val, "2026", "N/A", img_val)
                        self.lista_comics.insertar(obj_c)
        except Exception as e:
            print(f"Error en carga: {e}")

    # --- NAVEGACIÓN ---
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

    # --- RENDER ---
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
        puntero = lista.cabeza

        for _ in range(num_pag * 10):
            if puntero:
                puntero = puntero.siguiente

        sin_datos = True  # 👈 para detectar si no hay nada

        for i, nombre in enumerate(nombres_labels):
            label_obj = self.findChild(QLabel, nombre)

            if label_obj:
                if puntero:
                    texto = getattr(puntero.dato, atributo, "N/A")
                    label_obj.setText(f'"{texto}"')
                    puntero = puntero.siguiente
                    sin_datos = False
                else:
                    # 👇 SOLO el primer label muestra el mensaje
                    if i == 0 and sin_datos:
                        label_obj.setText("No hay más resultados")
                    else:
                        label_obj.setText("")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = MundoComic()
    ventana.show()
    sys.exit(app.exec())