from datetime import date


class UtilidadesFecha:
    """
    Clase utilitaria para manejo de meses en formato YYYY-MM
    """

    @staticmethod
    def mes_actual() -> str:
        hoy = date.today()
        return f"{hoy.year}-{hoy.month:02d}"

    @staticmethod
    def siguiente_mes(yyyy_mm: str) -> str:
        anio, mes = map(int, yyyy_mm.split("-"))
        if mes == 12:
            return f"{anio + 1}-01"
        return f"{anio}-{mes + 1:02d}"

    @staticmethod
    def meses_entre(mes_inicial: str, mes_final: str) -> list[str]:
        """
        Devuelve una lista de meses entre mes_inicial
        y mes_final
        """
        meses = []
        actual = UtilidadesFecha.siguiente_mes(mes_inicial)

        while actual <= mes_final:
            meses.append(actual)
            actual = UtilidadesFecha.siguiente_mes(actual)

        return meses
