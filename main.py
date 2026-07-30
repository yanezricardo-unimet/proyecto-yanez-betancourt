from App import App
from API import API

def main():
    """
    Funcion principal que crea la aplicacion y la pone a correr.
    """
    app = App()
    app.menu()

# main()


api = API()
print("antes:", api.hayConexion())      # False
print("conectar():", api.conectar())    # True si hay internet
print("despues:", api.hayConexion())