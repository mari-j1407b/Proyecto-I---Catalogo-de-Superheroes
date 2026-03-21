class Nodo:
    def __init__(self, dato):
        self.dato = dato
        self.siguiente = None
        self.anterior = None


class ListaDoble:
    def __init__(self):
        self.cabeza = None
        self.cola = None

    # ✅ Insertar al final
    def insertar(self, dato):
        nuevo = Nodo(dato)

        if self.cabeza is None:
            self.cabeza = self.cola = nuevo
        else:
            self.cola.siguiente = nuevo
            nuevo.anterior = self.cola
            self.cola = nuevo

    # ✅ Recorrer hacia adelante
    def recorrer_adelante(self):
        actual = self.cabeza
        while actual:
            print(actual.dato.nombre)
            actual = actual.siguiente

    # ✅ Recorrer hacia atrás
    def recorrer_atras(self):
        actual = self.cola
        while actual:
            print(actual.dato.nombre)
            actual = actual.anterior

    # ✅ Buscar por ID
    def buscar(self, id):
        actual = self.cabeza
        while actual:
            if actual.dato.id == id:
                return actual.dato
            actual = actual.siguiente
        return None