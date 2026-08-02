class Localidad:
    """
    Clase Localidad que representa una localidad de un municipio de Caracas,
    con su nombre y sus coordenadas geograficas. Muchas localidades no tienen
    coordenadas conocidas, por lo que latitud y longitud pueden ser None.

    Atributos:
        nombre (str): Nombre de la localidad.
        latitud (float): Latitud de la localidad (None si no se conoce).
        longitud (float): Longitud de la localidad (None si no se conoce).
    """

    def __init__(self, nombre, latitud, longitud):
        """
        Inicializa una instancia de la clase Localidad.

        Args:
            nombre (str): Nombre de la localidad.
            latitud (float): Latitud de la localidad (puede ser None).
            longitud (float): Longitud de la localidad (puede ser None).
        """
        self.nombre = nombre
        self.latitud = latitud
        self.longitud = longitud

    def tieneCoordenadas(self):
        """
        Indica si la localidad tiene coordenadas geograficas conocidas.

        Returns:
            bool: True si latitud y longitud no son None.
        """
        return self.latitud != None and self.longitud != None

    def mostrar(self):
        """
        Devuelve un texto corto con el nombre de la localidad.

        Returns:
            str: Nombre de la localidad.
        """
        return self.nombre
