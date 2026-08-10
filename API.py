import requests
from Clima import Clima

class API:
    """
    Clase API que se encarga de toda la comunicacion con Open-Meteo: verifica
    la conexion y consulta el clima actual. Las respuestas de la API (listas y
    diccionarios) se transforman siempre en objetos propios del sistema antes
    de devolverlas.

    Atributos:
        urlBase (str): URL del servicio de pronostico de Open-Meteo.
        conectado (bool): Indica si la ultima verificacion de conexion fue exitosa.
    """

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
        """
        Consulta el clima actual de una coordenada en Open-Meteo y devuelve un
        objeto Clima con los datos. La respuesta de la API (un diccionario) se
        transforma en el objeto; no se guarda como diccionario.

        Args:
            latitud (float): Latitud de la localidad.
            longitud (float): Longitud de la localidad.

        Returns:
            Clima: Objeto con los datos del clima, o None si falla la consulta.
        """
        parametros = {
            "latitude": latitud,
            "longitude": longitud,
            "current": "temperature_2m,relative_humidity_2m,wind_speed_10m,weather_code"
        }
        try:
            response = requests.get(self.urlBase, params=parametros, timeout=5)
            if response.status_code != 200:
                return None
            datos = response.json()
            actual = datos["current"]
            clima = Clima(actual["temperature_2m"], actual["relative_humidity_2m"], actual["wind_speed_10m"], actual["weather_code"])
            self.conectado = True
            return clima
        except:
            return None