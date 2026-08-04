from src.sheets.google_sheets import ClienteGoogleSheets


class SuscripcionesRepositorio:
    """
    Acceso a la tabla 'suscripciones'
    """

    #inicializa la conexion
    def __init__(self):
        self.ws = ClienteGoogleSheets().obtener_hoja("suscripciones")

    #obtiene las suscripciones activas
    def obtener_suscripciones_activas(self) -> list[dict]:
        registros = self.ws.get_all_records()
        
        #retorna:
        """
        {'suscripcion_id': 1, 'usuario_id': 1, 'servicio_id': 1, 'activa': 'TRUE'}
        {'suscripcion_id': 2, 'usuario_id': 2, 'servicio_id': 1, 'activa': 'TRUE'}
        """
        return [r for r in registros if str(r.get("activa", "")).strip().upper() == "TRUE"]
