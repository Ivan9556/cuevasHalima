#Inicio de la app
from app import create_app

app = create_app() #funcion que configura y devuelve la app Flask def en "__init__"

if __name__ == '__main__':
    app.run(debug=True) #activamos el modo desarrollador 
    