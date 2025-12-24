from src.sheets.google_sheets import ClienteGoogleSheets

class Usuarios:
    """
    Acceso a la tabla 'usuarios'
    """

    #inicializa la conexion
    def __init__(self):
        self.ws = ClienteGoogleSheets().obtener_hoja("usuarios")

    #obtiene la lista de usuarios
    def obtener_usuarios(self) -> list[dict]:
        registros = self.ws.get_all_records()
        return {r["usuario_id"]: r for r in registros}
