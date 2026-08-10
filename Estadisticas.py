from Calculo import Calculo

class Estadisticas:
    """
    Clase Estadisticas que lleva el registro de las consultas de clima hechas
    durante la sesion activa y calcula sobre ellas el ranking de temperaturas
    y el promedio general. Tambien arma el reporte de cobertura geografica a
    partir de los municipios cargados del archivo.

    Atributos:
        consultas (list): Lista de objetos Consulta hechas en la sesion.
        calculo (Calculo): Objeto de apoyo para los calculos numericos.
    """

    def __init__(self):
        """
        Inicializa una instancia de la clase Estadisticas sin consultas.
        """
        self.consultas = []
        self.calculo = Calculo()

    def registrar(self, consulta):
        """
        Guarda una consulta de clima en el historial de la sesion.

        Args:
            consulta (Consulta): Consulta realizada por el usuario.
        """
        self.consultas.append(consulta)

    def cantidadConsultas(self):
        """
        Indica cuantas consultas de clima se han hecho en la sesion.

        Returns:
            int: Cantidad de consultas registradas.
        """
        return len(self.consultas)

    def consultaMasCalida(self):
        """
        Busca la consulta con la temperatura mas alta de la sesion.

        Returns:
            Consulta: Consulta mas calida, o None si no hay consultas.
        """
        if len(self.consultas) == 0:
            return None
        masCalida = self.consultas[0]
        for consulta in self.consultas:
            if consulta.clima.temperatura > masCalida.clima.temperatura:
                masCalida = consulta
        return masCalida

    def consultaMasFria(self):
        """
        Busca la consulta con la temperatura mas baja de la sesion.

        Returns:
            Consulta: Consulta mas fria, o None si no hay consultas.
        """
        if len(self.consultas) == 0:
            return None
        masFria = self.consultas[0]
        for consulta in self.consultas:
            if consulta.clima.temperatura < masFria.clima.temperatura:
                masFria = consulta
        return masFria

    def promedioTemperatura(self):
        """
        Calcula el promedio de temperatura de todas las localidades
        consultadas durante la sesion.

        Returns:
            float: Temperatura promedio en grados Celsius, o None si no hay consultas.
        """
        valores = []
        for consulta in self.consultas:
            valores.append(consulta.clima.temperatura)
        return self.calculo.promedio(valores)

    def consultasOrdenadasPorTemperatura(self):
        """
        Devuelve las consultas de la sesion ordenadas de la mas calida a la
        mas fria, usando un ordenamiento por seleccion sobre una copia de la
        lista para no alterar el orden original.

        Returns:
            list: Lista de objetos Consulta ordenada de mayor a menor temperatura.
        """
        ordenadas = []
        for consulta in self.consultas:
            ordenadas.append(consulta)

        for i in range(len(ordenadas)):
            mayor = i
            for j in range(i + 1, len(ordenadas)):
                if ordenadas[j].clima.temperatura > ordenadas[mayor].clima.temperatura:
                    mayor = j
            auxiliar = ordenadas[i]
            ordenadas[i] = ordenadas[mayor]
            ordenadas[mayor] = auxiliar
        return ordenadas

    def mostrarRankingTemperatura(self):
        """
        Muestra en pantalla el ranking de temperatura de la sesion, indicando
        el municipio con la localidad mas calida y el de la mas fria.
        """
        print("\n==========================================")
        print("         RANKING DE TEMPERATURA")
        print("==========================================")
        if len(self.consultas) == 0:
            print("Aun no se han realizado consultas de clima en esta sesion.")
            print("Use las opciones 1 o 2 del menu para consultar el clima de una localidad.")
            return

        masCalida = self.consultaMasCalida()
        masFria = self.consultaMasFria()

        print("\nLocalidad mas calida:")
        print("  Municipio: " + masCalida.municipio.nombre)
        print("  Localidad: " + masCalida.localidad.nombre)
        print("  Temperatura: " + str(masCalida.clima.temperatura) + " C")

        print("\nLocalidad mas fria:")
        print("  Municipio: " + masFria.municipio.nombre)
        print("  Localidad: " + masFria.localidad.nombre)
        print("  Temperatura: " + str(masFria.clima.temperatura) + " C")

        print("\n--- Detalle de las consultas de la sesion ---")
        ordenadas = self.consultasOrdenadasPorTemperatura()
        for i in range(len(ordenadas)):
            print(str(i + 1) + ". " + ordenadas[i].mostrar())

    def mostrarPromedioGeneral(self):
        """
        Muestra en pantalla el promedio de temperatura de las localidades
        consultadas durante la sesion activa.
        """
        print("\n==========================================")
        print("       PROMEDIO GENERAL DE LA SESION")
        print("==========================================")
        if len(self.consultas) == 0:
            print("Aun no se han realizado consultas de clima en esta sesion.")
            return

        print("Consultas realizadas: " + str(self.cantidadConsultas()))
        print("Temperatura promedio: " + self.calculo.formatear(self.promedioTemperatura(), 2) + " C")

    def mostrarCoberturaGeografica(self, municipios):
        """
        Muestra en pantalla el listado de localidades que no tienen coordenadas
        registradas en el archivo, agrupadas por municipio.

        Args:
            municipios (list): Lista de objetos Municipio cargados del archivo.
        """
        print("\n==========================================")
        print("          COBERTURA GEOGRAFICA")
        print("==========================================")
        print("Localidades sin coordenadas registradas (null) por municipio:")

        totalSinCoordenadas = 0
        totalLocalidades = 0
        for municipio in municipios:
            totalLocalidades = totalLocalidades + municipio.contarLocalidades()
            sinCoordenadas = municipio.localidadesSinCoordenadas()
            totalSinCoordenadas = totalSinCoordenadas + len(sinCoordenadas)

            print("\nMunicipio: " + municipio.nombre)
            print("  Sin coordenadas: " + str(len(sinCoordenadas)) + " de " + str(municipio.contarLocalidades()))
            if len(sinCoordenadas) == 0:
                print("  Todas las localidades de este municipio tienen coordenadas.")
            else:
                for i in range(len(sinCoordenadas)):
                    print("  " + str(i + 1) + ". " + sinCoordenadas[i].nombre)

        print("\n------------------------------------------")
        print("Total de localidades sin coordenadas: " + str(totalSinCoordenadas) + " de " + str(totalLocalidades))
        if totalLocalidades > 0:
            porcentaje = (totalSinCoordenadas / totalLocalidades) * 100
            print("Porcentaje sin cobertura: " + self.calculo.formatear(porcentaje, 2) + "%")
