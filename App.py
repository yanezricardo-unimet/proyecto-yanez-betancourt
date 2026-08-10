from datetime import datetime, timedelta

from GestorArchivos import GestorArchivos
from API import API
from Consulta import Consulta
from Estadisticas import Estadisticas
from Historico import Historico

class App:
    """
    Clase App que controla toda la aplicacion MeteoCaracas: carga los datos del
    archivo, muestra los menus, consulta el clima en tiempo real, lleva las
    estadisticas de la sesion y arma los reportes historicos.

    Atributos:
        gestorArchivos (GestorArchivos): Objeto que lee el archivo de zonas.
        municipios (list): Lista de objetos Municipio cargados del archivo.
        api (API): Objeto que se comunica con Open-Meteo.
        estadisticas (Estadisticas): Objeto que guarda las consultas de la sesion.
    """

    def __init__(self):
        """
        Inicializa una instancia de la clase App con los atributos en vacio.
        """
        self.gestorArchivos = GestorArchivos()
        self.municipios = []
        self.api = API()
        self.estadisticas = Estadisticas()

    # ------------------------------------------------------------------
    # Entradas del usuario
    # ------------------------------------------------------------------

    def pedirIndice(self, cantidad, mensaje):
        """
        Pide al usuario que escoja un numero de una lista y no lo deja avanzar
        hasta que escriba un valor valido. El 0 se usa para volver atras.

        Args:
            cantidad (int): Cantidad de opciones disponibles.
            mensaje (str): Texto que se le muestra al usuario.

        Returns:
            int: Indice seleccionado empezando en 0, o -1 si el usuario decide volver.
        """
        while True:
            entrada = input(mensaje).strip()
            if not entrada.isnumeric():
                print("Entrada invalida. Escriba un numero entre 0 y " + str(cantidad) + ".")
                continue
            numero = int(entrada)
            if numero == 0:
                return -1
            if numero >= 1 and numero <= cantidad:
                return numero - 1
            print("Opcion fuera de rango. Escriba un numero entre 0 y " + str(cantidad) + ".")

    def pedirSeleccion(self, lista, mensaje):
        """
        Pide al usuario que escoja un elemento de una lista de objetos.

        Args:
            lista (list): Lista de objetos entre los que se puede escoger.
            mensaje (str): Texto que se le muestra al usuario.

        Returns:
            object: Objeto seleccionado, o None si el usuario decide volver.
        """
        indice = self.pedirIndice(len(lista), mensaje)
        if indice == -1:
            return None
        return lista[indice]

    def pedirFecha(self, mensaje):
        """
        Pide al usuario una fecha en formato AAAA-MM-DD y valida que exista de
        verdad. El 0 se usa para cancelar la operacion.

        Args:
            mensaje (str): Texto que se le muestra al usuario.

        Returns:
            datetime: Fecha ingresada, o None si el usuario cancela.
        """
        while True:
            entrada = input(mensaje).strip()
            if entrada == "0":
                return None
            try:
                return datetime.strptime(entrada, "%Y-%m-%d")
            except ValueError:
                print("Fecha invalida. Use el formato AAAA-MM-DD (ejemplo: 2020-01-31).")

    def confirmar(self, mensaje):
        """
        Le hace al usuario una pregunta de si o no y valida la respuesta.

        Args:
            mensaje (str): Pregunta que se le muestra al usuario.

        Returns:
            bool: True si el usuario responde que si.
        """
        while True:
            respuesta = input(mensaje).strip().lower()
            if respuesta == "s" or respuesta == "si":
                return True
            if respuesta == "n" or respuesta == "no":
                return False
            print("Respuesta invalida. Escriba S para si o N para no.")

    # ------------------------------------------------------------------
    # Seleccion de municipios y localidades
    # ------------------------------------------------------------------

    def seleccionarMunicipio(self):
        """
        Muestra la lista de municipios cargados y permite escoger uno.

        Returns:
            Municipio: Municipio seleccionado, o None si el usuario decide volver.
        """
        print("\n--- Municipios ---")
        for i in range(len(self.municipios)):
            print(str(i + 1) + ". " + self.municipios[i].nombre)
        return self.pedirSeleccion(self.municipios, "\nSeleccione un municipio (0 para volver): ")

    def seleccionarLocalidadConCoordenadas(self, municipio):
        """
        Muestra las localidades de un municipio que tienen coordenadas validas
        y permite escoger una.

        Args:
            municipio (Municipio): Municipio del que se listan las localidades.

        Returns:
            Localidad: Localidad seleccionada, o None si no hay o el usuario vuelve.
        """
        disponibles = municipio.localidadesConCoordenadas()
        if len(disponibles) == 0:
            print("\nEse municipio no tiene localidades con coordenadas para consultar.")
            return None

        print("\n--- Localidades de " + municipio.nombre + " (con coordenadas) ---")
        for i in range(len(disponibles)):
            print(str(i + 1) + ". " + disponibles[i].nombre)

        return self.pedirSeleccion(disponibles, "\nSeleccione una localidad (0 para volver): ")

    # ------------------------------------------------------------------
    # Consulta del clima en tiempo real
    # ------------------------------------------------------------------

    def consultarPorMunicipio(self):
        """
        Muestra la lista de municipios, permite elegir uno, luego muestra sus
        localidades con coordenadas validas y consulta el clima de la elegida.
        """
        municipio = self.seleccionarMunicipio()
        if municipio == None:
            return

        localidad = self.seleccionarLocalidadConCoordenadas(municipio)
        if localidad == None:
            return

        self.consultarClima(municipio, localidad)

    def buscarPorNombre(self):
        """
        Pide un texto al usuario y busca localidades cuyo nombre coincida en
        todos los municipios. Solo permite consultar las que tienen coordenadas.
        """
        texto = input("\nIngrese el nombre (o parte) de la localidad: ")
        if texto.strip() == "":
            print("\nDebe ingresar un texto para buscar.")
            return

        resultados = []
        municipiosResultado = []
        for municipio in self.municipios:
            for localidad in municipio.buscarPorNombre(texto):
                resultados.append(localidad)
                municipiosResultado.append(municipio)

        if len(resultados) == 0:
            print("\nNo se encontraron localidades con ese nombre.")
            return

        print("\n--- Resultados ---")
        for i in range(len(resultados)):
            aviso = ""
            if not resultados[i].tieneCoordenadas():
                aviso = " (sin coordenadas)"
            print(str(i + 1) + ". " + resultados[i].nombre + " - " + municipiosResultado[i].nombre + aviso)

        indice = self.pedirIndice(len(resultados), "\nSeleccione una localidad (0 para volver): ")
        if indice == -1:
            return

        localidad = resultados[indice]
        municipio = municipiosResultado[indice]
        if not localidad.tieneCoordenadas():
            print("\nEsa localidad no tiene coordenadas registradas, no se puede consultar su clima.")
            return

        self.consultarClima(municipio, localidad)

    def consultarClima(self, municipio, localidad):
        """
        Consulta el clima en tiempo real de una localidad, lo muestra en
        pantalla y lo registra en las estadisticas de la sesion.

        Args:
            municipio (Municipio): Municipio de la localidad.
            localidad (Localidad): Localidad a consultar (debe tener coordenadas).
        """
        print("\nConsultando el clima en tiempo real...")
        clima = self.api.consultarClimaActual(localidad.latitud, localidad.longitud)
        if clima == None:
            print("No se pudo obtener el clima. Verifique su conexion a internet e intente de nuevo.")
            return
        self.mostrarClima(municipio, localidad, clima)
        self.estadisticas.registrar(Consulta(municipio, localidad, clima))

    def mostrarClima(self, municipio, localidad, clima):
        """
        Muestra en pantalla los detalles meteorologicos de una localidad.

        Args:
            municipio (Municipio): Municipio de la localidad.
            localidad (Localidad): Localidad consultada.
            clima (Clima): Datos del clima obtenidos de la API.
        """
        print("\n==========================================")
        print("               CLIMA ACTUAL")
        print("==========================================")
        print("Municipio: " + municipio.nombre)
        print("Localidad: " + localidad.nombre)
        print("Latitud: " + str(localidad.latitud))
        print("Longitud: " + str(localidad.longitud))
        print("Temperatura: " + str(clima.temperatura) + " C")
        print("Humedad relativa: " + str(clima.humedad) + " %")
        print("Velocidad del viento: " + str(clima.viento) + " km/h")
        print("Estado del tiempo: " + clima.estado)

    # ------------------------------------------------------------------
    # Reportes y estadisticas
    # ------------------------------------------------------------------

    def mostrarReporteCarga(self):
        """
        Muestra en pantalla el reporte de la carga de datos: por cada municipio
        indica cantidad de localidades, cuantas tienen coordenadas, cuantas no,
        y el porcentaje con coordenadas.
        """
        print("\n==========================================")
        print("        REPORTE DE CARGA DE DATOS")
        print("==========================================")
        for municipio in self.municipios:
            print("\nMunicipio: " + municipio.nombre)
            print("  - Localidades cargadas: " + str(municipio.contarLocalidades()))
            print("  - Con coordenadas: " + str(municipio.contarConCoordenadas()))
            print("  - Sin coordenadas: " + str(municipio.contarSinCoordenadas()))
            print("  - Porcentaje con coordenadas: " + str(round(municipio.porcentajeConCoordenadas(), 2)) + "%")

    def menuEstadisticas(self):
        """
        Muestra el submenu del modulo de reportes y estadisticas y ejecuta la
        opcion escogida por el usuario hasta que decida volver.
        """
        while True:
            print("\n==========================================")
            print("        REPORTES Y ESTADISTICAS")
            print("==========================================")
            print("1. Ranking de temperatura de la sesion")
            print("2. Cobertura geografica (localidades sin coordenadas)")
            print("3. Promedio general de temperatura de la sesion")
            print("0. Volver al menu principal")

            opcion = input("\nIngrese una opcion: ").strip()
            if opcion == "0":
                return
            elif opcion == "1":
                self.estadisticas.mostrarRankingTemperatura()
            elif opcion == "2":
                self.estadisticas.mostrarCoberturaGeografica(self.municipios)
            elif opcion == "3":
                self.estadisticas.mostrarPromedioGeneral()
            else:
                print("\nOpcion invalida. Escriba un numero entre 0 y 3.")

    # ------------------------------------------------------------------
    # Historicos
    # ------------------------------------------------------------------

    def pedirPeriodo(self):
        """
        Pide al usuario la fecha de inicio y la fecha de fin del analisis
        historico y valida que el rango tenga sentido: que el inicio no sea
        posterior al fin, que no se pidan fechas anteriores a 1940 y que no se
        pidan fechas mas recientes de las que tiene disponible el archivo de
        Open-Meteo (que va con unos dias de retraso).

        Returns:
            tuple: Fecha de inicio y fecha de fin como objetos datetime,
                o (None, None) si el usuario cancela.
        """
        minimo = datetime(1940, 1, 1)
        limite = datetime.now() - timedelta(days=6)

        print("\nIndique el periodo a analizar en formato AAAA-MM-DD.")
        print("Fechas permitidas: desde " + minimo.strftime("%Y-%m-%d") +
              " hasta " + limite.strftime("%Y-%m-%d") + ".")
        print("Escriba 0 en cualquier momento para cancelar.")

        while True:
            fechaInicio = self.pedirFecha("\nFecha de inicio (AAAA-MM-DD): ")
            if fechaInicio == None:
                return None, None

            fechaFin = self.pedirFecha("Fecha de fin (AAAA-MM-DD): ")
            if fechaFin == None:
                return None, None

            if fechaInicio < minimo:
                print("\nLa fecha de inicio no puede ser anterior a " + minimo.strftime("%Y-%m-%d") + ".")
                continue
            if fechaFin > limite:
                print("\nEl archivo historico solo tiene datos hasta " + limite.strftime("%Y-%m-%d") + ".")
                continue
            if fechaInicio > fechaFin:
                print("\nLa fecha de inicio no puede ser posterior a la fecha de fin.")
                continue

            return fechaInicio, fechaFin

    def consultarHistorico(self):
        """
        Permite escoger una localidad con coordenadas y un periodo de tiempo,
        consulta el historico en Open-Meteo y muestra el reporte mes a mes, los
        promedios de cada magnitud, los anios destacados y, si el usuario
        quiere, el grafico comparativo.
        """
        municipio = self.seleccionarMunicipio()
        if municipio == None:
            return

        localidad = self.seleccionarLocalidadConCoordenadas(municipio)
        if localidad == None:
            return

        fechaInicio, fechaFin = self.pedirPeriodo()
        if fechaInicio == None:
            return

        textoInicio = fechaInicio.strftime("%Y-%m-%d")
        textoFin = fechaFin.strftime("%Y-%m-%d")

        print("\nConsultando el historico de " + localidad.nombre + "...")
        print("Segun el tamano del periodo esto puede tardar unos segundos.")
        registros = self.api.consultarHistorico(localidad.latitud, localidad.longitud,
                                                textoInicio, textoFin)

        if registros == None:
            print("\nNo se pudo obtener el historico. Verifique su conexion a internet e intente de nuevo.")
            return
        if len(registros) == 0:
            print("\nLa API no devolvio datos para ese periodo. Intente con otro rango de fechas.")
            return

        historico = Historico(municipio, localidad, textoInicio, textoFin, registros)
        historico.mostrarReporteMensual()
        historico.mostrarPromedios()
        historico.mostrarAniosExtremos()

        if self.confirmar("\nDesea ver el grafico comparativo? (S/N): "):
            historico.graficar()

    # ------------------------------------------------------------------
    # Carga y menu principal
    # ------------------------------------------------------------------

    def cargarDatos(self):
        """
        Carga las zonas de Caracas desde el archivo hacia la lista de municipios
        y revisa si hay conexion con Open-Meteo para avisar al usuario.
        """
        print("Cargando zonas de Caracas...")
        self.municipios = self.gestorArchivos.leerZonas()
        if len(self.municipios) == 0:
            print("No se pudo cargar el archivo de zonas.")
            print(self.gestorArchivos.ultimoError)
            return

        print("Zonas cargadas correctamente.")
        if self.api.conectar():
            print("Conexion con Open-Meteo disponible.")
        else:
            print("Sin conexion con Open-Meteo. Podra ver los datos cargados, pero no consultar el clima hasta tener internet.")

    def menu(self):
        """
        Muestra el menu principal y ejecuta la opcion escogida por el usuario
        hasta que decida salir del programa.
        """
        while True:
            print("\n==========================================")
            print("               METEOCARACAS")
            print("==========================================")
            print("1. Consultar clima por municipio y localidad")
            print("2. Buscar localidad por nombre")
            print("3. Ver reporte de carga")
            print("4. Reportes y estadisticas")
            print("5. Consultar historico por periodo")
            print("6. Salir")

            opcion = input("\nIngrese una opcion: ").strip()
            while (not opcion.isnumeric()) or (int(opcion) not in range(1, 7)):
                opcion = input("\nOpcion invalida. Escriba un numero entre 1 y 6.\nIngrese una opcion: ").strip()

            if opcion == "1":
                self.consultarPorMunicipio()
            elif opcion == "2":
                self.buscarPorNombre()
            elif opcion == "3":
                self.mostrarReporteCarga()
            elif opcion == "4":
                self.menuEstadisticas()
            elif opcion == "5":
                self.consultarHistorico()
            else:
                print("\nGracias por usar MeteoCaracas. Hasta luego.")
                break

    def iniciar(self):
        """
        Enciende la aplicacion: carga los datos, muestra el reporte de carga y
        entra al bucle principal del menu hasta que el usuario decide salir.
        """
        self.cargarDatos()
        if len(self.municipios) == 0:
            return
        self.mostrarReporteCarga()
        self.menu()
