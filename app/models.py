#Clase cueva
class cueva:
    def __init__(self, id ,nombre, huespedes, precio):
        self.id = id
        self.nombre = nombre
        self.huespedes = huespedes
        self.precio = precio
    def to_dict(self):
        return {
        "id" : self.id,
        "nombre" : self.nombre,
        "huespedes" : self.huespedes,
        "precio" :  self.precio
        }        
