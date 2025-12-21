from datetime import date
from sheets.tablas.tabla_suscripciones import SuscripcionesRepositorio
from sheets.tablas.tabla_servicios import ServiciosRepositorio
from sheets.tablas.tabla_movimientos import MovimientosRepositorio
from sheets.tablas.tabla_control import ControlRepositorio
from utils.fechas import UtilidadesFecha


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
        ultimo_mes = self.control_repo.obtener_valor("ultimo_mes_facturado")
        mes_actual = UtilidadesFecha.mes_actual()

        meses_pendientes = UtilidadesFecha.meses_entre(
            ultimo_mes, mes_actual
        )

        if not meses_pendientes:
            return

        servicios = self.servicios_repo.obtener_todos()
        suscripciones = self.suscripciones_repo.obtener_activas()

        filas = []

        for mes in meses_pendientes:
            for sub in suscripciones:
                servicio = servicios[sub["servicio_id"]]

                filas.append([
                    "",  # movimiento_id (lógico)
                    date.today().isoformat(),
                    mes,
                    sub["suscripcion_id"],
                    "CARGO",
                    servicio["costo"],
                    "SCRIPT"
                ])

        self.movimientos_repo.insertar_cargos(filas)
        self.control_repo.actualizar_valor(
            "ultimo_mes_facturado",
            meses_pendientes[-1]
        )
