import requests
from Clima import Clima

class API:
    def __init__(self):
        """
        Inicializa una instancia de la clase API con la URL de Open-Meteo.
        """
        self.urlBase = "https://api.open-meteo.com/v1/forecast"
        self.conectado = False

    def conectar(self):
        pass

    def hayConexion(self):
        pass

    def consultarClimaActual(self, latitud, longitud):
        pass