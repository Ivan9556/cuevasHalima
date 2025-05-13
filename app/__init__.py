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
from config import Config
import os

mongo = PyMongo()
mail = Mail()

def create_app():
    app = Flask(__name__)  # Crea la app Flask

    # Cargar la clase config desde el archivo de configuración (Config.py) (solo utiliza variables de entorno tras la clase)
    app.config.from_object(Config) 


    mongo.init_app(app)  # Inicializa MongoDB
    mail.init_app(app)  # Inicializa Mail

    # Rutas
    from .route import main
    app.register_blueprint(main)

    return app


