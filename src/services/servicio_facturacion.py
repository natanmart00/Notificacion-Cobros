from datetime import date
from src.sheets.tablas.tabla_suscripciones import SuscripcionesRepositorio
from src.sheets.tablas.tabla_servicios import ServiciosRepositorio
from src.sheets.tablas.tabla_movimientos import MovimientosRepositorio
from src.sheets.tablas.tabla_control import ControlRepositorio
from src.utils.fechas import UtilidadesFecha


class ServicioFacturacion:
    """
    Servicio encargado de generar cargos mensuales
    """

    def __init__(self):
        #inicializa repositorios (conexiones a las tablas de Google Sheets)
        self.servicios_repo = ServiciosRepositorio()
        self.suscripciones_repo = SuscripcionesRepositorio()
        self.movimientos_repo = MovimientosRepositorio()
        self.control_repo = ControlRepositorio()

    #genera cargos desde el ultimo mes factuado
    def generar_cargos_retroactivos(self):
        #obtiene los datos de la tabla control
        #mes donde inicia la facturación
        mes_inicial = self.control_repo.obtener_mes_inicial()
        #mes actual del sistema
        mes_actual = self.control_repo.obtener_mes_actual()
        #ultimo mes facturado
        ultimo_mes = self.control_repo.obtener_valor("ultimo_mes_facturado")

        #calcula los meses pendientes de facturar
        #empieza por el ultimo mes, si esta vacío sigue con el mes inicial y luego con el actual
        desde = ultimo_mes or mes_inicial or mes_actual
        #calcula los meses intermedios
        meses_pendientes = UtilidadesFecha.meses_entre(desde, mes_actual)

        #si no hay meses pendientes, retorna lista vacia
        if not meses_pendientes:
            return [] 

        #devuelve un diccionario {id: datos}
        servicios = self.servicios_repo.obtener_servicios()
        #devuelve una lista de suscripciones activas
        #retorna:
        """
        {'suscripcion_id': 1, 'usuario_id': 1, 'servicio_id': 1, 'activa': 'TRUE'}
        {'suscripcion_id': 2, 'usuario_id': 2, 'servicio_id': 1, 'activa': 'TRUE'}
        """
        suscripciones = self.suscripciones_repo.obtener_suscripciones_activas()

        #lista para acumular los cargos a insertar
        filas = []
        #por cada mes pendiente ej: '2024-05', '2024-06'
        for mes in meses_pendientes:
            #recorremos las suscripciones activas
            for sub in suscripciones:
                #busca el servicio correspondiente a esta suscripción
                servicio = servicios.get(sub["servicio_id"])
                
                #solo generamos cargo si el servicio existe Y está activo
                #(La suscripción ya viene filtrada por 'obtener_suscripciones_activas')
                if not servicio or not servicio.get("activa"):
                    #salta a la siguiente
                    continue

                #crea una fila para insertar en la tabla de movimientos
                filas.append([
                    #id vacío (no necesario)
                    "", 
                    #fecha de creacion del cargo
                    date.today().isoformat(),
                    #mes que se esta facturando
                    mes,
                    #id de la suscripcion
                    sub["suscripcion_id"],
                    #tipo de movimiento
                    "CARGO",
                    #monto del servicio
                    servicio["costo"],
                    #origen /creado por el script
                    "SCRIPT"
                ])

        #si se generaron cargos
        if filas:
            #inserta en tabla de movimientos
            self.movimientos_repo.insertar_cargos(filas)
            #actualiza el ultimo mes facturado en la tabla control
            self.control_repo.actualizar_valor("ultimo_mes_facturado", meses_pendientes[-1])

        #retorna las filas generadas
        return filas
    
"""
Flujo:
1. consulta que meses hay pendientes de facturar
2. por cada mes pendiente, recorre las suscripciones activas
3. genera un cargo por cada suscripción activa y servicio activo
4. inserta los cargos en la tabla de movimientos
5. actualiza el ultimo mes facturado en la tabla control
"""