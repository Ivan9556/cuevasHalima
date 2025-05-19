#Clase cueva
class cueva:
    def __init__(self,nombre, descripcion, precio, disponibilidad=True):
        self.nombre = nombre
        self.descripcion = descripcion
        self.precio = precio
        self.disponibilidad = disponibilidad
    def to_dict(self):
        return {
        "nombre" : self.nombre,
        "huespedes" : self.descripcion,
        "precio" :  self.precio,
        "disponibilidad" : self.disponibilidad
        }        
