from src.sheets.google_sheets import ClienteGoogleSheets


class MovimientosRepositorio:
    """
    Acceso a la tabla 'movimientos'
    """

    #inicializa la conexion a la hoja
    def __init__(self):
        self.ws = ClienteGoogleSheets().obtener_hoja("movimientos")

    #obtiene todos los registros de la tabla
    def obtener_movimientos(self) -> list[dict]:
        return self.ws.get_all_records()

    def insertar_cargos(self, filas: list[list]):
        """
        Inserta múltiples cargos de una sola vez
        """
        if filas:
            self.ws.append_rows(filas, value_input_option="USER_ENTERED")
