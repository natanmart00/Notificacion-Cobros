from collections import defaultdict
from sheets.tablas.tabla_suscripciones import SuscripcionesRepositorio
from sheets.tablas.tabla_servicios import ServiciosRepositorio
from sheets.tablas.tabla_movimientos import MovimientosRepositorio


class ServicioMensaje:
    """
    Construye el mensaje de deuda agrupado por persona, servicio y mes
    """

    def __init__(self):
        self.movimientos_repo = MovimientosRepositorio()
        self.suscripciones_repo = SuscripcionesRepositorio()
        self.servicios_repo = ServiciosRepositorio()

    def construir_mensaje(self) -> str:
        movimientos = self.movimientos_repo.obtener_todos()
        suscripciones = {
            s["suscripcion_id"]: s
            for s in self.suscripciones_repo.obtener_activas()
        }
        servicios = self.servicios_repo.obtener_todos()

        deuda = defaultdict(lambda: defaultdict(float))

        for mov in movimientos:
            sub = suscripciones.get(mov["suscripcion_id"])
            if not sub:
                continue

            nombre = sub["nombre"]
            servicio = servicios[sub["servicio_id"]]["nombre"]
            mes = mov["mes"]

            deuda[(nombre, servicio)][mes] += float(mov["monto"])

        lineas = ["Resumen de pagos pendientes:\n"]

        for (nombre, servicio), meses in deuda.items():
            pendientes = {m: v for m, v in meses.items() if v > 0}
            if not pendientes:
                continue

            lineas.append(f"{nombre} - {servicio}")
            total = 0

            for mes, monto in sorted(pendientes.items()):
                lineas.append(f"  • {mes}: ${monto:.2f}")
                total += monto

            lineas.append(f"  Total: ${total:.2f}\n")

        return "\n".join(lineas)
