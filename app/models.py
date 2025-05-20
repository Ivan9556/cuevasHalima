#Clase cueva
class Vivienda:
    def __init__(self,nombre, descripcion, precio, disponibilidad=True):
        self.nombre = nombre
        self.descripcion = descripcion
        self.precio = precio
        self.disponibilidad = disponibilidad
    """
    "to_dict" se define para convertir una instancia de una clase (un objeto) en un diccionario Python (serelizarlos)
    MongoDB (a través de PyMongo) espera recibir diccionarios, no objetos personalizados
    Esta funcion covierte un objeto en un diccionario.
    """
    def to_dict(self):
        return {
        "nombre" : self.nombre,
        "huespedes" : self.descripcion,
        "precio" :  self.precio,
        "disponibilidad" : self.disponibilidad
        }
    """    
    Metodo disponible para comprobar que la vivienda esté reservada o libre según las fechas
    pasadas por el usuario a través del formulario
    """
    def disponible(self, fecha_entrada, fecha_salida, db):
        #Buscamos una resera con las 3 condiciones
        reserva = db.reservas.find_one({
            "nombre": self.nombre, #Nombre de la vivienda
            "fecha_entrada": {"$lte": fecha_salida}, #La fecha de salida tiene que ser antes de la salida del usuario
            "fecha_salida": {"$gte": fecha_entrada} #La fecha entrada debe ser despúes de la fecha de entrada
        })    
        return reserva is None #Devuelve true si la vivienda está disponible "is not Done" devuelve false y no estaría disponible 