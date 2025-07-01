#Inicio de la app
from app import create_app

app = create_app() #funcion que configura y devuelve la app Flask def en "__init__"

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000, debug=True) #activamos el modo desarrollador 
    