#Inicio Flask y MongoDB
from flask import Flask
from flask_pymongo import PyMongo #extensión para conectar Flask con MongoDB.

mongo = PyMongo()

def create_app():
    app = Flask(__name__)  
    app.config.from_pyfile('../config.py') #Lee la configuracion desde config
    #Este método nos permite vincular la app
    mongo.init_app(app) #Inicia MongoDB

    from .route import main
    app.register_blueprint(main) # dividir rutas em varios archivos

    return app
