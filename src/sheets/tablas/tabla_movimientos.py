from sheets.google_sheets import ClienteGoogleSheets


class MovimientosRepositorio:
    """
    Acceso a la tabla 'movimientos'
    """

    def __init__(self):
        self.ws = ClienteGoogleSheets().obtener_hoja("movimientos")

    def obtener_todos(self) -> list[dict]:
        return self.ws.get_all_records()

    def insertar_cargos(self, filas: list[list]):
        """
        Inserta múltiples cargos de una sola vez
        """
        if filas:
            self.ws.append_rows(filas, value_input_option="USER_ENTERED")
