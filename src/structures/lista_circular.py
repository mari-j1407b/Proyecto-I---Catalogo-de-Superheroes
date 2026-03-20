class Nodo_circular():
    def __init__(self,value):
        self.value = value
        self.siguiente = None
class lista_circular():
    def __init__(self):
        self.cabeza = None
    def insertar_final(self,value):
        nuevo = Nodo_circular(value)
        if self.cabeza is None:
            self.cabeza = nuevo
            nuevo.siguiente = nuevo
            return
        actual = self.cabeza
        while actual.siguiente != self.cabeza:
            actual =actual.siguiente
        actual.siguiente = nuevo
        nuevo.siguiente = self.cabeza
    def recorrer(self):
        if self.cabeza is None:
            return
        actual = self.cabeza
        while True:
            print(actual.value)
            actual = actual.siguiente
            if actual == self.cabeza:
                break
                
            


