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
        """
        Intenta conectarse a Open-Meteo para verificar si hay internet. Si falla,
        deja conectado en False sin detener el programa.

        Returns:
            bool: True si se logro conectar.
        """
        try:
            response = requests.get(self.urlBase, timeout=5)
            # Open-Meteo responde 400 si faltan parametros; con eso ya sabemos que hay red
            if response.status_code == 200 or response.status_code == 400:
                self.conectado = True
            else:
                self.conectado = False
        except:
            # Si no hay internet o el servicio no responde, seguimos sin conexion
            self.conectado = False
        return self.conectado

    def hayConexion(self):
        """
        Indica si la API esta conectada.

        Returns:
            bool: Estado de la conexion.
        """
        return self.conectado

    def consultarClimaActual(self, latitud, longitud):
        pass