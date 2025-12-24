from src.sheets.google_sheets import ClienteGoogleSheets


class ServiciosRepositorio:
    """
    Acceso a la tabla 'servicios'
    """

    #inicializa la conexion
    def __init__(self):
        self.ws = ClienteGoogleSheets().obtener_hoja("servicios")

    #obtiene todos los registros de la tabla
    def obtener_servicios(self) -> dict[int, dict]:
        """
        Devuelve un diccionario indexado por servicio_id
        {
            servicio_id: {datos del servicio}
        }
        """

        registros = self.ws.get_all_records()
        return {r["servicio_id"]: r for r in registros}
