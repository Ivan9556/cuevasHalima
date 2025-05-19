#Clase cueva
class Vivienda:
    def __init__(self,nombre, descripcion, precio, disponibilidad=True):
        self.nombre = nombre
        self.descripcion = descripcion
        self.precio = precio
        self.disponibilidad = disponibilidad
# to_dict se define para convertir una instancia de una clase (un objeto) en un diccionario Python (serelizarlos)
# MongoDB (a través de PyMongo) espera recibir diccionarios, no objetos personalizados
# Esta funcion covierte un objeto en un diccionario.
    def to_dict(self):
        return {
        "nombre" : self.nombre,
        "huespedes" : self.descripcion,
        "precio" :  self.precio,
        "disponibilidad" : self.disponibilidad
        }        
