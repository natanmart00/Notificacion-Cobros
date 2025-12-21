from sheets.google_sheets import ClienteGoogleSheets


class ServiciosRepositorio:
    """
    Acceso a la tabla 'servicios'
    """

    def __init__(self):
        self.ws = ClienteGoogleSheets().obtener_hoja("servicios")

    def obtener_todos(self) -> dict:
        """
        Devuelve servicios indexados por servicio_id
        """
        registros = self.ws.get_all_records()
        return {r["servicio_id"]: r for r in registros}
