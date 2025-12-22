from src.sheets.tablas.tabla_servicios import ServiciosRepositorio

def prueba_tabla_servicios():
    print("=" * 60)
    print("PRUEBA TABLA SERVICIOS")
    print("=" * 60)

    repo = ServiciosRepositorio()
    servicios = repo.obtener_todos()
    
    for servicio_id, servicio in servicios.items():
        print(servicio_id,servicio)
        
    """
    Resultado esperado:
    1 {'servicio_id': 1, 'nombre': 'Servicio A', 'costo': $3.00}
    """

if __name__ == "__main__":
    prueba_tabla_servicios()
