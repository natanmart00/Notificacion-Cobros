from dotenv import load_dotenv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv()

from services.servicio_facturacion import FacturacionService
from services.servicio_mensaje import MensajeService
from whatsapp.sender import WhatsAppSender

def main():
    # 1. Generar cargos (incluye retroactivos)
    facturacion = FacturacionService()
    facturacion.generar_cargos_retroactivos()

    # 2. Construir mensaje consolidado
    mensaje_service = MensajeService()
    mensaje = mensaje_service.construir_mensaje()

    if not mensaje.strip():
        return

    # 3. Enviar mensaje por WhatsApp
    sender = WhatsAppSender()
    sender.enviar_mensaje(mensaje)


if __name__ == "__main__":
    main()