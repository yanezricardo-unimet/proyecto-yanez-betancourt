from Calculo import Calculo

class RegistroAnual:
    """
    Clase RegistroAnual que agrupa los meses de un mismo anio y calcula sus
    valores resumidos. Se usa para determinar el anio mas caluroso, el mas
    fresco, el mas lluvioso y el mas humedo del periodo consultado.

    Atributos:
        anio (int): Anio representado.
        meses (list): Lista de objetos RegistroMensual de ese anio.
        calculo (Calculo): Objeto de apoyo para los calculos numericos.
    """

    def __init__(self, anio):
        """
        Inicializa una instancia de la clase RegistroAnual sin meses cargados.

        Args:
            anio (int): Anio representado.
        """
        self.anio = anio
        self.meses = []
        self.calculo = Calculo()

    def agregarMes(self, registroMensual):
        """
        Agrega un registro mensual al anio.

        Args:
            registroMensual (RegistroMensual): Registro del mes a agregar.
        """
        self.meses.append(registroMensual)

    def cantidadMeses(self):
        """
        Indica cuantos meses tiene cargados el anio.

        Returns:
            int: Cantidad de meses del anio.
        """
        return len(self.meses)

    def temperaturaPromedio(self):
        """
        Calcula la temperatura promedio del anio a partir de sus meses.

        Returns:
            float: Temperatura promedio en grados Celsius, o None si no hay datos.
        """
        valores = []
        for mes in self.meses:
            valores.append(mes.temperaturaPromedio())
        return self.calculo.promedio(valores)

    def humedadPromedio(self):
        """
        Calcula la humedad relativa promedio del anio a partir de sus meses.

        Returns:
            float: Humedad relativa promedio en porcentaje, o None si no hay datos.
        """
        valores = []
        for mes in self.meses:
            valores.append(mes.humedadPromedio())
        return self.calculo.promedio(valores)

    def precipitacionAcumulada(self):
        """
        Suma la precipitacion de todos los meses del anio.

        Returns:
            float: Precipitacion acumulada en mm, o None si no hay datos.
        """
        valores = []
        for mes in self.meses:
            valores.append(mes.precipitacionAcumulada())
        return self.calculo.total(valores)

    def vientoPromedio(self):
        """
        Calcula la velocidad promedio del viento del anio a partir de sus meses.

        Returns:
            float: Velocidad promedio del viento en km/h, o None si no hay datos.
        """
        valores = []
        for mes in self.meses:
            valores.append(mes.vientoPromedio())
        return self.calculo.promedio(valores)
