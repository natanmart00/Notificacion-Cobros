from src.sheets.google_sheets import ClienteGoogleSheets


class Dashboard:
    """
    Hoja derivada para visualización (Looker / consultas)
    Se sobrescribe completamente en cada ejecución
    """

    #inicializamos los encabezados de la tabla
    HEADERS = [
        "usuario_id",
        "usuario",
        "servicio",
        "mes",
        "monto_pendiente"
    ]

    #creamos la conexion a la hoja dashboard
    def __init__(self):
        self.ws = ClienteGoogleSheets().obtener_hoja("dashboard")

    #sobreescribimos la hoja dashboard
    def sobrescribir(self, filas: list[list]):
        """
        Borra solo los datos (a partir de la fila 2) y escribe nuevas filas
        """
        #obtiene todos los datos actuales de la hoja
        datos_actuales = self.ws.get_all_values()
        
        #limpia solo desde la fila 2 en adelante
        if len(datos_actuales) > 1:
            #calcula el rango a borrar (desde fila 2 hasta el final)
            num_columnas = len(self.HEADERS)
            #convierte el numero de columna a letra de excel: 
            #chr(62+5) = "E"
            letra_columna_final = chr(64 + num_columnas)
            #si letra_columna_final = "E" y len(datos_actuales=5), rango_borrar = "A2:E5"
            rango_borrar = f"A2:{letra_columna_final}{len(datos_actuales)}"
            #boora el rango en la hoja de calculo
            self.ws.batch_clear([rango_borrar])
        
        #si hay filas para escribir, actualizar a partir de la fila 2
        if filas:
            #determina rango para actualizar
            num_filas = len(filas)
            num_columnas = len(self.HEADERS)
            letra_columna_final = chr(64 + num_columnas)
            
            #crea el rango donde se escribiran los nuevos datos
            rango_actualizar = f"A2:{letra_columna_final}{num_filas + 1}"
            #escribe los nuevos datos en el rango calculado
            self.ws.update(values=filas, range_name=rango_actualizar, value_input_option="USER_ENTERED")
            