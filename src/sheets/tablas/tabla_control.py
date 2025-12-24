from src.sheets.google_sheets import ClienteGoogleSheets
from datetime import date

class ControlRepositorio:
    """
    Acceso a la tabla 'control' para configuraciones del sistema
    """

    #se conecta a la hoja llamada control de google_sheets
    def __init__(self):
        self.ws = ClienteGoogleSheets().obtener_hoja("control")

    #retorna todos los registros de la hoja como lista de diccionarios
    #metodo privado
    def _obtener_todos_los_registros(self):
        """Método interno para leer la hoja completa"""
        return self.ws.get_all_records()

    #obtiene el valor de una de las claves de la tabla
    #ejemplo obtener_valor("mes_inicial")  retorna "2024-01"
    def obtener_valor(self, clave_buscada: str):
        """
        Busca una clave en la columna 'clave' y retorna su 'valor'
        """
        registros = self._obtener_todos_los_registros()
        for reg in registros:
            #usamos strip() por si hay espacios accidentales en el Sheets
            if str(reg.get("clave")).strip() == clave_buscada:
                return reg.get("valor")
        
        return None
    
    #usa el metodo general obtener_valor para buscar solo el mes inicial
    def obtener_mes_inicial(self):
        return self.obtener_valor("mes_inicial")

    #usa el metodo obtener_valor para buscar el mes actual,
    #si no existe usa la fecha actual y formateamos %Y-%m para que devuelva "2025-12"
    def obtener_mes_actual(self):
        mes_actual = self.obtener_valor("mes_actual") or date.today().strftime("%Y-%m")
        return mes_actual

    
    def actualizar_valor(self, clave: str, nuevo_valor: str):
        """
        Busca la fila de la clave y actualiza su valor en Google Sheets
        """
        registros = self.ws.get_all_records()
        for i, reg in enumerate(registros):
            if reg.get("clave") == clave:
                """
                gspread indexa desde 1, donde la fila 1 sería el encabezado,
                por eso empezamos desde i+2
                
                donde en update_cell(fila,columna,valor)
                """
                self.ws.update_cell(i + 2, 2, nuevo_valor) 
                return True
        return False