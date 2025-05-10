#Rutas de la app
from flask import Blueprint, render_template

"""
Blueprint permite organizar una aplicación Flask en componentes reutilizables y modulares.

'main': Es el nombre del Blueprint. Se usa luego para 
registrar rutas y para llamar con url_for('main.nombre_función').

__name__: Indica el módulo actual. Flask lo usa para localizar archivos 
relacionados (por ejemplo, plantillas o archivos estáticos si se personaliza).

"""
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
