class RegistroDiario:
    """
    Clase RegistroDiario que representa los datos meteorologicos de un solo
    dia devueltos por la API historica de Open-Meteo. Cada valor puede venir
    en None cuando la API no tiene el dato de ese dia.

    Atributos:
        fecha (str): Fecha del registro en formato AAAA-MM-DD.
        anio (int): Anio extraido de la fecha.
        mes (int): Mes extraido de la fecha (1 a 12).
        temperatura (float): Temperatura media del dia en grados Celsius.
        humedad (float): Humedad relativa media del dia en porcentaje.
        precipitacion (float): Precipitacion acumulada del dia en mm.
        viento (float): Velocidad maxima del viento del dia en km/h.
    """

    def __init__(self, fecha, temperatura, humedad, precipitacion, viento):
        """
        Inicializa una instancia de la clase RegistroDiario y separa el anio
        y el mes a partir de la fecha.

        Args:
            fecha (str): Fecha del registro en formato AAAA-MM-DD.
            temperatura (float): Temperatura media del dia (puede ser None).
            humedad (float): Humedad relativa media del dia (puede ser None).
            precipitacion (float): Precipitacion acumulada del dia (puede ser None).
            viento (float): Velocidad maxima del viento del dia (puede ser None).
        """
        self.fecha = fecha
        self.anio = int(fecha[0:4])
        self.mes = int(fecha[5:7])
        self.temperatura = temperatura
        self.humedad = humedad
        self.precipitacion = precipitacion
        self.viento = viento
