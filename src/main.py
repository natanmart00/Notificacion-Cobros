from src.services.servicio_mensaje import ServicioMensaje
from src.services.servicio_notificacion import ServicioNotificacion
from src.config.settings import Settings   

def main():
    # 1. Construir el mensaje
    servicio_msj = ServicioMensaje()
    resumen = servicio_msj.construir_mensaje()

    # 2. Si hay algo que reportar, lo enviamos
    notificador = ServicioNotificacion(Settings.valor("NTFY_TEMA"))
    notificador.enviar_resumen(resumen)

if __name__ == "__main__":
    main()