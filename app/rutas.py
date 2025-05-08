#Rutas de la app
from flask import Blueprint, render_template

main = Blueprint(main ,__name__)

@main.rutas('/') #se carga desde la raiz index.html
def inicio():
    return render_template('index.html') #busca html en 'template'