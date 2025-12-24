from datetime import date


class UtilidadesFecha:
    """
    Clase para manejo de meses en formato YYYY-MM
    """

    #retorna el mes actual en formato YYYY-MM
    @staticmethod
    def mes_actual() -> str:
        hoy = date.today()
        return f"{hoy.year}-{hoy.month:02d}"

    
    @staticmethod
    def siguiente_mes(yyyy_mm: str) -> str:
        #si no hay entrada, retorna error
        if not yyyy_mm:
            raise ValueError("La fecha no puede ser None o vacía")

        #divide la cadena 2025-12 en 2 partes usando el guion como separador
        #luego convierte ambas partes en enteros, asi obtenemos el año y el mes
        anio, mes = map(int, yyyy_mm.split("-"))

        #si el mes es 12 (diciembre) cambia al siguiente año
        if mes == 12:
            return f"{anio + 1}-01"
        
        #retorna YYYY_MM
        return f"{anio}-{mes + 1:02d}"
    
    
    @staticmethod
    def meses_entre(mes_inicial: str, mes_final: str) -> list[str]:
        """
        Devuelve una lista de meses entre mes_inicial
        y mes_final
        """
        meses = []
        #obtiene el mes actual
        actual = UtilidadesFecha.siguiente_mes(mes_inicial)

        #mientras el mes actual sea menor o igual que el mes actual
        while actual <= mes_final:
            #agrega el mes actual
            meses.append(actual)
            #calcula el mes siguiente
            actual = UtilidadesFecha.siguiente_mes(actual)

        return meses
