from src.sheets.tablas.tabla_control import ControlRepositorio

def prueba_tabla_control():
    print("=" * 60)
    print("PRUEBA TABLA CONTROL")
    print("=" * 60)

    repo = ControlRepositorio()
    parametros = repo._obtener_todos_los_registros()

    print(parametros)
    print("mes_inicial:", repo.obtener_mes_inicial())
    print("mes_actual:", repo.obtener_mes_actual())
    
    """
    Resultado esperado:
    {'mes_inicial': '2025-09', 'mes_actual': '2025-12', 'ultima_ejecucion': '2025-12-21'}
    mes_inicial: 2025-09
    mes_actual: 2025-12
    """
    

if __name__ == "__main__":
    prueba_tabla_control()