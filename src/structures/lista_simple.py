class Nodo_simple():
    def __init__(self,value):
        self.value = value
        self.siguiente = None
class Lista_simple():
    def __init__(self):
        self.cabeza = None
    def insertar_final(self,value):
        nuevo = Nodo_simple(value)
        if self.cabeza is None:
            self.head = nuevo
            return
        actual = self.cabeza
        while actual.siguiente is not None:
            actual = actual.siguiente
        actual.siguiente = nuevo
    def recorrer(self):
        actual = self.cabeza
        while actual is not None:
            print(actual.value)
            actual = actual.siguiente
    
