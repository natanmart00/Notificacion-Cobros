import traceback
from src.services.servicio_facturacion import ServicioFacturacion
from src.services.servicio_mensaje import ServicioMensaje

def prueba_google_sheets():
    print("=" * 60)
    print("INICIANDO PRUEBA DE SISTEMA DE FACTURACIÓN")
    print("=" * 60)

    try:
        # 1. Instanciar servicios
        facturacion = ServicioFacturacion()
        mensaje_service = ServicioMensaje()

        # 2. Ejecutar generación de cargos
        print("\n[1/2] Generando cargos retroactivos...")
        # Nota: Asegúrate que tu método genere una lista de filas 
        # y que la retorne para poder medir el éxito aquí.
        cargos_generados = facturacion.generar_cargos_retroactivos()
        
        # Asumiendo que modificaste el servicio para devolver la lista de filas insertadas
        if cargos_generados and len(cargos_generados) > 0:
            print(f"✔ Éxito: Se insertaron {len(cargos_generados)} nuevos cargos en la hoja.")
        else:
            print("ℹ Info: No se encontraron meses pendientes o suscripciones nuevas.")

        print("-" * 60)

        # 3. Construir y mostrar el mensaje de deuda
        print("[2/2] Construyendo resumen de deuda...")
        mensaje = mensaje_service.construir_mensaje()

        print("\nRESULTADO DEL MENSAJE:")
        print("." * 40)
        if mensaje:
            print(mensaje)
        else:
            print("✔ El sistema indica que no hay saldos pendientes.")
        print("." * 40)

    except Exception as e:
        print("\n❌ ERROR DURANTE LA PRUEBA:")
        print(f"Tipo de error: {type(e).__name__}")
        print(f"Detalle: {e}")
        print("\nTraza del error para depuración:")
        traceback.print_exc()

    print("\n" + "=" * 60)
    print("PRUEBA FINALIZADA")
    print("=" * 60)

if __name__ == "__main__":
    prueba_google_sheets()