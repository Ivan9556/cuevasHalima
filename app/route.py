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
from .models import Vivienda
from datetime import datetime


main = Blueprint('main' ,__name__)

@main.route('/') #se carga desde la raiz index.html
def inicio():
    return render_template('index.html') #busca html en 'template'

@main.route('/sobreNosotros')
def sobreNosotros():
    return render_template('sobreNosotros.html')

@main.route('/cueva')
def cueva():
    return render_template('cueva.html')

@main.route('/queHacer')
def queHacer():
    return render_template('queHacer.html')

@main.route('/encuentranos')
def encuentranos():
    return render_template('encuentranos.html')

@main.route('/reserva')
def reserva():
    return render_template('reserva.html')

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



@main.route('/buscar-reserva', methods=['POST'])
def buscar_reserva():
    db= mongo.db
    #Recogemos los datos del formulario y los convertimos en "datetime" para comparar fechas
    #Utilizamos '%Y-%m-%d' para covertir la cadena str a datetime
    fechaEntrada = datetime.strptime(request.form['fecha_entrada'], '%d-%m-%Y')
    fechaSalida = datetime.strptime(request.form['fecha_salida'], '%d-%m-%Y')
    
    #Obtenemos todas las viviendas disponibles en la bd
    listaViviendas = db.viviendas.find({})

    #Definimos una lista vacía para añadir las viviendas que esten disponibles
    viviendasDisponibles = []

    #Recorremos cada vivienda, 'v' se convierte en un diccionario de Python donde almacena la info de MongoDB (JSON)
    for v in listaViviendas:
        #Esa informacion la recorremos con el for y vamos añadiendo a los parámetros del constructor esos datos
        vivienda = Vivienda(
            nombre=v['nombre'],
            descripcion=v['descripcion'],
            precio=v['precio']
        )
        #Comprovamos si la vivienda está disponible con nuestro método "disponible"
        if vivienda.disponible(fechaEntrada, fechaSalida, db):
            #Si se cumple, añadimos la vivienda a la lista
            viviendasDisponibles.append(vivienda)
        #Renderizamos la pagina de nuevo y le pasamos la vivienda para que la represente
        return render_template('/reserva.html', viviendas=viviendasDisponibles)


"""
Funcion reserva
    adultos = request.form.get('adultos')
    ninos = request.form.get('ninos')

    reserva = {
        "fecha_entrada": fechaEntrada,
        "fecha_salida" : fechaSalida,
        "adultos" : int(adultos),
        "ninos" : int(ninos)
    }
    mongo.db.reservas.insert_one(reserva)
    flash('Reserva hecha correctamente')
    return redirect(url_for('main.reserva'))
"""

    