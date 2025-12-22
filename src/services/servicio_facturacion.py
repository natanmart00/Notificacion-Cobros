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
        self.servicios_repo = ServiciosRepositorio()
        self.suscripciones_repo = SuscripcionesRepositorio()
        self.movimientos_repo = MovimientosRepositorio()
        self.control_repo = ControlRepositorio()

    def generar_cargos_retroactivos(self):
        mes_inicial = self.control_repo.obtener_mes_inicial()
        mes_actual = self.control_repo.obtener_mes_actual()
        ultimo_mes = self.control_repo.obtener_valor("ultimo_mes_facturado")

        desde = ultimo_mes or mes_inicial or mes_actual
        meses_pendientes = UtilidadesFecha.meses_entre(desde, mes_actual)

        if not meses_pendientes:
            return [] 

        # 1. Cargamos TODOS los servicios y suscripciones
        servicios = self.servicios_repo.obtener_todos() # Devuelve dict {id: datos}
        suscripciones = self.suscripciones_repo.obtener_activas()

        filas = []
        for mes in meses_pendientes:
            for sub in suscripciones:
                # Obtenemos los datos del servicio relacionado
                servicio = servicios.get(sub["servicio_id"])
                
                # VALIDACIÓN CRUCIAL:
                # Solo generamos cargo si el servicio existe Y está activo
                # (La suscripción ya viene filtrada por 'obtener_activas')
                if not servicio or not servicio.get("activa"):
                    continue

                filas.append([
                    "", 
                    date.today().isoformat(),
                    mes,
                    sub["suscripcion_id"],
                    "CARGO",
                    servicio["costo"],
                    "SCRIPT"
                ])

        if filas:
            self.movimientos_repo.insertar_cargos(filas)
            self.control_repo.actualizar_valor("ultimo_mes_facturado", meses_pendientes[-1])

        return filas