from dotenv import load_dotenv
load_dotenv()

from services.servicio_facturacion import FacturacionService
from services.servicio_mensaje import MensajeService


def main():
    facturacion = FacturacionService()
    mensaje_service = MensajeService()

    # 1. Generar cargos (incluye retroactivos)
    facturacion.generar_cargos_retroactivos()

    # 2. Construir mensaje de deuda
    mensaje = mensaje_service.construir_mensaje()

    if mensaje.strip():
        print(mensaje)


if __name__ == "__main__":
    main()
