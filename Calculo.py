class Calculo:
    """
    Clase Calculo con operaciones numericas de apoyo que se repiten en varias
    partes del sistema. Todas ignoran los valores None, porque la API historica
    puede no tener el dato de algunos dias.
    """

    def promedio(self, valores):
        """
        Calcula el promedio de una lista de numeros ignorando los None.

        Args:
            valores (list): Lista de numeros que puede contener None.

        Returns:
            float: Promedio de los valores validos, o None si no hay ninguno.
        """
        validos = self.filtrar(valores)
        if len(validos) == 0:
            return None
        return sum(validos) / len(validos)

    def total(self, valores):
        """
        Suma una lista de numeros ignorando los None.

        Args:
            valores (list): Lista de numeros que puede contener None.

        Returns:
            float: Suma de los valores validos, o None si no hay ninguno.
        """
        validos = self.filtrar(valores)
        if len(validos) == 0:
            return None
        return sum(validos)

    def filtrar(self, valores):
        """
        Devuelve solo los valores que no son None de una lista.

        Args:
            valores (list): Lista de numeros que puede contener None.

        Returns:
            list: Lista sin valores None.
        """
        validos = []
        for valor in valores:
            if valor != None:
                validos.append(valor)
        return validos

    def formatear(self, valor, decimales=1):
        """
        Convierte un numero en texto redondeado para mostrarlo en pantalla.

        Args:
            valor (float): Numero a mostrar (puede ser None).
            decimales (int): Cantidad de decimales a usar.

        Returns:
            str: Numero redondeado como texto, o "N/D" si el valor es None.
        """
        if valor == None:
            return "N/D"
        return str(round(valor, decimales))
