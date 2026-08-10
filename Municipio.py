class Municipio:
    """
    Clase Municipio que agrupa las localidades de uno de los municipios del
    Area Metropolitana de Caracas (Chacao, Baruta, El Hatillo, Sucre, Libertador).

    Atributos:
        nombre (str): Nombre del municipio.
        localidades (list): Lista de objetos Localidad del municipio.
    """
    def __init__(self, nombre):
        """
        Inicializa una instancia de la clase Municipio sin localidades.

        Args:
            nombre (str): Nombre del municipio.
        """
        self.nombre = nombre
        self.localidades = []

    def agregarLocalidad(self, localidad):
        """
        Agrega una localidad a la lista del municipio.

        Args:
            localidad (Localidad): Localidad a agregar.
        """
        self.localidades.append(localidad)

    def contarLocalidades(self):
        """
        Cuenta cuantas localidades tiene cargadas el municipio.

        Returns:
            int: Cantidad total de localidades.
        """
        return len(self.localidades)

    def contarConCoordenadas(self):
        """
        Cuenta las localidades que tienen coordenadas conocidas.

        Returns:
            int: Cantidad de localidades con coordenadas.
        """
        contador = 0
        for localidad in self.localidades:
            if localidad.tieneCoordenadas():
                contador = contador + 1
        return contador

    def contarSinCoordenadas(self):
        """
        Cuenta las localidades que no tienen coordenadas conocidas.

        Returns:
            int: Cantidad de localidades sin coordenadas.
        """
        return self.contarLocalidades() - self.contarConCoordenadas()

    def porcentajeConCoordenadas(self):
        """
        Calcula el porcentaje de localidades con coordenadas conocidas.

        Returns:
            float: Porcentaje (0.0 a 100.0). Devuelve 0.0 si no hay localidades.
        """
        total = self.contarLocalidades()
        if total == 0:
            return 0.0
        return (self.contarConCoordenadas() / total) * 100

    def localidadesConCoordenadas(self):
        """
        Arma la lista de las localidades del municipio que si tienen
        coordenadas, que son las unicas que se pueden consultar en la API.

        Returns:
            list: Lista de objetos Localidad con coordenadas conocidas.
        """
        disponibles = []
        for localidad in self.localidades:
            if localidad.tieneCoordenadas():
                disponibles.append(localidad)
        return disponibles

    def localidadesSinCoordenadas(self):
        """
        Arma la lista de las localidades del municipio que no tienen
        coordenadas registradas, para el reporte de cobertura geografica.

        Returns:
            list: Lista de objetos Localidad sin coordenadas conocidas.
        """
        faltantes = []
        for localidad in self.localidades:
            if not localidad.tieneCoordenadas():
                faltantes.append(localidad)
        return faltantes

    def buscarPorNombre(self, texto):
        """
        Busca las localidades del municipio cuyo nombre contenga el texto
        indicado, sin distinguir entre mayusculas y minusculas.

        Args:
            texto (str): Nombre o parte del nombre a buscar.

        Returns:
            list: Lista de objetos Localidad que coinciden con la busqueda.
        """
        coincidencias = []
        texto = texto.lower()
        for localidad in self.localidades:
            if texto in localidad.nombre.lower():
                coincidencias.append(localidad)
        return coincidencias