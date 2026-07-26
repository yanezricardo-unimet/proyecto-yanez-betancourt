from Municipio import Municipio

class App:
    def __init__(self):
        self.municipios = []

    def consultarPorMunicipio(self):
        pass

    def buscarPorNombre(self):
        pass

    def mostrarReporteCarga(self):
        pass

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

        
