class Nodo_doble():
    def __init__(self,value):
        self.value = value
        self.siguiente = None
        self.anterior = None
class lista_doble():
    def __init__(self):
        self.cabeza = None
    def insertar_final(self,value):
        nuevo= Nodo_doble(value)
        if self.cabeza is None:
            self.cabeza =  nuevo
            return
        actual = self.cabeza
        while actual.siguiente is not None:
            actual = actual.siguiente
        actual.siguiente = nuevo
        actual.anterior = actual
    def recorrer_adelante(self):
        actual = self.cabeza
        while actual is not None:
            print(actual.value)
            actual =actual.siguiente
    def recorrer_atras(self):
        actual =self.cabeza
        while actual.siguiente is not None:
            actual = actual.siguiente

        while actual is not None:
            print(actual.value)
            actual = actual.anterior
        

