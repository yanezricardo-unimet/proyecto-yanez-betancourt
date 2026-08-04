from Municipio import Municipio
from GestorArchivos import GestorArchivos
from API import API

class App:
    def __init__(self):
        """
        Inicializa una instancia de la clase App con los atributos en vacio.
        """
        self.gestorArchivos = GestorArchivos()
        self.municipios = []
        self.api = API()

    def consultarPorMunicipio(self):
        """
        Muestra la lista de municipios, permite elegir uno, luego muestra sus
        localidades con coordenadas validas y consulta el clima de la elegida.
        """
        print("\n--- Municipios ---")
        for i in range(len(self.municipios)):
            print(str(i + 1) + ". " + self.municipios[i].nombre)

        municipio = self.pedirSeleccion(self.municipios, "\nSeleccione un municipio (0 para volver): ")
        if municipio == None:
            return

        disponibles = municipio.localidadesConCoordenadas()
        if len(disponibles) == 0:
            print("\nEse municipio no tiene localidades con coordenadas para consultar.")
            return

        print("\n--- Localidades de " + municipio.nombre + " (con coordenadas) ---")
        for i in range(len(disponibles)):
            print(str(i + 1) + ". " + disponibles[i].nombre)

        localidad = self.pedirSeleccion(disponibles, "\nSeleccione una localidad (0 para volver): ")
        if localidad == None:
            return

        self.consultarClima(municipio, localidad)

    def buscarPorNombre(self):
        pass

    def mostrarReporteCarga(self):
        pass

    def cargarDatos(self):
        """
        Carga las zonas de Caracas desde el archivo hacia la lista de municipios
        y revisa si hay conexion con Open-Meteo para avisar al usuario.
        """
        print("Cargando zonas de Caracas...")
        self.municipios = self.gestorArchivos.leerZonas()
        if len(self.municipios) == 0:
            print("No se pudo cargar el archivo de zonas. Verifique que exista zonas_caracas.json.")
            return

        print("Zonas cargadas correctamente.")
        if self.api.conectar():
            print("Conexion con Open-Meteo disponible.")
        else:
            print("Sin conexion con Open-Meteo. Podra ver los datos cargados, pero no consultar el clima hasta tener internet.")

    def menu(self):
        while True:
            print("\n==========================================")
            print("               METEOCARACAS")
            print("==========================================")
            print("1. Consultar clima por municipio y localidad")
            print("2. Buscar localidad por nombre")
            print("3. Ver reporte de carga")
            print("4. Salir")
    
            opcion = input("\nIngrese una opcion: ")
            while (not opcion.isnumeric()) or (int(opcion) not in range(1,5)):
                opcion = input("\nOpcion invalida. Intente de nuevo.\nIngrese una opcion: ")
    
            if opcion == "1":
                self.consultarPorMunicipio()
            elif opcion == "2":
                self.buscarPorNombre()
            elif opcion == "3":
                self.mostrarReporteCarga()
            else:
                print("\nGracias por usar MeteoCaracas. Hasta luego.")
                break

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

    def cargarDatos(self):
        """
        Carga las zonas de Caracas desde el archivo hacia la lista de municipios
        y revisa si hay conexion con Open-Meteo para avisar al usuario.
        """
        print("Cargando zonas de Caracas...")
        self.municipios = self.gestorArchivos.leerZonas()
        if len(self.municipios) == 0:
            print("No se pudo cargar el archivo de zonas. Verifique que exista zonas_caracas.json.")
            return

        print("Zonas cargadas correctamente.")
        if self.api.conectar():
            print("Conexion con Open-Meteo disponible.")
        else:
            print("Sin conexion con Open-Meteo. Podra ver los datos cargados, pero no consultar el clima hasta tener internet.")

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
        
