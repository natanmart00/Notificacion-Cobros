from collections import defaultdict
from src.sheets.tablas.tabla_usuarios import Usuarios
from src.sheets.tablas.tabla_suscripciones import SuscripcionesRepositorio
from src.sheets.tablas.tabla_servicios import ServiciosRepositorio
from src.sheets.tablas.tabla_movimientos import MovimientosRepositorio

class ServicioMensaje:
    def __init__(self):
        self.usuarios_repo = Usuarios()
        self.movimientos_repo = MovimientosRepositorio()
        self.suscripciones_repo = SuscripcionesRepositorio()
        self.servicios_repo = ServiciosRepositorio()
        
    def formatear_monto(self, valor):
        if valor == "" or valor is None: return 0.0
        try:
            if isinstance(valor, (int, float)): return float(valor)
            return float(str(valor).replace("$", "").replace(",", "").strip())
        except:
            return 0.0

    def construir_mensaje(self) -> str:
        # 1. Cargar datos maestros
        usuarios_map = self.usuarios_repo.obtener_usuarios()
        suscripciones_map = {s["suscripcion_id"]: s for s in self.suscripciones_repo.ws.get_all_records()}
        servicios_map = self.servicios_repo.obtener_todos()
        movimientos = self.movimientos_repo.obtener_todos()

        # 2. Agrupar TODO por Usuario
        # pagos_globales[u_id] = float
        # cargos_globales[u_id] = [ {mes, s_id, monto}, ... ]
        pagos_globales = defaultdict(float)
        cargos_globales = defaultdict(list)

        for mov in movimientos:
            sub = suscripciones_map.get(mov["suscripcion_id"])
            if not sub: continue
            
            u_id = sub["usuario_id"]
            monto = self.formatear_monto(mov["monto"])
            tipo = str(mov.get("tipo", "CARGO")).upper().strip()

            if tipo == "PAGO":
                pagos_globales[u_id] += monto
            else:
                cargos_globales[u_id].append({
                    "mes": mov["mes"],
                    "s_id": sub["servicio_id"],
                    "monto": monto
                })

        # 3. Construir el mensaje
        lineas = ["* RESUMEN GLOBAL DE CUENTAS*\n"]
        hay_deuda_general = False

        for u_id in sorted(cargos_globales.keys()):
            usuario_data = usuarios_map.get(u_id)
            if not usuario_data: continue
            
            nombre_usuario = usuario_data["nombre"]
            # Ordenamos TODOS los cargos del usuario por mes cronológicamente
            todos_los_cargos = sorted(cargos_globales[u_id], key=lambda x: x["mes"])
            saldo_pagos = pagos_globales[u_id]
            
            # Aquí guardaremos la deuda final ya procesada
            # estructura: deuda_final[nombre_servicio] = [lineas de texto]
            deuda_final_por_servicio = defaultdict(list)
            total_usuario = 0

            for cargo in todos_los_cargos:
                monto_cargo = cargo["monto"]
                nombre_srv = servicios_map.get(cargo["s_id"], {}).get("nombre", "Servicio")
                
                monto_pendiente = 0
                if saldo_pagos >= monto_cargo:
                    saldo_pagos -= monto_cargo
                elif saldo_pagos > 0:
                    monto_pendiente = monto_cargo - saldo_pagos
                    saldo_pagos = 0
                else:
                    monto_pendiente = monto_cargo

                if monto_pendiente > 0:
                    texto_abono = " (abono)" if monto_pendiente < monto_cargo else ""
                    deuda_final_por_servicio[nombre_srv].append(
                        f"    • {cargo['mes']}: ${monto_pendiente:.2f}{texto_abono}"
                    )
                    total_usuario += monto_pendiente

            # 4. Formatear el mensaje del usuario
            if deuda_final_por_servicio:
                hay_deuda_general = True
                lineas.append(f"👤 {nombre_usuario.upper()}")
                
                for srv_nombre, detalles in deuda_final_por_servicio.items():
                    lineas.append(f"   *{srv_nombre}*")
                    lineas.extend(detalles)
                
                lineas.append(f"  *TOTAL DEUDA: ${total_usuario:.2f}*")
                lineas.append("") 
            
            elif saldo_pagos > 0:
                hay_deuda_general = True
                lineas.append(f"👤 {nombre_usuario.upper()}")
                lineas.append(f"   Saldo a favor global: ${saldo_pagos:.2f}")
                lineas.append("")

        return "\n".join(lineas) if hay_deuda_general else "✔ Todos los saldos están al día."