from src.sheets.tablas.tabla_usuarios import Usuarios

def prueba_tabla_usuarios():
    print("=" * 60)
    print("PRUEBA TABLA USUARIOS")
    print("=" * 60)

    repo = Usuarios()
    usuarios = repo.obtener_usuarios()
    
    for usuario_id, usuario in usuarios.items():
        print(usuario_id, usuario)
        
    """
    Resultado esperado:
    1 {'servicio_id': 1, 'nombre': 'Servicio A', 'costo': $3.00}
    """

if __name__ == "__main__":
    prueba_tabla_usuarios()
