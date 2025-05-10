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
from flask import Blueprint, render_template, url_for, flash
from flask_mail import Message
from . import mail #Iniciandolo previamente en __init__.py


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

@main.route('/encuentranos', methods=['POST'])
def enviar_mensaje():
    nombre = request.form.get('nombre') 
    correo = request.form.get('correo')
    asunto = request.form.get('asunto')
    mensaje = request.form.get('mensaje')

    if not nombre or not correo:
        flash('Algunos campos son obligatorios')
        return redirect(url_for('main.inicio'))
    
    msg = Message(
        subject = asunto,
        sender = correo,
        recipients = [ejemplo_cuevas@hotmail.com],
        body = mensaje
    )
    mail.send(msg)
    flash('Mensaje enviado')
    return redirect(url_for('main.inicio'))