from src.sheets.google_sheets import ClienteGoogleSheets


class Dashboard:
    """
    Hoja derivada para visualización (Looker / consultas)
    Se sobrescribe completamente en cada ejecución
    """

    HEADERS = [
        "usuario_id",
        "usuario",
        "servicio",
        "mes",
        "monto_pendiente"
    ]

    def __init__(self):
        self.ws = ClienteGoogleSheets().obtener_hoja("dashboard")

    def sobrescribir(self, filas: list[list]):
        """
        Borra la hoja y escribe el estado actual de deudas
        """
        self.ws.clear()

        if not filas:
            self.ws.append_row(self.HEADERS)
            return

        self.ws.append_row(self.HEADERS)
        self.ws.append_rows(filas, value_input_option="USER_ENTERED")
