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
        Inicializa una instancia de la clase GestorArchivos con la ruta por defecto.
        """
        self.rutaZonas = "zonas_caracas.json"

    def leerZonas(self):
        """
        Lee el archivo zonas_caracas.json y construye la lista de municipios con
        sus localidades. En el archivo el municipio El Hatillo viene con guion
        bajo (El_Hatillo), por lo que se normaliza a "El Hatillo".

        Returns:
            list: Lista de objetos Municipio. Lista vacia si no existe el archivo.
        """
        if not os.path.exists(self.rutaZonas):
            return []

        archivo = open(self.rutaZonas, "r", encoding="utf-8")
        data = json.load(archivo)
        archivo.close()

        municipios = []
        for nombreMunicipio in data:
            # El archivo trae "El_Hatillo"; se muestra como "El Hatillo"
            nombre = nombreMunicipio.replace("_", " ")
            municipio = Municipio(nombre)
            for dict in data[nombreMunicipio]:
                localidad = Localidad(dict["localidad"], dict["latitud"], dict["longitud"])
                municipio.agregarLocalidad(localidad)
            municipios.append(municipio)
        return municipios