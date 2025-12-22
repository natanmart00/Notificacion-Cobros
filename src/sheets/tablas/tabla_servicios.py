from src.sheets.google_sheets import ClienteGoogleSheets


class ServiciosRepositorio:
    """
    Acceso a la tabla 'servicios'
    """

    def __init__(self):
        self.ws = ClienteGoogleSheets().obtener_hoja("servicios")

    def obtener_todos(self) -> dict[int, dict]:
        """
        Devuelve un diccionario indexado por servicio_id
        {
            servicio_id: {datos del servicio}
        }
        """

        registros = self.ws.get_all_records()
        return {r["servicio_id"]: r for r in registros}
