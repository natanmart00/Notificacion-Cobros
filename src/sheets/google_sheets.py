import gspread
from src.config.settings import Settings


class ClienteGoogleSheets:
    """
    Cliente para Google Sheets.
    """

    #inicializa la conexion a Google Sheets
    def __init__(self):
        #accede a las credenciales del .env
        ruta_credenciales = Settings.ruta("GOOGLE_CREDENTIALS_PATH")

        #crea las credenciales de OAuth2
        #inicializa un cliente autorizado con las credenciales
        self.cliente = gspread.service_account(
            filename=str(ruta_credenciales),
            scopes=[
                #leer y modificar hojas de calculo
                "https://www.googleapis.com/auth/spreadsheets",
                #acceder a archivos de google drive
                "https://www.googleapis.com/auth/drive"
            ]
        )
        #abre una hoja de calculo especifica
        self.spreadsheet = self.cliente.open_by_key(
            #accede al valor de la hoja de calculo del .env
            Settings.valor("SPREADSHEET_ID")
        )

    #accede a una hoja especifica
    def obtener_hoja(self, nombre_hoja: str):
        return self.spreadsheet.worksheet(nombre_hoja)
