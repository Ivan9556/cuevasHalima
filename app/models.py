#Clase cueva
class Vivienda:
    def __init__(self,nombre, descripcion, precio, img, capacidad):
        self.nombre = nombre
        self.descripcion = descripcion
        self.precio = precio
        self.img = img
        self.capacidad = capacidad
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
        "img" : self.img,
        "capacidad" : self.capacidad
        }
    """    
    Metodo disponible para comprobar que la vivienda esté reservada o libre según las fechas
    pasadas por el usuario a través del formulario
    """
    def disponible(self, fecha_entrada, fecha_salida, db):
        #Buscamos una resera con las 3 condiciones
        reserva = db.reservas.find_one({
            "nombre_vivienda": self.nombre, #Nombre de la vivienda
            "fecha_entrada": {"$lte": fecha_salida}, #La fecha de salida tiene que ser antes de la salida del usuario
            "fecha_salida": {"$gte": fecha_entrada} #La fecha entrada debe ser despúes de la fecha de entrada
        })    
        return reserva is None #Devuelve true si la vivienda está disponible "is not Done" devuelve false y no estaría disponible 

    @staticmethod
    def precio_reserva(n_personas, n_noches):
        
        match n_personas:

            case 1:
                p_total = 78 * n_noches
            case 2:
                p_total = 82 * n_noches
            case 3:
                p_total = 103 * n_noches
            case 4:
                p_total = 116 * n_noches
            case 5:
                p_total = 129 * n_noches
            case 6:
                p_total = 138 * n_noches
            case _:
                p_total = 144 * n_noches

        return p_total

class Reserva():
    def __init__(self, id_reserva, nombre_vivienda, precio_reserva, nombre_persona, apellidos_persona, fecha_entrada, 
    fecha_salida, numero_adultos, numero_ninos, telefono, correo, direccion, ciudad, provincia, codigo_postal, pais, estado):
        
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
        self.correo = correo
        self.direccion = direccion
        self.ciudad = ciudad
        self.provincia = provincia
        self.codigo_postal = codigo_postal
        self.pais = pais
        self.estado = estado

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
            "correo": self.correo,
            "direccion": self.direccion,
            "ciudad": self.ciudad,
            "provincia": self.provincia,
            "codigo_postal": self.codigo_postal,
            "pais": self.pais,
            "estado": self.estado
        }
    """
    Usamos la colleccion "contador", donde buscamos el documento con id llamado "id_reserva", "$inc" le indicamos a Mongo que 
    incremente el valor en 1, comprobamos que exista documento con "upsert = true" y por último devolvemos el documento con el 
    valor actualizado con "return_document" 
    """
    @staticmethod
    def generar_id(db):
        resultado = db.contador.find_one_and_update(
                { "_id " : "id_reserva" },
                { "$inc" : { "valor" : 1}},
                upsert = True,
                return_document = True
        )
        return resultado["valor"]
"""
@classmethod es un decorador que indica a Python que el método pertenece a ka clase, no a una instancia de la clase.
En vez de usar "self" (representa una instancia), recibe "cls", que representa la clase misma. Útil si queremos acceder
al método de la clase, pero no a un objeto.
Podemos unar también @staticmethod, no necesita pasar "cls" ni "self" dentro del método ya que lo que hacemos es hacer estático el 
método y por lo tanto no depende de ninguna instancia.
"""
