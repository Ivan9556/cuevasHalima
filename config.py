#Configuracion de la app
import os
from dotenv import load_dotenv

#Carga automatica de las variables del archivo.env
#IMPORTANTE de define una clase porque el metodo app.config.from_pyfile('../config.py')
#Solo se le puede pasar variables de texto plano, no metodos get del archivo .env
load_dotenv()

class Config:
    MONGO_URI = os.getenv("MONGO_URI")
    SECRET_KEY = os.getenv("SECRET_KEY")
    MAIL_SERVER = os.getenv("MAIL_SERVER")
    MAIL_PORT = int(os.getenv("MAIL_PORT"))
    MAIL_USE_TLS = os.getenv("MAIL_USE_TLS") == "True"
    MAIL_USE_SSL = os.getenv("MAIL_USE_SSL") == "True"
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = os.getenv("MAIL_DEFAULT_SENDER")
    STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY")



