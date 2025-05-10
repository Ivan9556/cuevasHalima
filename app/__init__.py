"""
Este archivo se encarga de inicializar la aplicación Flask y sus extensiones.

- Crea una instancia de Flask.
- Carga la configuración desde un archivo externo (config.py).
- Inicializa extensiones como PyMongo, Flask-Mail, etc.
- Registra Blueprints para organizar las rutas por módulos.

"""

from flask import Flask
from flask_pymongo import PyMongo #extensión para conectar Flask con MongoDB.
from flask_mail import Mail


mongo = PyMongo()
mail =  Mail()

def create_app():
    app = Flask(__name__)  
    app.config.from_pyfile('../config.py') #Lee la configuracion desde config
    #Este método nos permite vincular la app
    mongo.init_app(app) #Inicia MongoDB
    mail.init_app(app)

    from .route import main
    app.register_blueprint(main) # dividir rutas em varios archivos

    return app
