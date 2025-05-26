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
        "descripcion" : self.descripcion,
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

class Reserva():
    def __init__(self, id_reserva, nombre_vivienda, precio_reserva, nombre_persona, apellidos_persona, fecha_entrada, 
    fecha_salida, numero_adultos, numero_ninos, telefono, direccion, ciudad, provincia, codigo_postal, pais):
        
        self.id_reserva = id_reserva
        self.nombre_vivienda = nombre_vivienda
        self.precio_reserva = precio_reserva
        self.nombre_persona = nombre_persona
        self.apellidos_persona = apellidos_persona
        self.fecha_entrada = fecha_entrada
        self.fecha_salida = fecha_salida
        self.numero_adultos = numero_adultos
        self.numero_ninos = numero_ninos
        self.telefono = telefono
        self.direccion = direccion
        self.ciudad = ciudad
        self.provincia = provincia
        self.codigo_postal = codigo_postal
        self.pais = pais

    def to_dict(self):
        return {
            "id_reserva": self.id_reserva,
            "nombre_vivienda": self.nombre_vivienda,
            "precio_reserva": self.precio_reserva,
            "nombre_persona": self.nombre_persona,
            "apellidos_persona": self.apellidos_persona,
            "fecha_entrada": self.fecha_entrada,
            "fecha_salida": self.fecha_salida,
            "numero_adultos": self.numero_adultos,
            "numero_ninos": self.numero_ninos,
            "telefono": self.telefono,
            "direccion": self.direccion,
            "ciudad": self.ciudad,
            "provincia": self.provincia,
            "codigo_postal": self.codigo_postal,
            "pais": self.pais
        }
    def id_reserva(self, id_reserva, db):
        
        return 
