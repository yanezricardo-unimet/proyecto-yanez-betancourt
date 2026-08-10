class Clima:
    """
    Clase Clima que guarda los datos meteorologicos actuales de una localidad
    obtenidos de la API de Open-Meteo, ya transformados en objeto.

    Atributos:
        temperatura (float): Temperatura actual en grados Celsius.
        humedad (float): Humedad relativa en porcentaje.
        viento (float): Velocidad del viento en km/h.
        codigoTiempo (int): Codigo WMO del estado del tiempo.
        estado (str): Descripcion en texto del estado del tiempo.
    """

    def __init__(self, temperatura, humedad, viento, codigoTiempo):
        """
        Inicializa una instancia de la clase Clima y traduce el codigo del
        estado del tiempo a su descripcion en texto.

        Args:
            temperatura (float): Temperatura actual en grados Celsius.
            humedad (float): Humedad relativa en porcentaje.
            viento (float): Velocidad del viento en km/h.
            codigoTiempo (int): Codigo WMO del estado del tiempo.
        """
        self.temperatura = temperatura
        self.humedad = humedad
        self.viento = viento
        self.codigoTiempo = codigoTiempo
        self.estado = self.traducirCodigo(codigoTiempo)

    def traducirCodigo(self, codigo):
        """
        Traduce un codigo WMO de Open-Meteo a una descripcion en texto. Esta
        tabla es una constante propia del programa (no es informacion de la API).

        Args:
            codigo (int): Codigo WMO del estado del tiempo.

        Returns:
            str: Descripcion del estado del tiempo, o "Desconocido" si no aplica.
        """
        codigos = {
            0: "Despejado",
            1: "Mayormente despejado",
            2: "Parcialmente nublado",
            3: "Nublado",
            45: "Niebla",
            48: "Niebla con escarcha",
            51: "Llovizna ligera",
            53: "Llovizna moderada",
            55: "Llovizna densa",
            56: "Llovizna helada ligera",
            57: "Llovizna helada densa",
            61: "Lluvia ligera",
            63: "Lluvia moderada",
            65: "Lluvia fuerte",
            66: "Lluvia helada ligera",
            67: "Lluvia helada fuerte",
            71: "Nieve ligera",
            73: "Nieve moderada",
            75: "Nieve fuerte",
            77: "Granos de nieve",
            80: "Chubascos ligeros",
            81: "Chubascos moderados",
            82: "Chubascos violentos",
            85: "Chubascos de nieve ligeros",
            86: "Chubascos de nieve fuertes",
            95: "Tormenta",
            96: "Tormenta con granizo ligero",
            99: "Tormenta con granizo fuerte"
        }
        if codigo in codigos:
            return codigos[codigo]
        return "Desconocido"

    