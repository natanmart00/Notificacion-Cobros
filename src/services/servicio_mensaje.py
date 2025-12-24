from collections import defaultdict
from src.sheets.tablas.tabla_usuarios import Usuarios
from src.sheets.tablas.tabla_suscripciones import SuscripcionesRepositorio
from src.sheets.tablas.tabla_servicios import ServiciosRepositorio
from src.sheets.tablas.tabla_movimientos import MovimientosRepositorio
from src.sheets.tablas.tabla_dashboard import Dashboard

class ServicioMensaje:
    def __init__(self):
        #inicializa los repositorios 
        self.usuarios_repo = Usuarios()
        self.movimientos_repo = MovimientosRepositorio()
        self.suscripciones_repo = SuscripcionesRepositorio()
        self.servicios_repo = ServiciosRepositorio()
        #para guardar los datos en el dashboard
        self.dashboard_repo = Dashboard()
        
    #obtiene un string y lo formatea a float
    def formatear_monto(self, valor):
        #para valores vacíos o nulos
        if valor == "" or valor is None: return 0.0
        try:
            #comprueba si el valor es un entero o float, y lo convierte en float
            if isinstance(valor, (int, float)): return float(valor)
            #sino
            #limpia el formato de moneda:"$1,000.50" a 1000.50 eliminando la "," y el "$" y lo convierte a float
            return float(str(valor).replace("$", "").replace(",", "").strip())
        except:
            #si falla la conversion devuelve 0.0
            return 0.0


    def construir_mensaje(self) -> str:
        #carga datos maestros
        #devuelve diccionario {usuario_id: {datos_usuario}}
        usuarios_map = self.usuarios_repo.obtener_usuarios()
        
        
        """
        devuelve un diccionario de diccionarios:
        {
            id #: {
                datos_suscripcion
            },
            ...
        }
        {
            1: {
                'suscripcion_id': 1, 
                'usuario_id': 1, 
                'servicio_id': 1, 
                'activa': 'TRUE'
            }, 
            2: {
                'suscripcion_id': 2, 
                'usuario_id': 2, 
                'servicio_id': 1, 
                'activa': 'TRUE'
            }
        }
        
        """
        suscripciones_map = {s["suscripcion_id"]: s for s in self.suscripciones_repo.ws.get_all_records()}
        #Diccionario {id_servicio: {datos_suscripcion}}
        servicios_map = self.servicios_repo.obtener_servicios()
        #lista de todos los movimientos de la tabla movimientos
        movimientos = self.movimientos_repo.obtener_servicios()

        #agrupar todo por Usuario
        """
        defaultdict crea una llave con valor por defecto
        en este caso, para pagos es float (0.0) y para cargos es una lista vacía []
        1. pagos_globales = {usuario_id: total_pagos}
        2. cargos_globales = {usuario_id: [lista_de_cargos]} 
        """
        #acumula pagos por usuario
        pagos_globales = defaultdict(float)
        #acumula cargos por usuario
        cargos_globales = defaultdict(list)

        
        for mov in movimientos:
            #busca la suscripcion relacionada con este movimeiento
            sub = suscripciones_map.get(mov["suscripcion_id"])
            #sino existe suscripcion la salta
            if not sub: continue
            
            #id del usuario (u_id = user_id)
            u_id = sub["usuario_id"]
            #formatea el monto a float
            monto = self.formatear_monto(mov["monto"])
            #tipo de movimiento: CARGO o PAGO
            tipo = str(mov.get("tipo", "CARGO")).upper().strip()

            #si el tipo es pago
            if tipo == "PAGO":
                #acumula en pagos globales del usuario correspondiente
                pagos_globales[u_id] += monto
            else:
                #almacena cada cargo con sus detalles
                cargos_globales[u_id].append({
                    #mes facturado
                    "mes": mov["mes"],
                    #id del servicio (service_id)
                    "s_id": sub["servicio_id"],
                    #monto del cargo
                    "monto": monto
                })
                
        #construiye el mensaje
        #en la variable lineas se van agregando las lineas del mensaje final
        lineas = ["CUENTAS\n"]
        #variable para saber si hay deuda en general
        hay_deuda_general = False

        #combinamos usuarios que tinen cargos o pagos
        """
        si tenemos:
        cargos_globales = {"usuario1": 100, "usuario2": 200}
        pagos_globales = {"usuario2": 50, "usuario3": 150}
        
        todos_los_usuarios_con_actividad retorna un diccionario de todos los usuarios 
        {"usuario1", "usuario2", "usuario3"}
        """
        todos_los_usuarios_con_actividad = set(cargos_globales.keys()) | set(pagos_globales.keys())

        #para guardar los datos del dashboard
        filas_dashboard = []

        #convierte a todos lo usuarios con actividad en una lista ordenada y la recorre
        for u_id in sorted(todos_los_usuarios_con_actividad):
            
            #obtiene la informacion del usuario 
            usuario_data = usuarios_map.get(u_id)
            #si no hay pasa a la siguiente
            if not usuario_data: continue
            
            #obtiene el nombre del usuario
            nombre_usuario = usuario_data["nombre"]
            #si no tiene cargos, usamos una lista vacía para que el bucle no falle
            lista_cargos_usuario = cargos_globales.get(u_id, [])
            #ordena los cargos por mes (mas antiguos primero)
            """
            si tenemos:
            [
                {"mes": 3, "monto": 100},
                {"mes": 1, "monto": 200},
                {"mes": 2, "monto": 150}
            ]
            
            retornamos:
            [
                {"mes": 1, "monto": 200},
                {"mes": 2, "monto": 150},
                {"mes": 3, "monto": 100}
            ]
            """
            todos_los_cargos = sorted(lista_cargos_usuario, key=lambda x: x["mes"])
            
            #pagos disponibles para este usuario
            saldo_pagos = pagos_globales.get(u_id, 0.0)
            
            #agrupa deudas por servicio
            deuda_final_por_servicio = defaultdict(list)
            #acumula deuda total del usuario
            total_usuario = 0

            # Procesar cargos (si existen)
            for cargo in todos_los_cargos:
                #obtrenemos el monto
                monto_cargo = cargo["monto"]
                #obtenemos el nombre del servicio
                nombre_srv = servicios_map.get(cargo["s_id"], {}).get("nombre", "Servicio")
                
                #lo que queda por pagar despues de aplicar pagos
                monto_pendiente = 0
                
                if saldo_pagos >= monto_cargo:
                    #el pago cubre completamente el cargo
                    #se reduce el saldo disponible
                    saldo_pagos -= monto_cargo
                elif saldo_pagos > 0:
                    #el pago cubre parcialmente el cargo
                    #calcula lo que falta
                    monto_pendiente = monto_cargo - saldo_pagos
                    #se agota el saldo
                    saldo_pagos = 0
                else:
                    #no hay saldo disponible, todo queda pendiente
                    monto_pendiente = monto_cargo

                #si queda algo pendiente despues de aplicar los pagos
                #guarda en dashboard
                if monto_pendiente > 0:
                    filas_dashboard.append([
                        #id de usuario
                        u_id,
                        #nombre de usuario
                        nombre_usuario,
                        #nombre del servicio
                        nombre_srv,
                        #mes
                        cargo["mes"],
                        #monto pendiente redondeado
                        round(monto_pendiente, 2)
                    ])

                    #prepara texto para el mensaje
                    texto_abono = " (abono)" if monto_pendiente < monto_cargo else ""
                    
                    """
                    devuelve • 2025-09: $2.00 (abono)
                    """
                    deuda_final_por_servicio[nombre_srv].append(
                        f"    • {cargo['mes']}: ${monto_pendiente:.2f}{texto_abono}"
                    )
                    
                    total_usuario += monto_pendiente

            #formatea el mensaje del usuario
            if deuda_final_por_servicio:
                #hay al menos un usuario con deuda
                hay_deuda_general = True
                #agregamos el nombre del usuario en mayusculas al mensaje
                lineas.append(f"👤 {nombre_usuario.upper()}")
                
                for srv_nombre, detalles in deuda_final_por_servicio.items():
                    #nombre del servicio
                    lineas.append(f"   *{srv_nombre}*")
                    #agrega todos los meses con deudas
                    lineas.extend(detalles)
                lineas.append(f"  *TOTAL DEUDA: ${total_usuario:.2f}*")
                #linea en blanco
                lineas.append("") 
                
                """
                USUARIO
                    *Servicio*
                        • 2025-10: $1.00
                        • 2025-11: $3.00
                        • 2025-12: $3.00
                    *TOTAL DEUDA: $7.00*
                """
            
            #si no hay deuda pero sobró dinero (saldo a favor)
            elif saldo_pagos > 0:
                hay_deuda_general = True
                lineas.append(f"👤 {nombre_usuario.upper()}")
                lineas.append(f"    Saldo a favor global: ${saldo_pagos:.2f}")
                lineas.append("")
        
        #guarda en la tabla de dashboard los resultados del calculo
        self.dashboard_repo.sobrescribir(filas_dashboard)

        #retorna el mensaje o indicacion de que todos estan al dia
        return "\n".join(lineas) if hay_deuda_general else "✔ Todos los saldos están al día."