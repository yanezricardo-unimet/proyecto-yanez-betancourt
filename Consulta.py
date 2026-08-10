from datetime import datetime

class Consulta:
    """
    Clase Consulta que guarda el resultado de una consulta de clima hecha
    durante la sesion activa. Sirve para armar despues el ranking de
    temperaturas y el promedio general.

    Atributos:
        municipio (Municipio): Municipio de la localidad consultada.
        localidad (Localidad): Localidad consultada.
        clima (Clima): Datos del clima obtenidos en esa consulta.
        hora (str): Hora en que se realizo la consulta (HH:MM:SS).
    """

    def __init__(self, municipio, localidad, clima):
        """
        Inicializa una instancia de la clase Consulta y le coloca la hora
        en que fue realizada.

        Args:
            municipio (Municipio): Municipio de la localidad consultada.
            localidad (Localidad): Localidad consultada.
            clima (Clima): Datos del clima obtenidos de la API.
        """
        self.municipio = municipio
        self.localidad = localidad
        self.clima = clima
        self.hora = datetime.now().strftime("%H:%M:%S")

    def mostrar(self):
        """
        Devuelve un texto de una linea con el resumen de la consulta, para
        usarlo en los listados de estadisticas.

        Returns:
            str: Resumen con localidad, municipio, temperatura y hora.
        """
        return (self.localidad.nombre + " (" + self.municipio.nombre + ") - " +
                str(self.clima.temperatura) + " C - " + self.clima.estado +
                " - consultado a las " + self.hora)
