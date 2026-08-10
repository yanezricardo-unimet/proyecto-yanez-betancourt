import matplotlib.pyplot as plt

from Calculo import Calculo
from RegistroMensual import RegistroMensual
from RegistroAnual import RegistroAnual

class Historico:
    """
    Clase Historico que organiza los registros diarios devueltos por la API
    historica de Open-Meteo en registros mensuales y anuales, calcula los
    promedios del periodo, determina los anios extremos y genera el grafico
    comparativo de cada magnitud.

    Atributos:
        municipio (Municipio): Municipio de la localidad analizada.
        localidad (Localidad): Localidad analizada.
        fechaInicio (str): Fecha de inicio del periodo (AAAA-MM-DD).
        fechaFin (str): Fecha de fin del periodo (AAAA-MM-DD).
        registrosDiarios (list): Lista de objetos RegistroDiario del periodo.
        meses (list): Lista de objetos RegistroMensual ordenada cronologicamente.
        anios (list): Lista de objetos RegistroAnual ordenada cronologicamente.
        calculo (Calculo): Objeto de apoyo para los calculos numericos.
    """

    def __init__(self, municipio, localidad, fechaInicio, fechaFin, registrosDiarios):
        """
        Inicializa una instancia de la clase Historico y arma de una vez los
        agrupamientos por mes y por anio.

        Args:
            municipio (Municipio): Municipio de la localidad analizada.
            localidad (Localidad): Localidad analizada.
            fechaInicio (str): Fecha de inicio del periodo (AAAA-MM-DD).
            fechaFin (str): Fecha de fin del periodo (AAAA-MM-DD).
            registrosDiarios (list): Lista de objetos RegistroDiario del periodo.
        """
        self.municipio = municipio
        self.localidad = localidad
        self.fechaInicio = fechaInicio
        self.fechaFin = fechaFin
        self.registrosDiarios = registrosDiarios
        self.calculo = Calculo()
        self.meses = []
        self.anios = []
        self.agruparPorMes()
        self.agruparPorAnio()

    def agruparPorMes(self):
        """
        Recorre los registros diarios y los agrupa en objetos RegistroMensual,
        creando un mes nuevo cada vez que aparece una combinacion de anio y
        mes que todavia no existe.
        """
        for registro in self.registrosDiarios:
            mes = self.buscarMes(registro.anio, registro.mes)
            if mes == None:
                mes = RegistroMensual(registro.anio, registro.mes)
                self.meses.append(mes)
            mes.agregarDia(registro)

    def agruparPorAnio(self):
        """
        Recorre los registros mensuales ya construidos y los agrupa en objetos
        RegistroAnual.
        """
        for mes in self.meses:
            anio = self.buscarAnio(mes.anio)
            if anio == None:
                anio = RegistroAnual(mes.anio)
                self.anios.append(anio)
            anio.agregarMes(mes)

    def buscarMes(self, anio, numeroMes):
        """
        Busca el registro mensual que corresponde a un anio y mes dados.

        Args:
            anio (int): Anio buscado.
            numeroMes (int): Numero del mes buscado (1 a 12).

        Returns:
            RegistroMensual: Registro encontrado, o None si no existe todavia.
        """
        for mes in self.meses:
            if mes.anio == anio and mes.mes == numeroMes:
                return mes
        return None

    def buscarAnio(self, anio):
        """
        Busca el registro anual que corresponde a un anio dado.

        Args:
            anio (int): Anio buscado.

        Returns:
            RegistroAnual: Registro encontrado, o None si no existe todavia.
        """
        for registroAnual in self.anios:
            if registroAnual.anio == anio:
                return registroAnual
        return None

    def temperaturaPromedio(self):
        """
        Calcula la temperatura promedio de todo el periodo consultado.

        Returns:
            float: Temperatura promedio en grados Celsius, o None si no hay datos.
        """
        valores = []
        for registro in self.registrosDiarios:
            valores.append(registro.temperatura)
        return self.calculo.promedio(valores)

    def humedadPromedio(self):
        """
        Calcula la humedad relativa promedio de todo el periodo consultado.

        Returns:
            float: Humedad relativa promedio en porcentaje, o None si no hay datos.
        """
        valores = []
        for registro in self.registrosDiarios:
            valores.append(registro.humedad)
        return self.calculo.promedio(valores)

    def precipitacionTotal(self):
        """
        Suma la precipitacion de todo el periodo consultado.

        Returns:
            float: Precipitacion acumulada en mm, o None si no hay datos.
        """
        valores = []
        for registro in self.registrosDiarios:
            valores.append(registro.precipitacion)
        return self.calculo.total(valores)

    def precipitacionPromedioMensual(self):
        """
        Calcula cuanta precipitacion cae en promedio en un mes del periodo.

        Returns:
            float: Precipitacion promedio mensual en mm, o None si no hay datos.
        """
        valores = []
        for mes in self.meses:
            valores.append(mes.precipitacionAcumulada())
        return self.calculo.promedio(valores)

    def vientoPromedio(self):
        """
        Calcula la velocidad promedio del viento de todo el periodo consultado.

        Returns:
            float: Velocidad promedio del viento en km/h, o None si no hay datos.
        """
        valores = []
        for registro in self.registrosDiarios:
            valores.append(registro.viento)
        return self.calculo.promedio(valores)

    def anioExtremo(self, magnitud, buscarMayor):
        """
        Busca el anio con el valor mas alto o mas bajo de una magnitud dentro
        del periodo consultado.

        Args:
            magnitud (str): Magnitud a comparar ("temperatura", "humedad",
                "precipitacion" o "viento").
            buscarMayor (bool): True para buscar el valor mas alto, False para
                buscar el mas bajo.

        Returns:
            RegistroAnual: Anio con el valor extremo, o None si no hay datos.
        """
        extremo = None
        valorExtremo = None
        for registroAnual in self.anios:
            valor = self.valorAnual(registroAnual, magnitud)
            if valor == None:
                continue
            if valorExtremo == None:
                extremo = registroAnual
                valorExtremo = valor
            elif buscarMayor and valor > valorExtremo:
                extremo = registroAnual
                valorExtremo = valor
            elif (not buscarMayor) and valor < valorExtremo:
                extremo = registroAnual
                valorExtremo = valor
        return extremo

    def valorAnual(self, registroAnual, magnitud):
        """
        Devuelve el valor resumido de una magnitud para un anio.

        Args:
            registroAnual (RegistroAnual): Anio del que se quiere el valor.
            magnitud (str): Magnitud pedida ("temperatura", "humedad",
                "precipitacion" o "viento").

        Returns:
            float: Valor de la magnitud en ese anio, o None si no hay datos.
        """
        if magnitud == "temperatura":
            return registroAnual.temperaturaPromedio()
        elif magnitud == "humedad":
            return registroAnual.humedadPromedio()
        elif magnitud == "precipitacion":
            return registroAnual.precipitacionAcumulada()
        elif magnitud == "viento":
            return registroAnual.vientoPromedio()
        return None

    def valorMensual(self, registroMensual, magnitud):
        """
        Devuelve el valor resumido de una magnitud para un mes.

        Args:
            registroMensual (RegistroMensual): Mes del que se quiere el valor.
            magnitud (str): Magnitud pedida ("temperatura", "humedad",
                "precipitacion" o "viento").

        Returns:
            float: Valor de la magnitud en ese mes, o None si no hay datos.
        """
        if magnitud == "temperatura":
            return registroMensual.temperaturaPromedio()
        elif magnitud == "humedad":
            return registroMensual.humedadPromedio()
        elif magnitud == "precipitacion":
            return registroMensual.precipitacionAcumulada()
        elif magnitud == "viento":
            return registroMensual.vientoPromedio()
        return None

    def mostrarReporteMensual(self):
        """
        Muestra en pantalla una tabla con los valores de cada mes del periodo:
        temperatura, humedad relativa, precipitacion acumulada y viento,
        separando los meses por anio.
        """
        print("\n==========================================")
        print("        HISTORICO POR PERIODO")
        print("==========================================")
        print("Municipio: " + self.municipio.nombre)
        print("Localidad: " + self.localidad.nombre)
        print("Coordenadas: " + str(self.localidad.latitud) + ", " + str(self.localidad.longitud))
        print("Periodo: " + self.fechaInicio + " hasta " + self.fechaFin)
        print("Dias analizados: " + str(len(self.registrosDiarios)))

        for registroAnual in self.anios:
            print("\n--- Anio " + str(registroAnual.anio) + " ---")
            print("Mes".ljust(12) + "Temp (C)".rjust(10) + "Humedad (%)".rjust(14) +
                  "Precip (mm)".rjust(14) + "Viento (km/h)".rjust(16))
            print("-" * 66)
            for mes in registroAnual.meses:
                print(mes.nombreMes().ljust(12) +
                      self.calculo.formatear(mes.temperaturaPromedio()).rjust(10) +
                      self.calculo.formatear(mes.humedadPromedio()).rjust(14) +
                      self.calculo.formatear(mes.precipitacionAcumulada()).rjust(14) +
                      self.calculo.formatear(mes.vientoPromedio()).rjust(16))

    def mostrarPromedios(self):
        """
        Muestra en pantalla los valores promedio de cada magnitud para todo el
        periodo consultado.
        """
        print("\n==========================================")
        print("       PROMEDIOS DEL PERIODO")
        print("==========================================")
        print("Temperatura promedio: " + self.calculo.formatear(self.temperaturaPromedio(), 2) + " C")
        print("Humedad relativa promedio: " + self.calculo.formatear(self.humedadPromedio(), 2) + " %")
        print("Precipitacion acumulada total: " + self.calculo.formatear(self.precipitacionTotal(), 2) + " mm")
        print("Precipitacion promedio por mes: " + self.calculo.formatear(self.precipitacionPromedioMensual(), 2) + " mm")
        print("Velocidad promedio del viento: " + self.calculo.formatear(self.vientoPromedio(), 2) + " km/h")

    def mostrarAniosExtremos(self):
        """
        Muestra en pantalla el anio mas caluroso, el mas fresco, el de mayor
        precipitacion y el de mayor humedad relativa del periodo consultado.
        """
        print("\n==========================================")
        print("        ANIOS DESTACADOS DEL PERIODO")
        print("==========================================")
        if len(self.anios) == 0:
            print("No hay datos suficientes para determinar los anios destacados.")
            return
        if len(self.anios) == 1:
            print("El periodo consultado abarca un solo anio (" + str(self.anios[0].anio) + "),")
            print("por lo que ese anio es el extremo en todas las magnitudes.")

        masCaluroso = self.anioExtremo("temperatura", True)
        masFresco = self.anioExtremo("temperatura", False)
        masLluvioso = self.anioExtremo("precipitacion", True)
        masHumedo = self.anioExtremo("humedad", True)

        if masCaluroso != None:
            print("\nAnio mas caluroso: " + str(masCaluroso.anio) +
                  " (" + self.calculo.formatear(masCaluroso.temperaturaPromedio(), 2) + " C)")
        if masFresco != None:
            print("Anio mas fresco: " + str(masFresco.anio) +
                  " (" + self.calculo.formatear(masFresco.temperaturaPromedio(), 2) + " C)")
        if masLluvioso != None:
            print("Anio con mayor precipitacion: " + str(masLluvioso.anio) +
                  " (" + self.calculo.formatear(masLluvioso.precipitacionAcumulada(), 2) + " mm)")
        if masHumedo != None:
            print("Anio con mayor humedad relativa: " + str(masHumedo.anio) +
                  " (" + self.calculo.formatear(masHumedo.humedadPromedio(), 2) + " %)")

    def serieMensual(self, registroAnual, magnitud):
        """
        Arma las listas de meses y valores de una magnitud para un anio, para
        poder dibujarlas en el grafico.

        Args:
            registroAnual (RegistroAnual): Anio del que se arma la serie.
            magnitud (str): Magnitud a graficar.

        Returns:
            tuple: Lista de numeros de mes y lista de valores correspondientes.
        """
        numerosMes = []
        valores = []
        for mes in registroAnual.meses:
            valor = self.valorMensual(mes, magnitud)
            if valor != None:
                numerosMes.append(mes.mes)
                valores.append(valor)
        return numerosMes, valores

    def graficar(self):
        """
        Genera un grafico con cuatro paneles (temperatura, humedad,
        precipitacion y viento) en el que cada anio del periodo se dibuja como
        una linea distinta, para poder comparar su evolucion mes a mes. El
        grafico se guarda como imagen PNG y luego se muestra en pantalla.

        Returns:
            str: Nombre del archivo PNG generado, o None si no se pudo graficar.
        """
        if len(self.anios) == 0:
            print("\nNo hay datos suficientes para generar el grafico.")
            return None

        magnitudes = [
            ("temperatura", "Temperatura promedio", "Grados Celsius"),
            ("humedad", "Humedad relativa promedio", "Porcentaje"),
            ("precipitacion", "Precipitacion acumulada", "Milimetros"),
            ("viento", "Velocidad del viento", "km/h")
        ]

        try:
            figura, ejes = plt.subplots(2, 2, figsize=(14, 9))
            figura.suptitle("Evolucion mensual por anio - " + self.localidad.nombre +
                            " (" + self.municipio.nombre + ")\nPeriodo: " +
                            self.fechaInicio + " a " + self.fechaFin, fontsize=13)

            for i in range(len(magnitudes)):
                magnitud = magnitudes[i][0]
                titulo = magnitudes[i][1]
                etiquetaY = magnitudes[i][2]
                eje = ejes[i // 2][i % 2]

                for registroAnual in self.anios:
                    numerosMes, valores = self.serieMensual(registroAnual, magnitud)
                    if len(valores) == 0:
                        continue
                    eje.plot(numerosMes, valores, marker="o", label=str(registroAnual.anio))

                eje.set_title(titulo)
                eje.set_xlabel("Mes")
                eje.set_ylabel(etiquetaY)
                eje.set_xticks(range(1, 13))
                eje.grid(True, linestyle="--", alpha=0.5)
                eje.legend(title="Anio", fontsize=8)

            plt.tight_layout(rect=[0, 0, 1, 0.94])

            nombreArchivo = "historico_" + self.nombreArchivoValido() + ".png"
            plt.savefig(nombreArchivo)
            print("\nGrafico guardado como: " + nombreArchivo)
            print("Cierre la ventana del grafico para volver al menu.")
            plt.show()
            plt.close(figura)
            return nombreArchivo
        except Exception as error:
            print("\nNo se pudo generar el grafico: " + str(error))
            return None

    def nombreArchivoValido(self):
        """
        Arma un nombre de archivo sin espacios ni caracteres raros a partir del
        nombre de la localidad y del periodo consultado.

        Returns:
            str: Texto apto para usar como nombre de archivo.
        """
        texto = self.localidad.nombre + "_" + self.fechaInicio + "_" + self.fechaFin
        limpio = ""
        for caracter in texto:
            if caracter.isalnum() or caracter == "_" or caracter == "-":
                limpio = limpio + caracter
            else:
                limpio = limpio + "_"
        return limpio
