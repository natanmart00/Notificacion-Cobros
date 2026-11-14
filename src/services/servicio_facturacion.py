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

    # genera cargos desde el ultimo mes facturado
    def generar_cargos_retroactivos(self):
        # obtiene los datos de la tabla control
        mes_inicial = self.control_repo.obtener_mes_inicial()
        mes_actual = self.control_repo.obtener_mes_actual()
        ultimo_mes = self.control_repo.obtener_valor("ultimo_mes_facturado")

        # negocio: factura todos los periodos adeudados desde el inicio o ultimo cobro
        # framework: meses_entre() avanza al mes siguiente asumiendo inicio ya cobrado
        # codigo: si ultimo_mes no existia, se omitia mes_inicial sin ser cobrado
        # resolucion: incluye mes_inicial si es la primera corrida o avanza si ya existe
        if ultimo_mes:
            meses_pendientes = UtilidadesFecha.meses_entre(
                str(ultimo_mes).strip(), mes_actual
            )
        elif mes_inicial:
            mes_inicio = str(mes_inicial).strip()
            if mes_inicio <= mes_actual:
                meses_pendientes = [mes_inicio] + UtilidadesFecha.meses_entre(
                    mes_inicio, mes_actual
                )
            else:
                meses_pendientes = []
        else:
            meses_pendientes = [mes_actual]

        # si no hay meses pendientes, retorna lista vacia
        if not meses_pendientes:
            print("ℹ️ No hay meses pendientes de facturar.")
            return []

        # devuelve un diccionario {id: datos}
        servicios = self.servicios_repo.obtener_servicios()
        # devuelve una lista de suscripciones activas
        suscripciones = self.suscripciones_repo.obtener_suscripciones_activas()

        # negocio: asociar cada suscripcion con su respectivo servicio comercial
        # framework: gspread puede devolver enteros o cadenas segun el formato de celda
        # codigo: discordancia de tipo entre id entero y cadena devolvia None
        # resolucion: indexa servicios por clave en texto y valida activo flexiblemente
        servicios_por_id = {str(k).strip(): v for k, v in servicios.items()}

        # lista para acumular los cargos a insertar
        filas = []
        # por cada mes pendiente ej: "2024-05", "2024-06"
        for mes in meses_pendientes:
            for sub in suscripciones:
                sub_srv_id = str(sub.get("servicio_id", "")).strip()
                servicio = servicios_por_id.get(sub_srv_id)

                if not servicio:
                    continue

                valor_activa = servicio.get("activa", servicio.get("activo", ""))
                es_activo = (
                    str(valor_activa).strip().upper() in ["TRUE", "VERDADERO", "1"]
                    or valor_activa is True
                )
                if not es_activo:
                    continue

                filas.append([
                    "",
                    date.today().isoformat(),
                    mes,
                    sub.get("suscripcion_id"),
                    "CARGO",
                    servicio.get("costo"),
                    "SCRIPT",
                ])

        # si se generaron cargos
        if filas:
            self.movimientos_repo.insertar_cargos(filas)
            self.control_repo.actualizar_valor(
                "ultimo_mes_facturado", meses_pendientes[-1]
            )
            self.control_repo.actualizar_valor("mes_actual", mes_actual)
            print(f"✅ Cargos generados exitosamente hasta el mes: {meses_pendientes[-1]}")
        else:
            print("ℹ️ No se generaron nuevos cargos en esta ejecución.")

        return filas
    
"""
Flujo:
1. consulta que meses hay pendientes de facturar
2. por cada mes pendiente, recorre las suscripciones activas
3. genera un cargo por cada suscripción activa y servicio activo
4. inserta los cargos en la tabla de movimientos
5. actualiza el ultimo mes facturado en la tabla control
"""