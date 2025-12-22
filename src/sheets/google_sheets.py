import gspread
from google.oauth2.service_account import Credentials
from src.config.settings import Settings


class ClienteGoogleSheets:
    """
    Cliente centralizado para Google Sheets.
    """

    def __init__(self):
        ruta_credenciales = Settings.ruta("GOOGLE_CREDENTIALS_PATH")

        credenciales = Credentials.from_service_account_file(
            ruta_credenciales,
            scopes=[
                "https://www.googleapis.com/auth/spreadsheets",
                "https://www.googleapis.com/auth/drive"
            ]
        )

        self.cliente = gspread.authorize(credenciales)
        self.spreadsheet = self.cliente.open_by_key(
            Settings.valor("SPREADSHEET_ID")
        )

    def obtener_hoja(self, nombre_hoja: str):
        return self.spreadsheet.worksheet(nombre_hoja)
