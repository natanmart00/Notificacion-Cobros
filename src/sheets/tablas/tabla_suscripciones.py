from sheets.google_sheets import ClienteGoogleSheets


class SuscripcionesRepositorio:
    """
    Acceso a la tabla 'suscripciones'
    """

    def __init__(self):
        self.ws = ClienteGoogleSheets().obtener_hoja("suscripciones")

    def obtener_activas(self) -> list[dict]:
        registros = self.ws.get_all_records()
        return [r for r in registros if r["activa"]]
