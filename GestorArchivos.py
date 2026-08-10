import json
import os
from Municipio import Municipio
from Localidad import Localidad

class GestorArchivos:
    """
    Clase GestorArchivos que se encarga de leer el archivo zonas_caracas.json y
    transformar su contenido en una lista de objetos Municipio, cada uno con su
    lista de objetos Localidad.

    Atributos:
        rutaZonas (str): Ruta del archivo de zonas de Caracas.
    """

    def __init__(self):
        """
        Inicializa una instancia de la clase GestorArchivos con la ruta por
        defecto. La ruta se arma a partir de la carpeta donde esta el programa,
        para que funcione aunque se ejecute desde otro directorio.
        """
        carpeta = os.path.dirname(os.path.abspath(__file__))
        self.rutaZonas = os.path.join(carpeta, "zonas_caracas.json")
        self.ultimoError = ""

    def leerZonas(self):
        """
        Lee el archivo zonas_caracas.json y construye la lista de municipios con
        sus localidades. En el archivo el municipio El Hatillo viene con guion
        bajo (El_Hatillo), por lo que se normaliza a "El Hatillo". Si el archivo
        no existe o esta danado, se guarda el motivo en ultimoError y se devuelve
        una lista vacia, sin detener el programa.

        Returns:
            list: Lista de objetos Municipio. Lista vacia si hubo algun problema.
        """
        self.ultimoError = ""

        if not os.path.exists(self.rutaZonas):
            self.ultimoError = "No se encontro el archivo zonas_caracas.json en la carpeta del programa."
            return []

        try:
            archivo = open(self.rutaZonas, "r", encoding="utf-8")
            data = json.load(archivo)
            archivo.close()
        except json.JSONDecodeError:
            self.ultimoError = "El archivo zonas_caracas.json no tiene un formato JSON valido."
            return []
        except:
            self.ultimoError = "No se pudo leer el archivo zonas_caracas.json."
            return []

        municipios = []
        for nombreMunicipio in data:
            # El archivo trae "El_Hatillo"; se muestra como "El Hatillo"
            nombre = nombreMunicipio.replace("_", " ")
            municipio = Municipio(nombre)
            for datosLocalidad in data[nombreMunicipio]:
                # Se ignoran los registros incompletos en lugar de romper la carga
                if "localidad" not in datosLocalidad:
                    continue
                latitud = datosLocalidad.get("latitud")
                longitud = datosLocalidad.get("longitud")
                localidad = Localidad(datosLocalidad["localidad"], latitud, longitud)
                municipio.agregarLocalidad(localidad)
            municipios.append(municipio)

        if len(municipios) == 0:
            self.ultimoError = "El archivo zonas_caracas.json no contiene municipios."
        return municipios