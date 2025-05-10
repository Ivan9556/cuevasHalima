#Configuracion de la app
import os
from dotenv import load_dotenv

#Carga automatica de las variables del archivo.env
load_dotenv()

#URL de MongoDB
MONGO_URI = os.getenv("MONGO_URI")
SECRET_KEY = os.getenv("SECRET_KEY")

#Protocolo SMTP
MAIL_SERVER = os.getenv("MAIL_SERVER")
MAIL_PORT = int(os.getenv("MAIL_PORT"))
MAIL_USE_TLS = os.getenv("MAIL_USE_TLS")
MAIL_USERNAME = os.getenv("MAIL_USERNAME")
MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
MAIL_DEFAULT_SENDER = os.getenv("MAIL_DEFAULT_SENDER")

