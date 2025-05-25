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
    def __init__(self, id_reserva, nombre_vivienda, precio_reserva ,nombre_persona, apellidos_persona, fecha_entrada, 
        fecha_salida, numero_personas, telefono, direccion, ciudad, provincia, codigo_postal, pais):

        self.id_reserva = id_reserva
        self.nombre_vivienda = nombre_vivienda
        self.precio_reserva = precio_reserva
        self.nombre_persona = nombre_persona
        self.apellidos_persona = apellidos_persona
        self.fecha_entrada = fecha_entrada
        self.fecha_salida = fecha_salida
        self.numero_personas = numero_personas
        self.telefono = telefono
        self.direccion = ciudad
        self.provincia = provincia
        self.codigo_postal = codigo_postal
        self.pais = pais
    
    def to_dict(self):
        return{
            "id_reserva" : id_reserva,
            "nombre_vivienda" : nombre_vivienda,
            "precio_reserva" : precio_reserva,
            "nombre_persona" : nombre_persona,
            "apellidos_persona" : apellidos_persona,
            "fecha_entrada" : fecha_entrada,
            "fecha_salida" : fecha_salida,
            "numero_personas" : numero_personas,
            "telefono" : telefono,
            "direccion" : direccion,
            "provincia" : provincia,
            "codigo_postal" : codigo_postal,
            "pais" : pais
        }