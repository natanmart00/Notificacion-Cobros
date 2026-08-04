from src.sheets.tablas.tabla_suscripciones import SuscripcionesRepositorio

def prueba_tabla_suscripciones():
    print("=" * 60)
    print("PRUEBA TABLA SUSCRIPCIONES")
    print("=" * 60)

    repo = SuscripcionesRepositorio()
    suscripciones = repo.obtener_suscripciones_activas()

    for suscripcion in suscripciones:
        print(suscripcion)
        
    """
    Resultado esperado:
    {'suscripcion_id': 1, 'nombre': 'Juan', 'servicio_id': 1, 'activa': 'TRUE'}
    {'suscripcion_id': 2, 'nombre': 'Pepito', 'servicio_id': 1, 'activa': 'TRUE'}
    """

if __name__ == "__main__":
    prueba_tabla_suscripciones()
