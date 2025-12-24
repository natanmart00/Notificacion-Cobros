from src.sheets.tablas.tabla_movimientos import MovimientosRepositorio

def prueba_tabla_movimientos():
    print("=" * 60)
    print("PRUEBA TABLA MOVIMIENTOS")
    print("=" * 60)

    repo = MovimientosRepositorio()
    movimientos = repo.obtener_todos()

    for movimiento in movimientos:
        print(movimiento)
    
    """
    Resultado esperado:
    {'movimiento_id': 1, 'fecha': '21/12/2025', 'mes': '2025-09', 'suscripcion_id': 5, 'tipo': 'Cargo', 'monto': 3, 'origen': 'SCRIPT'}
    {'movimiento_id': 2, 'fecha': '21/12/2025', 'mes': '2025-10', 'suscripcion_id': 5, 'tipo': 'Cargo', 'monto': 3, 'origen': 'SCRIPT'}
    """

if __name__ == "__main__":
    prueba_tabla_movimientos()
