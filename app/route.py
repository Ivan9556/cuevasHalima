"""
Este archivo define las rutas (endpoints) de la aplicación web.

Cada función decorada con @main.route corresponde a una URL específica.

Aquí se maneja la lógica para renderizar páginas HTML con `render_template`, 
gestionar formularios mediante `request`, y realizar acciones como enviar correos o acceder a la base de datos.

Blueprint permite organizar una aplicación Flask en componentes reutilizables y modulares.

'main': Es el nombre del Blueprint. Se usa luego para 
registrar rutas y para llamar con url_for('main.nombre_función').

__name__: Indica el módulo actual. Flask lo usa para localizar archivos 
relacionados (por ejemplo, plantillas o archivos estáticos si se personaliza).
"""
from flask import Blueprint, render_template, url_for, flash, request, redirect, current_app, jsonify
from flask_mail import Message
from . import mail #Iniciandolo previamente en __init__.py
from app import mongo # importa el objeto mongo de __init__.py
from .models import Vivienda, Reserva
from datetime import datetime



main = Blueprint('main' ,__name__)

@main.route('/') #se carga desde la raiz index.html
def inicio():
    return render_template('index.html') #busca html en 'template'

@main.route('/sobre-nosotros')
def sobre_nosotros():
    return render_template('sobre-nosotros.html')

@main.route('/cueva')
def cueva():
    return render_template('cueva.html')

@main.route('/que-hacer')
def que_hacer():
    return render_template('que-hacer.html')

@main.route('/encuentranos')
def encuentranos():
    return render_template('encuentranos.html')

@main.route('/reserva')
def reserva():
    return render_template('reserva.html')

@main.route('/formulario-reserva')
def formulario_reserva():
    return render_template('formulario-reserva.html')

@main.route('/encuentranos', methods=['POST'])
def enviar_mensaje():
    nombre = request.form.get('nombre') 
    correo = request.form.get('correo')
    asunto = request.form.get('asunto')
    mensaje = request.form.get('mensaje')

    if not nombre or not correo:
        flash('Algunos campos son obligatorios')
        return redirect(url_for('main.encuentranos'))
    """
    No se debe utilizar en sender otro correo que no sea el tuyo piopio
    Gmail bloquea correos que afirman venir de una dirección que no coincide con la autenticación SMTP
    Para Gmail hay que utilizar la clave app, si no ninja2 devuelve una excepcion
    """
    msg = Message(
        subject = asunto,
        sender = current_app.config['MAIL_USERNAME'],
        recipients = ['cuevashalima@gmail.com'],
        body = f"""
        Nombre: {nombre}
        Correo-Electronico: {correo}

        Mensaje:
        {mensaje}
        """    
    )
    mail.send(msg)
    #Guardamos el mensaje para utilizarlo en la plantilla que renderice
    flash('Mensaje enviado correctamente')
    return redirect(url_for('main.encuentranos'))

@main.route("/test-db")
def test_db():    
    try:
        # Accede a la base de datos y realiza un ping
        db = mongo.db  # Accede al cliente MongoDB
        db.command("ping")
        return jsonify({"Insetada vivienda nueva"})
        
        return jsonify({"status": "Conectado a MongoDB correctamente"})
    except Exception as e:
        return jsonify({"error": str(e)})

@main.route('/buscar-reserva', methods=['GET'])
def buscar_reserva():
    db= mongo.db
    #Recogemos los datos del formulario y los convertimos en "datetime" para comparar fechas
    #Utilizamos '%Y-%m-%d' para covertir la cadena str a datetime
    fecha_entrada = request.args['entrada']
    fecha_salida = request.args['salida']
    numero_adultos = request.args['adultos']
    numero_ninos = request.args['ninos']

    #Recogemos el número de noches de las fechas señaladas por el metodo .days (datetime)
    cantidad_noches = (fecha_salida - fecha_entrada).days
    
    #Obtenemos todas las viviendas disponibles en la bd
    listaViviendas = db.viviendas.find({})

    #Definimos una lista vacía para añadir las viviendas que esten disponibles
    viviendas_disponibles = []

    #Recorremos cada vivienda, 'v' se convierte en un diccionario de Python donde almacena la info de MongoDB (JSON)
    for v in listaViviendas:
        #Esa informacion la recorremos con el for y vamos añadiendo a los parámetros del constructor esos datos
        vivienda = Vivienda(
            nombre=v['nombre'],
            descripcion=v['descripcion'],
            precio=v['precio']
        )
        #Comprovamos si la vivienda está disponible con nuestro método "disponible"
        if vivienda.disponible(fecha_entrada, fecha_salida, db):
            #Si se cumple, añadimos la vivienda a la lista
            viviendas_disponibles.append(vivienda)

    #Renderizamos la pagina de nuevo y le pasamos las viviendas y el número de noches para que las represente
    return render_template(viviendas=viviendas_disponibles, cantidad_noches = cantidad_noches, 
    fecha_entrada = fecha_entrada, fecha_salida = fecha_salida, numero_adultos = numero_adultos ,numero_ninos = numero_ninos)

@main.route('/form_reserva', methods=['POST'])
def hacer_reserva():

    db = mongo.db

    id_reserva = Reserva.generar_id(db)

    nombre_vivienda = request.form["nombre_vivienda"]
    precio_reserva = request.form["precio_vivienda"]
    nombre_persona = request.form["nombre_persona"]
    apellidos_persona = request.form["apellidos_persona"]
    fecha_entrada = request.form["fecha_entrada"]
    fecha_salida = request.form["fecha_salida"]
    numero_adultos = request.form["numero_adultos"]
    numero_ninos = request.form["numero_ninos"]
    telefono = request.form["telefono"]
    direccion = request.form["direccion"]
    ciudad = request.form["ciudad"]
    provincia = request.form["provincia"]
    codigo_postal = request.form["codigo_postal"]
    pais = request.form["pais"]



    reserva = Reserva(
        id_reserva= id_reserva, 
        nombre_vivienda=nombre_vivienda,
        precio_reserva=precio_reserva,
        nombre_persona=nombre_persona,
        apellidos_persona=nombre_persona,
        fecha_entrada=fecha_entrada,
        fecha_salida=fecha_salida,
        numero_adultos=numero_adultos,
        numero_ninos=numero_ninos,
        telefono=telefono,
        direccion=direccion,
        ciudad=ciudad,
        provincia=provincia,
        codigo_postal=codigo_postal,
        pais=pais
    )

    db.reservas.insert_one(reserva.to_dict())

    print("reserva insertada correctamente")

    return render_template("/reserva.html")
