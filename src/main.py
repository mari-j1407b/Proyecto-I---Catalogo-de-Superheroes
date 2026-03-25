import sys
import os
import json
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QToolButton
from PyQt6.QtGui import QIcon
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
        
        # 🔥 DEBUG: ver nombres reales de botones
        print("\n--- BOTONES REALES EN LA INTERFAZ ---")
        for b in self.findChildren(QToolButton):
            print(b.objectName())
        
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
        # Conexiones de busqueda
      
        self.ui.stackedWidget.setCurrentIndex(0) 
        self.ui.stackedWidget_3.setCurrentIndex(0) 
        self.actualizar_labels_personajes()

        self.actualizar_labels_comics()

    # --- CARGA ---
    def cargar_datos_en_estructuras(self):
        # 1. CARGAR PERSONAJES
        try:
            ruta_p = 'data/personajes_locales.json'
            if os.path.exists(ruta_p):
                with open(ruta_p, 'r', encoding='utf-8') as f:
                    for p in json.load(f):
                        nombre = p.get('name', 'N/A')
                        # Regla Mari: minúsculas y guiones
                        img_name = nombre.lower().replace(" ", "-") + ".jpg"
                        
                        obj_p = Personaje(p.get('id'), nombre, p.get('deck', 'Sin descripción'), img_name)
                        self.lista_personajes.insertar(obj_p)
            print(f"✅ Cargados {self.lista_personajes.longitud} personajes.")
        except Exception as e:
            print(f"Error cargando personajes: {e}")

        try:
            ruta_c = 'data/comics_locales.json'
            if os.path.exists(ruta_c):
                with open(ruta_c, 'r', encoding='utf-8') as f:
                    for c in json.load(f):
                        # En cómics el nombre suele venir en volume -> name
                        nombre_v = c.get('volume', {}).get('name', 'Cómic')
                        # Regla Mari: minúsculas, guiones y sufijo -comic
                        img_name = nombre_v.lower().replace(" ", "-") + "-comic.jpg"
                        
                        obj_c = Comic(c.get('id'), nombre_v, c.get('deck', 'N/A'), "2026", "N/A", img_name)
                        self.lista_comics.insertar(obj_c)
            print(f"✅ Cargados {self.lista_comics.longitud} cómics.")
        except Exception as e:
            print(f"Error cargando cómics: {e}")

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
        labels = {
            0: ["label_12","label_13","label_34","label_35","label_36","label_37","label_38","label_39","label_40","label_41"],
            1: ["label_52","label_53","label_54","label_55","label_56","label_57","label_58","label_59","label_60","label_61"],
            2: ["label_62","label_63","label_64","label_65","label_66","label_67","label_68","label_69","label_70","label_71"]
        }
        self.llenar_datos(labels[indice], self.lista_comics, indice, "titulo", "comics")

    def actualizar_labels_personajes(self):
        indice = self.ui.stackedWidget_3.currentIndex()
        labels = {
            0: ["label_89","label_88","label_87","label_86","label_85","label_84","label_83","label_82","label_81","label_80"],
            1: ["label_79","label_78","label_77","label_76","label_75","label_74","label_73","label_72","label_22","label_21"],
            2: ["label_99","label_98","label_97","label_96","label_95","label_94","label_93","label_92","label_91","label_90"]
        }
        self.llenar_datos(labels[indice], self.lista_personajes, indice, "nombre", "personajes")



    def llenar_datos(self, nombres_labels, lista, num_pag, atributo, subcarpeta):
        puntero = lista.cabeza
        # Saltamos los elementos de las páginas anteriores
        for _ in range(num_pag * 10):
            if puntero: puntero = puntero.siguiente
        for i in range(len(nombres_labels)):
            label = self.findChild(QLabel, nombres_labels[i])
            if label:
                if puntero:
                    texto = getattr(puntero.dato, atributo, "N/A")
                    imagen = getattr(puntero.dato, "imagen", "")
                    label.setText(f'"{texto}"')
                    # Buscamos el botón en el mismo cuadro (frame/widget)
                    boton = label.parent().findChild(QToolButton)
                    # USAMOS LA SUBCARPETA CORRECTA (personajes o comics)
                    ruta_imagen = os.path.join("assets", subcarpeta, imagen)

                    # 🔥 AGREGA ESTA LÍNEA DE DEBUG AHORA 🔥
                    print(f"🔍 DEBUG [{subcarpeta}]: Buscando archivo en -> {os.path.abspath(ruta_imagen)}")

                    if boton:
                        if os.path.exists(ruta_imagen):
                            boton.setIcon(QIcon(ruta_imagen))
                        else:    
                            boton.setIcon(QIcon(os.path.join("assets", "img", "placeholder.png")))
                    puntero = puntero.siguiente
                else:
                    label.setText("") 


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = MundoComic()
    ventana.show()
    sys.exit(app.exec())