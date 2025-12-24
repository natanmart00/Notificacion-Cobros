import requests
from src.config.settings import Settings

class ServicioNotificacion:
    def __init__(self, tema_privado):
        """
        tema_privado: El nombre del canal que pusiste en la App (ej: cobranza_whatsapp_2025_privado)
        """
        self.url = f"https://ntfy.sh/{tema_privado}"

    def enviar_mensaje(self, mensaje):
        """
        Envía el resumen de deudas como una notificación push al celular.
        """
        try:
            print(f" Enviando notificación a ntfy.sh...")
            
            #realizamos la petición POST
            #ntfy usa el cuerpo de la petición (data) como el contenido del mensaje
            respuesta = requests.post(
                self.url,
                #codifica el mensaje a UTF-8
                data=mensaje.encode('utf-8'),
                #hace que suene y resalte en el telefono
                headers={
                    "Priority": "high", 
                }
            )
            
            #si el status code es 200 = exitoso
            if respuesta.status_code == 200:
                print("✅ Notificación enviada con éxito.")
            else:
                print(f"⚠️ Error en el servidor ntfy: {respuesta.status_code}")
                
        except Exception as e:
            print(f"❌ Falló el envío de la notificación: {e}")