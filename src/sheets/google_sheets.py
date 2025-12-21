import os
import gspread
from google.oauth2.service_account import Credentials


class ClienteGoogleSheets:
    """
    Cliente centralizado para acceder a Google Sheets
    """

    SCOPES = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]

    def __init__(self):
        credenciales = Credentials.from_service_account_file(
            os.getenv("GOOGLE_CREDENTIALS_PATH"),
            scopes=self.SCOPES
        )
        self.cliente = gspread.authorize(credenciales)
        self.spreadsheet = self.cliente.open_by_key(
            os.getenv("SPREADSHEET_ID")
        )

    def obtener_hoja(self, nombre_hoja: str):
        return self.spreadsheet.worksheet(nombre_hoja)
