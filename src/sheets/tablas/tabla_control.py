from sheets.google_sheets import ClienteGoogleSheets


class ControlRepositorio:
    """
    Maneja el estado interno del sistema
    """

    def __init__(self):
        self.ws = ClienteGoogleSheets().obtener_hoja("control")

    def obtener_valor(self, clave: str) -> str:
        registros = self.ws.get_all_records()
        for r in registros:
            if r["clave"] == clave:
                return r["valor"]
        return None

    def actualizar_valor(self, clave: str, valor: str):
        celda = self.ws.find(clave)
        self.ws.update_cell(celda.row, celda.col + 1, valor)
