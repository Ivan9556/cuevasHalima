#Inicio Flask y MongoDB
from flask import Flask
from flask_pymongo import PyMongo #extensión para conectar Flask con MongoDB.

mongo = PyMongo()

def create_app():
    app = Flask(__name__)  
    app.config.from_pyfile('../config.py') #Lee la configuracion desde config

    mongo.__init__app(app) #Inicia MongoDB

    from .rutas import main
    app.register_blueprint(main) # dividir rutas em varios archivos

    return app
