from Calculo import Calculo

class RegistroMensual:
    """
    Clase RegistroMensual que agrupa todos los registros diarios de un mismo
    mes de un mismo anio y calcula sus valores resumidos.

    Atributos:
        anio (int): Anio del mes.
        mes (int): Numero del mes (1 a 12).
        registrosDiarios (list): Lista de objetos RegistroDiario de ese mes.
        calculo (Calculo): Objeto de apoyo para los calculos numericos.
    """

    NOMBRES_MESES = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
                     "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]

    def __init__(self, anio, mes):
        """
        Inicializa una instancia de la clase RegistroMensual sin dias cargados.

        Args:
            anio (int): Anio del mes.
            mes (int): Numero del mes (1 a 12).
        """
        self.anio = anio
        self.mes = mes
        self.registrosDiarios = []
        self.calculo = Calculo()

    def agregarDia(self, registro):
        """
        Agrega un registro diario al mes.

        Args:
            registro (RegistroDiario): Registro del dia a agregar.
        """
        self.registrosDiarios.append(registro)

    def nombreMes(self):
        """
        Devuelve el nombre del mes en palabras.

        Returns:
            str: Nombre del mes (por ejemplo "Enero").
        """
        return RegistroMensual.NOMBRES_MESES[self.mes - 1]

    def cantidadDias(self):
        """
        Indica cuantos dias tiene cargados el mes.

        Returns:
            int: Cantidad de registros diarios del mes.
        """
        return len(self.registrosDiarios)

    def temperaturaPromedio(self):
        """
        Calcula la temperatura promedio del mes.

        Returns:
            float: Temperatura promedio en grados Celsius, o None si no hay datos.
        """
        valores = []
        for registro in self.registrosDiarios:
            valores.append(registro.temperatura)
        return self.calculo.promedio(valores)

    def humedadPromedio(self):
        """
        Calcula la humedad relativa promedio del mes.

        Returns:
            float: Humedad relativa promedio en porcentaje, o None si no hay datos.
        """
        valores = []
        for registro in self.registrosDiarios:
            valores.append(registro.humedad)
        return self.calculo.promedio(valores)

    def precipitacionAcumulada(self):
        """
        Suma la precipitacion de todos los dias del mes.

        Returns:
            float: Precipitacion acumulada en mm, o None si no hay datos.
        """
        valores = []
        for registro in self.registrosDiarios:
            valores.append(registro.precipitacion)
        return self.calculo.total(valores)

    def vientoPromedio(self):
        """
        Calcula la velocidad promedio del viento del mes.

        Returns:
            float: Velocidad promedio del viento en km/h, o None si no hay datos.
        """
        valores = []
        for registro in self.registrosDiarios:
            valores.append(registro.viento)
        return self.calculo.promedio(valores)
