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
from datetime import datetime, timedelta
import stripe



main = Blueprint('main' ,__name__)


def fechas_ocupadas(db):
    db = mongo.db
    #Almacenamos las reservas de la db
    reservas = db.reservas.find()
    #Numero de viviendas en total, para saber cuando una fecha está ocupada en todas 
    total_viviendas = db.viviendas.count_documents({})
    #Dicionario de fechas que se van a ocupar por cada vivienda
    lista_fechas = {}
    #Recorremos cada reserva y leemos a qué vivienda pertenece
    for reserva in reservas:
        vivienda = reserva["nombre_vivienda"]
        if vivienda not in lista_fechas:
            #Si esa vivienda aún no tiene fechas creamos un set() "conjunto vacío"
            lista_fechas[vivienda] = set()
        f_ini = reserva["fecha_entrada"]
        f_fin = reserva["fecha_salida"]
        #Agregamos las fechas de cada vivienda, usando la clave "nombre_vivienda" en el diccionario
        #No usamos for porque no estamos iterando, si no constuyendo un rango de fechas
        while f_ini <= f_fin:
            lista_fechas[vivienda].add(f_ini.strftime('%Y-%m-%d'))
            f_ini += timedelta(days=1)
            """
            Ej:
            "A": {"2025-06-01", "2025-06-02"},
            "B": {"2025-06-01", "2025-06-03"},
            """

    #Contamos cuantas viviendas tienen reservada cada fecha, creando un nuevo diccionario vacío
    contador_fechas = {}
    #Ahora recorremos la lista_fechas (diccionario anterior) pero solo las fechas almacenadas (sin claves)
    #Este primer for recorre la lista de fechas por vivienda 
    for fechas in lista_fechas.values():
        #Con este recorremos cada fecha dentro de la lista
        for fecha in fechas:
            #Y por último contamos cuantas veces aparece la fecha en todas las listas
            #Si es la primera vez a 0 le +1 y si existe le +1 
            contador_fechas[fecha] = contador_fechas.get(fecha, 0) + 1
    """
    Ejemplo:    
    "2025-06-01": 2,  # esta fecha está ocupada por 2 viviendas
    "2025-06-02": 1,  # esta solo por una

    Recorre todos los sets de fechas de cada vivienda. Por cada fecha, suma 1 al contador.

    Ultimo paso, agregar solo las fechas que esten ocupadas por todas las viviendas, si viviendas es = 2
    solo se bloquea las fechas con count == 2.
    fecha for.. Incluye la fecha en la lista si cumple..
    for fecha, count in.. Recorre cada uno de esos pares
    contador_fechas.items().. Devuelve los pares clave-valor del diccionario contador_fechas
    if count == total_viviendas.. Si el n. de viviendas que ocupa la fecha es igual al numero de viviendas en db
    """
    fechas_bloqueadas = [fecha for fecha, count in contador_fechas.items() if count == total_viviendas]

    return fechas_bloqueadas

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
    db= mongo.db
    fechas_reservadas = fechas_ocupadas(db)
    return render_template('reserva.html', fechas_reservadas = fechas_reservadas)

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
    
    #Variable db
    db= mongo.db

    #Recogemos los datos del formulario 
    entrada_str = request.args.get('entrada')
    salida_str = request.args.get('salida')
    numero_adultos = request.args.get('adultos')
    numero_ninos = request.args.get('niños')

    #los convertimos en "datetime" para comparar fechas. Utilizamos '%Y-%m-%d' para covertir la cadena str a datetime
    fecha_entrada = datetime.strptime(entrada_str , "%Y-%m-%d")
    fecha_salida = datetime.strptime(salida_str, "%Y-%m-%d")

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
            precio=int(v['precio']),
            img=v['img'],
            capacidad=v['capacidad']
        )
        if vivienda.disponible(fecha_entrada, fecha_salida, db):
            viviendas_disponibles.append(vivienda)
            
    fechas_reservadas = fechas_ocupadas(db)

    #Renderizamos la pagina de nuevo y le pasamos las viviendas y el número de noches para que las represente
    return render_template(
        '/reserva.html', 
        viviendas=viviendas_disponibles,
        cantidad_noches = cantidad_noches, 
        fecha_entrada = fecha_entrada, 
        fecha_salida = fecha_salida, 
        entrada_str = entrada_str,
        salida_str = salida_str,
        numero_adultos = numero_adultos,
        numero_ninos = numero_ninos,
        fechas_reservadas = fechas_reservadas

        )

@main.route('/form_reserva', methods=['POST'])
def hacer_reserva():

    db = mongo.db

    id_reserva = Reserva.generar_id(db)
    nombre_vivienda = request.form["nombre_vivienda"]
    precio_reserva = request.form["precio_vivienda"]
    nombre_persona = request.form["nombre_persona"]
    apellidos_persona = request.form["apellidos_persona"]
    fecha_entrada_str = request.form["fecha_entrada"]
    fecha_salida_str= request.form["fecha_salida"]
    numero_adultos = request.form["numero_adultos"]
    numero_ninos = request.form["numero_ninos"]
    telefono = request.form["telefono"]
    direccion = request.form["direccion"]
    ciudad = request.form["ciudad"]
    provincia = request.form["provincia"]
    codigo_postal = request.form["codigo_postal"]
    pais = request.form["pais"]


    #Pasamos las fechas a datetime
    fecha_entrada = datetime.strptime(fecha_entrada_str, "%Y-%m-%d %H:%M:%S" )
    fecha_salida = datetime.strptime(fecha_salida_str, "%Y-%m-%d %H:%M:%S")

    #Guardamos la reserva en la db
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

    fechas_reservadas = fechas_ocupadas(db)
    

    print("reserva insertada correctamente")

    return render_template("/reserva.html", fechas_reservadas = fechas_reservadas)

@main.route('/metodo-pago', methods=['POST'])
def realizar_pago():

    #Clave Stripe
    stripe.api_key = 'sk_test_51RVutIQ6yxCCrrhAY5KuAL4b48LqwXJ0W3xCk1o4TabzZSqV9hVGoxQcjTIJaPggCy8GQpOYs7EKBmkIbAQt8WRI00r2LEGouc'

    try:
        sesion = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'eur',
                    'product_data':{
                        'name': 'Reserva vivienda',
                    },
                    'unit_amount': 5000,
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url='http://127.0.0.1:5000/sucess',
            cancel_url='http://127.0.0.1:5000/cancel'
        )
        return redirect(sesion.url)
    except Exception as e:
        return jsonify(error=str(e)), 403

@main.route('/sucess')
def success():
    return 'Pago exitoso'

@main.route('/cancel')
def cancel():
    return 'El pago fallo'
