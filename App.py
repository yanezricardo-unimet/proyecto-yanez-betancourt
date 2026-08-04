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
        pass

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

    def iniciar(self):
        pass
        
