from src.sheets.google_sheets import ClienteGoogleSheets
from datetime import date

class ControlRepositorio:
    """
    Acceso a la tabla 'control' para configuraciones del sistema
    """

    #se conecta a la hoja llamada control de google_sheets
    def __init__(self):
        self.ws = ClienteGoogleSheets().obtener_hoja("control")

    #retorna todos los registros de la hoja como lista de diccionarios
    #metodo privado
    def _obtener_todos_los_registros(self):
        """Método interno para leer la hoja completa"""
        return self.ws.get_all_records()

    #obtiene el valor de una de las claves de la tabla
    #ejemplo obtener_valor("mes_inicial")  retorna "2024-01"
    def obtener_valor(self, clave_buscada: str):
        """
        Busca una clave en la columna 'clave' y retorna su 'valor'
        """
        registros = self._obtener_todos_los_registros()
        for reg in registros:
            #usamos strip() por si hay espacios accidentales en el Sheets
            if str(reg.get("clave")).strip() == clave_buscada:
                return reg.get("valor")
        
        return None
    
    #usa el metodo general obtener_valor para buscar solo el mes inicial
    def obtener_mes_inicial(self):
        return self.obtener_valor("mes_inicial")

    def obtener_mes_actual(self):
        # negocio: el cobro debe calcularse contra el periodo en curso real
        # framework: google sheets conserva valores de texto estaticos en celdas
        # codigo: si "mes_actual" tenia texto antiguo, impedia usar la fecha de hoy
        # resolucion: compara con el reloj del sistema y prioriza el mes mas reciente
        mes_real = date.today().strftime("%Y-%m")
        mes_hoja = self.obtener_valor("mes_actual")
        if not mes_hoja:
            return mes_real
        mes_limpio = str(mes_hoja).strip()
        if len(mes_limpio) != 7 or "-" not in mes_limpio or mes_limpio < mes_real:
            return mes_real
        return mes_limpio
    
    def actualizar_valor(self, clave: str, nuevo_valor: str):
        # negocio: sincroniza el estado de ejecucion para no duplicar ni perder cobros
        # framework: gspread indexa filas iniciando en 1 donde la fila 1 es encabezado
        # codigo: si la clave no existia retornaba "false" y no persistia el avance
        # resolucion: busca fila con limpieza de espacios o agrega fila si no existe
        registros = self.ws.get_all_records()
        for i, reg in enumerate(registros):
            if str(reg.get("clave", "")).strip() == clave:
                self.ws.update_cell(i + 2, 2, nuevo_valor) 
                return True
        self.ws.append_row([clave, nuevo_valor, ""])
        return True