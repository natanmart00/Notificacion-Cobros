from src.sheets.google_sheets import ClienteGoogleSheets


class Dashboard:
    """
    Hoja derivada para visualización (Looker / consultas)
    Se sobrescribe completamente en cada ejecución
    """

    #inicializamos los encabezados de la tabla
    HEADERS = [
        "usuario_id",
        "usuario",
        "servicio",
        "mes",
        "monto_pendiente"
    ]

    #creamos la conexion a la hoja dashboard
    def __init__(self):
        self.ws = ClienteGoogleSheets().obtener_hoja("dashboard")

    #sobreescribimos la hoja dashboard
    def sobrescribir(self, filas: list[list]):
        """
        Borra la hoja y escribe el estado actual de deudas
        """
        #limpiamos la hoja
        self.ws.clear()
        
        #sobreescribimos los encabezados
        self.ws.append_row(self.HEADERS)
        
        #luego escribir las filas si existen
        if filas:
            self.ws.append_rows(filas, value_input_option="USER_ENTERED")
