from src.sheets.google_sheets import ClienteGoogleSheets

class ControlRepositorio:
    """
    Acceso a la tabla 'control' para configuraciones del sistema
    """

    def __init__(self):
        self.ws = ClienteGoogleSheets().obtener_hoja("control")

    def _obtener_todos_los_registros(self):
        """Método interno para leer la hoja completa"""
        return self.ws.get_all_records()

    def obtener_valor(self, clave_buscada: str):
        """
        Busca una clave en la columna 'clave' y retorna su 'valor'
        """
        registros = self._obtener_todos_los_registros()
        for reg in registros:
            # Usamos strip() por si hay espacios accidentales en el Excel/Sheets
            if str(reg.get("clave")).strip() == clave_buscada:
                return reg.get("valor")
        return None

    def obtener_mes_inicial(self):
        return self.obtener_valor("mes_inicial")

    def obtener_mes_actual(self):
        return self.obtener_valor("mes_actual")

    def actualizar_valor(self, clave: str, nuevo_valor: str):
        """
        Busca la fila de la clave y actualiza su valor en Google Sheets
        """
        registros = self.ws.get_all_records()
        for i, reg in enumerate(registros):
            if reg.get("clave") == clave:
                # +2 porque gspread usa base 1 y hay encabezado
                self.ws.update_cell(i + 2, 2, nuevo_valor) 
                return True
        return False