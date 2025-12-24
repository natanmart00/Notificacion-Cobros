from src.services.servicio_mensaje import ServicioMensaje
from src.services.servicio_notificacion import ServicioNotificacion
from src.config.settings import Settings   

def main():
    #construimos el mensaje
    servicio_msj = ServicioMensaje()
    resumen = servicio_msj.construir_mensaje()

    #si hay algo que reportar, lo enviamos
    notificador = ServicioNotificacion(Settings.valor("NTFY_TEMA"))
    notificador.enviar_mensaje(resumen)

if __name__ == "__main__":
    main()